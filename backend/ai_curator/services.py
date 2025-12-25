# backend/ai_curator/services.py

import requests
import json
import re
import xml.etree.ElementTree as ET
from django.conf import settings
from openai import OpenAI

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
)


def get_aladin_data_complete(isbn13: str):
    ttb_key = getattr(settings, "ALADIN_TTB_KEY", None)
    if not ttb_key:
        print("🚨 오류: settings.py에 ALADIN_TTB_KEY가 없습니다.")
        return None

    url = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"
    params = {
        "ttbkey": ttb_key,
        "itemIdType": "ISBN13",
        "ItemId": isbn13,
        "output": "xml",
        "Version": "20131101",
        "OptResult": "reviewList,description",
    }

    try:
        res = requests.get(url, params=params, timeout=7)
        res.raise_for_status()
        root = ET.fromstring(res.text)

        # ✅ 네임스페이스 대응
        item = root.find(".//{*}item")
        if item is None:
            return None

        title = (item.findtext("{*}title") or "").strip()
        author = (item.findtext("{*}author") or "").strip()
        description = (item.findtext("{*}description") or "").strip()

        reviews = []
        for r in item.findall(".//{*}review"):
            t = (r.findtext("{*}title") or "").strip()
            t = t.replace("[100자평]", "").replace("[마이리뷰]", "").strip()
            if t:
                reviews.append(t)

        return {
            "title": title,
            "author": author,
            "description": description,
            "reviews": reviews,
        }

    except Exception as e:
        print(f"🚨 알라딘 API 요청 실패: {e}")
        return None


def analyze_book_complete(book_data):
    """
    ✅ 프롬프트는 건드리지 않음 (요청대로 그대로 유지)
    """
    if not book_data:
        return None

    title = book_data["title"]
    author = book_data["author"]
    desc = book_data["description"] if book_data["description"] else "제공된 설명 없음"
    reviews_text = "\n".join(book_data["reviews"][:30]) if book_data["reviews"] else "리뷰 없음"

    prompt = f"""
    당신은 20년 경력의 베스트셀러 북 큐레이터입니다.
    아래 정보를 바탕으로 독자에게 어필할 수 있는 매력적인 콘텐츠를 JSON으로 만들어주세요.

    [책 정보]
    - 제목: {title}
    - 저자: {author}
    - 알라딘 제공 설명: {desc}
    - 독자들의 실제 리뷰: {reviews_text}

    [필수 요청 사항 (JSON 필드)]
    
    1. "story_summary" (문자열): 
       - 이 책의 핵심 줄거리를 3~4줄로 요약하세요.
       - 중요: 만약 '알라딘 제공 설명'이 빈약하다면, 당신이 가진 '{title} ({author})'에 대한 지식을 활용해서 줄거리를 완성하세요.
       - 스포일러 없이, 독자가 읽고 싶어지도록 흥미롭게 작성하세요.

    2. "summary_reviews" (문자열 리스트, 5개):
       - 제공된 '독자들의 실제 리뷰'를 분석하여 가장 많이 언급된 호평 포인트 5가지를 문장으로 요약하세요. (~해요체)
    
    3. "keywords" (문자열 리스트, 3~5개):
       - 이 책을 관통하는 핵심 단어(테마, 감정, 장르 등)를 뽑아주세요.
       
    4. "recommend_targets" (문자열 리스트, 3개):
       - 이 책을 읽으면 특히 좋을 것 같은 독자 유형 3가지를 구체적으로 추천해주세요.


    [응답 포맷 예시]
    {{
        "story_summary": "600년을 산 팽나무의 시선으로...",
        "summary_reviews": ["작가의 필력이 대단해요.", "여운이 깊게 남아요."],
        "keywords": ["가족", "역사", "자연"],
        "recommend_targets": ["지친 일상에 위로가 필요한 분", "황석영 작가의 팬"],
    }}
    
    조건: 반드시 JSON 형식을 지키고, 한국어 존댓말(~해요)을 사용하세요.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 유능한 북 큐레이터입니다. JSON 형식으로만 응답하세요."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"🚨 GPT 호출 오류: {e}")
        return None


def _clean_author_for_wiki(author_name: str) -> str:
    if not author_name:
        return ""

    s = str(author_name).strip()

    # "댄 브라운 (지은이), 양선아 (옮긴이)" → "댄 브라운 (지은이)"
    if "," in s:
        s = s.split(",", 1)[0].strip()

    # "댄 브라운 (지은이)" → "댄 브라운"
    if "(" in s:
        s = s.split("(", 1)[0].strip()

    return s


def get_wikipedia_author_info(author_name: str):
    """
    위키 소개글/썸네일 + (추가) 위키 페이지 URL까지 반환
    """
    if not author_name:
        return None, None, None

    clean_name = _clean_author_for_wiki(author_name)
    if not clean_name:
        return None, None, None

    url = "https://ko.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts|pageimages|info",
        "inprop": "url",
        "titles": clean_name,
        "pithumbsize": 300,
        "exintro": True,
        "explaintext": True,
        "redirects": 1,
    }

    try:
        res = requests.get(url, params=params, timeout=7, headers={"User-Agent": "JandiBook/1.0"})
        data = res.json()

        pages = data.get("query", {}).get("pages", {})
        if not pages:
            return None, None, None

        page_id = next(iter(pages))
        if page_id == "-1":
            return None, None, None

        page = pages[page_id]
        intro = page.get("extract", "") or ""
        image_url = page.get("thumbnail", {}).get("source")
        page_url = page.get("fullurl")
        return intro, image_url, page_url

    except Exception as e:
        print(f"🚨 위키피디아 API 에러: {e}")
        return None, None, None


def get_country_literature_info(country_name: str):
    """
    나라 이름을 바탕으로 AI 문학 가이드, 대표 작가 정보, 그리고 10권의 추천 도서 목록을 생성합니다.
    """
    prompt = f"""
    당신은 세계 북트래블 가이드이자 북 큐레이터입니다.
    '{country_name}'을(를) 대표하는 문학적 특징과 대표 작가, 그리고 한국에서 읽을 수 있는 베스트셀러/대표 도서 10권을 추천해주세요.

    [필수 요청 사항 (JSON 필드)]
    1. "literary_guide" (문자열): 
       - {country_name} 문학의 특징, 역사적 배경, 혹은 읽기 전에 알면 좋은 팁을 3~4줄로 매력적으로 작성하세요.
    2. "representative_author" (객체):
       - "name": {country_name}을 대표하는 작가 이름
       - "description": 작가에 대한 짧은 소개 (1~2줄)
    3. "recommended_books" (배열, 10개):
       - 각 항목은 객체여야 합니다: {{"title": "책 제목", "author": "저자 이름"}}
       - 한국의 알라딘 API에서 검색이 가능할 법한 유명한 책들로 구성하세요.

    [응답 포맷 예시]
    {{
        "literary_guide": "영국 문학은 셰익스피어의 고전부터 현대 판타지까지...",
        "representative_author": {{
            "name": "J.K. 롤링",
            "description": "전 세계를 매료시킨 판타지의 거장"
        }},
        "recommended_books": [
            {{"title": "해리 포터와 마법사의 돌", "author": "J.K. 롤링"}},
            ...
        ]
    }}

    조건: 반드시 JSON 형식을 지키고, 한국어 존댓말(~해요)을 사용하세요.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 세계 문학 전문가입니다. JSON 형식으로만 응답하세요."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"🚨 GPT 호출 오류 (Book Travel): {e}")
        return None
