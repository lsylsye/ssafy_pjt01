import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from openai import OpenAI
from .models import Book

# API 키 설정
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
)

@csrf_exempt
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