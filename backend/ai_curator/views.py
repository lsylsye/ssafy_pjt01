import json
import random
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
from openai import OpenAI
from .models import Book, AIReviewAnalysis
from .services import (
    get_aladin_data_complete, 
    analyze_book_complete, 
    get_wikipedia_author_info,
    get_country_literature_info
)
from books.services.aladin import search_books_by_query, _to_cover500

# API 키 설정
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
)

@api_view(["POST"])
def recommend_book(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answers = data.get('answers', [])

            # 1. 사용자 성향 분석
            keywords_map = [
                ["대중적/베스트셀러", "마이너/유니크"],
                ["정보/팩트 중심", "감성/은유 중심"],
                ["비판적/분석적", "공감/이입"],
                ["탄탄한 서사/스토리", "여운/분위기"],
                ["명확한 닫힌 결말", "열린 결말/상상"],
                ["지식/성장/자기계발", "위로/힐링/도피"],
                ["완독/끈기", "찍먹/흥미위주"]
            ]
            
            user_traits = []
            for i, ans in enumerate(answers):
                if i < len(keywords_map):
                    idx = int(ans) - 1
                    user_traits.append(keywords_map[i][idx])
            
            user_summary = ", ".join(user_traits)

            # 2. DB에서 책 가져오기 (랜덤 60권 샘플링하여 토큰 절약 및 다양성 확보)
            all_books = list(Book.objects.all())
            if len(all_books) > 60:
                books = random.sample(all_books, 60)
            else:
                books = all_books

            # 3. 프롬프트용 책 목록 텍스트 생성
            book_context = ""
            for book in books:
                # 카테고리 정보도 주면 AI가 판단하기 더 좋음
                book_context += f"[ID:{book.id}] {book.title} (카테고리: {book.category_name}) / 설명: {book.description[:80]}...\n"

            # 4. 프롬프트 작성 (2권 추천 요청)
            system_prompt = "당신은 사용자의 성향을 완벽하게 분석해주는 전문 북 큐레이터입니다."
            user_prompt = f"""
            [사용자 성향]
            {user_summary}

            [도서 목록]
            {book_context}

            [요청사항]
            1. 사용자의 성향을 분석하여 [도서 목록] 중 가장 어울리는 책 **2권**을 추천해주세요.
               - 첫 번째 책: 사용자의 취향을 저격하는 **'운명의 책'**
               - 두 번째 책: 의외의 발견이 될 수 있는 **'새로운 시도'**
            2. 각 책에 대해 추천하는 이유를 2문장 내외로 매력적으로 작성하세요.
            3. 결과는 반드시 아래 JSON 포맷을 준수하여 출력하세요.

            [JSON 출력 예시]
            {{
                "recommendations": [
                    {{
                        "book_id": 10,
                        "type": "운명의 책",
                        "reason": "당신의 논리적인 성향에 딱 맞는 과학적 통찰이 담겨 있습니다."
                    }},
                    {{
                        "book_id": 45,
                        "type": "새로운 시도",
                        "reason": "가끔은 감성적인 소설로 머리를 식혀보는 건 어떨까요?"
                    }}
                ]
            }}
            """

            # 5. API 호출
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            # 6. 결과 파싱
            ai_content = response.choices[0].message.content
            result_data = json.loads(ai_content)
            recommendations = result_data.get('recommendations', [])

            response_books = []
            for item in recommendations:
                try:
                    book_id = item.get('book_id')
                    book_obj = Book.objects.get(id=book_id)
                    
                    response_books.append({
                        "id": book_obj.id,
                        "title": book_obj.title,
                        "author": book_obj.author,
                        "cover": book_obj.cover,       # 표지 URL
                        "isbn": book_obj.isbn13,       # 상세페이지 이동용
                        "description": book_obj.description,
                        "type": item.get('type'),      # 추천 타입 (운명의 책/새로운 시도)
                        "reason": item.get('reason')   # AI 추천사
                    })
                except Book.DoesNotExist:
                    continue

            return JsonResponse({
                "analysis": user_summary,  # 사용자 분석 키워드
                "books": response_books    # 추천 책 2권 리스트
            })

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST required"}, status=400)

@api_view(["GET"])
def book_ai_review(request, isbn13):
    isbn13 = (isbn13 or "").strip()

    # 간단 검증(원하면 더 엄격히)
    if not isbn13:
        return JsonResponse({"error": "isbn13 is required"}, status=400)

    # 1) 캐시 확인
    cached = AIReviewAnalysis.objects.filter(isbn13=isbn13).first()
    if cached:
        return JsonResponse({
            "story_summary": cached.story_summary or "",
            "summary_reviews": cached.summary_reviews or [],
            "keywords": cached.keywords or [],
            "recommend_targets": cached.recommend_targets or [],
            "author_info": cached.author_info or "",
            "author_works": cached.author_works or [],
            "author_image": cached.author_image or "",
        })

    # 2) 알라딘 데이터 수집
    aladin_data = get_aladin_data_complete(isbn13)
    if not aladin_data:
        return JsonResponse({"message": "도서 정보를 찾을 수 없습니다."}, status=404)

    # 3) 위키(작가 소개/사진/링크)
    wiki_intro, wiki_img, wiki_url = get_wikipedia_author_info(aladin_data.get("author", ""))

    # 4) GPT 분석(줄거리/리뷰/키워드/추천대상) 
    ai_result = analyze_book_complete(aladin_data)
    if not isinstance(ai_result, dict):
        return JsonResponse({"error": "AI 분석 실패"}, status=500)

    # 5) 저장
    obj = AIReviewAnalysis.objects.create(
        isbn13=isbn13,
        story_summary=ai_result.get("story_summary", "") or "",
        summary_reviews=ai_result.get("summary_reviews", []) or [],
        keywords=ai_result.get("keywords", []) or [],
        recommend_targets=ai_result.get("recommend_targets", []) or [],

        # ✅ 작가정보/사진은 위키로 고정
        author_info=wiki_intro or "",
        author_image=wiki_img or "",

    )

    # 6) 반환
    return JsonResponse({
        "story_summary": obj.story_summary,
        "summary_reviews": obj.summary_reviews,
        "keywords": obj.keywords,
        "recommend_targets": obj.recommend_targets,
        "author_info": obj.author_info,          # 위키 소개글
        "author_works": obj.author_works,        # (선택) GPT 기반 대표작
        "author_image": obj.author_image,        # 위키 이미지
    })


@api_view(["POST"])
def book_travel(request):
    """
    나라별 문학 가이드 + 대표 작가 + 도서 5권 검색 (사전 정의된 데이터 사용)
    """
    try:
        from .country_books_data import COUNTRY_LITERATURE_DATA
        from concurrent.futures import ThreadPoolExecutor
        
        data = json.loads(request.body)
        country = data.get("country", "").strip()
        if not country:
            return JsonResponse({"error": "country is required"}, status=400)

        # 1. 사전 정의된 데이터에서 해당 국가 정보 가져오기
        country_data = COUNTRY_LITERATURE_DATA.get(country)
        if not country_data:
            return JsonResponse({"error": f"{country}에 대한 데이터가 없습니다."}, status=404)

        # 2. 대표 작가 위키 정보 (이미지 등) 가져오기
        author_name = country_data.get("representative_author", {}).get("name")
        wiki_intro, wiki_img, wiki_url = get_wikipedia_author_info(author_name)

        # 3. 추천 도서 목록에 대해 알라딘 API 검색 (병렬 처리)
        recommended_books = country_data.get("books", [])
        
        def fetch_aladin_data(book_info):
            query = f"{book_info['title']} {book_info['author']}"
            search_results = search_books_by_query(query, max_results=1)
            if search_results:
                item = search_results[0]
                cover = _to_cover500(item.get("cover", ""))
                # 표지가 유효한 경우만 반환
                if cover and "/img/no_image" not in cover:
                    return {
                        "title": item.get("title"),
                        "author": item.get("author"),
                        "publisher": item.get("publisher"),
                        "isbn13": item.get("isbn13"),
                        "cover": cover,
                    }
            return None

        with ThreadPoolExecutor(max_workers=10) as executor:
            raw_books = list(executor.map(fetch_aladin_data, recommended_books))

        # 표지가 있는 책만 필터링하고 최대 5개만 추출
        aladin_books = [b for b in raw_books if b is not None][:5]

        return JsonResponse({
            "country": country,
            "literary_guide": country_data.get("literary_guide"),
            "author": {
                "name": author_name,
                "description": country_data.get("representative_author", {}).get("description"),
                "image": wiki_img or "",
                "wiki_url": wiki_url or ""
            },
            "books": aladin_books
        })

    except Exception as e:
        print(f"🚨 book_travel 에러: {e}")
        return JsonResponse({"error": str(e)}, status=500)