# 📚 잔디북 - AI 기반 도서 추천 및 커뮤니티 플랫폼

## 📋 목차
- [프로젝트 개요](#-프로젝트-개요)
- [팀원 정보 및 업무 분담](#-팀원-정보-및-업무-분담)
- [목표 서비스 및 실제 구현 정도](#-목표-서비스-및-실제-구현-정도)
- [데이터베이스 모델링 (ERD)](#-데이터베이스-모델링-erd)
- [추천 알고리즘에 대한 기술적 설명](#-추천-알고리즘에-대한-기술적-설명)
- [핵심 기능에 대한 설명](#-핵심-기능에-대한-설명)
- [생성형 AI를 활용한 부분](#-생성형-ai를-활용한-부분)
- [서비스 URL](#-서비스-url)
- [설치 및 실행 방법](#-설치-및-실행-방법)

---

## 🎯 프로젝트 개요

**잔디북**은 사용자의 독서 취향을 분석하여 맞춤형 도서를 추천하고, 독서 활동을 기록하며, 다른 독서가들과 소통할 수 있는 종합 독서 플랫폼입니다.

### 주요 특징
- 🤖 **AI 기반 개인화 추천**: OpenAI API를 활용한 맞춤형 도서 추천
- 📊 **독서 활동 시각화**: GitHub 스타일의 잔디(Grass) 시스템으로 독서 활동 추적
- 🌍 **Book Travel**: 국가별 베스트셀러 탐색 및 문학 가이드 제공
- 💬 **커뮤니티**: 리뷰, 자유게시판, 댓글 시스템을 통한 독서가 간 소통
- 📖 **나만의 서재**: 북마크, 리뷰 작성, 독서 통계 관리

### 기술 스택

#### Backend
- **프레임워크**: Django 5.2.9, Django REST Framework 3.16.1
- **데이터베이스**: SQLite3
- **인증**: JWT (djangorestframework-simplejwt 5.5.1)
- **API 문서화**: drf-yasg 1.21.11
- **외부 API**: 
  - 알라딘 Open API (도서 정보)
  - OpenAI API (AI 추천 및 큐레이션)

#### Frontend
- **프레임워크**: Vue 3.5.25
- **빌드 도구**: Vite 7.2.4
- **상태 관리**: Pinia 3.0.4
- **라우팅**: Vue Router 4.6.3
- **HTTP 클라이언트**: Axios 1.13.2
- **UI 컴포넌트**: 
  - Lucide Vue Next (아이콘)
  - Swiper 12.0.3 (캐러셀)
  - Vue3 Calendar Heatmap 2.0.5 (활동 시각화)

---

## 👥 팀원 정보 및 업무 분담

### 팀 구성
- **팀명**: SSAFY 12기 관통 PJT 1팀
- **프로젝트 기간**: 2025년 12월

### 업무 분담

#### Backend 개발
- **인증/사용자 관리**: 회원가입, 로그인, JWT 인증, 프로필 관리
- **도서 관리**: 알라딘 API 연동, 베스트셀러 동기화, 도서 검색
- **커뮤니티**: 게시판, 댓글, 좋아요 시스템
- **AI 큐레이션**: OpenAI API 연동, 추천 알고리즘 구현
- **독서 활동 추적**: Grass 시스템, 경험치 관리

#### Frontend 개발
- **UI/UX 디자인**: 반응형 레이아웃, 다크 모드 지원
- **페이지 구현**:
  - 홈, 검색, 도서 상세
  - 로그인/회원가입, 취향 테스트
  - 커뮤니티 (자유게시판, 리뷰)
  - 마이페이지, 나의 서재
  - Book Travel
- **상태 관리**: Pinia를 활용한 전역 상태 관리
- **API 연동**: Axios 인터셉터를 통한 인증 처리

---

## 🎯 목표 서비스 및 실제 구현 정도

### 계획된 핵심 기능

#### 1. ✅ 사용자 인증 및 프로필 관리
- 회원가입/로그인 (JWT 기반)
- 프로필 편집 (닉네임, 소개, 프로필 이미지, 선호 국가/장르)
- 팔로우/팔로잉 시스템
- **구현 완료**: 100%

#### 2. ✅ 도서 정보 및 검색
- 알라딘 API 연동 베스트셀러 자동 동기화
- 도서 검색 및 상세 정보 조회
- 북마크 기능
- **구현 완료**: 100%

#### 3. ✅ AI 기반 추천 시스템
- 취향 테스트를 통한 초기 추천
- 사용자 활동 기반 맞춤 추천
- Book Travel: 국가별 베스트셀러 및 문학 가이드
- **구현 완료**: 100%

#### 4. ✅ 커뮤니티 기능
- 자유게시판 및 리뷰 게시판
- 댓글 및 대댓글 시스템
- 좋아요 기능
- 말머리(Prefix) 시스템
- **구현 완료**: 100%

#### 5. ✅ 독서 활동 추적
- GitHub 스타일 잔디(Grass) 시스템
- 리뷰/댓글 작성 시 자동 경험치 획득
- 독서 통계 시각화
- **구현 완료**: 100%

#### 6. ✅ 나만의 서재
- 북마크한 도서 관리
- 작성한 리뷰 목록
- 커뮤니티 활동 내역
- 독서 레벨 및 경험치 표시
- **구현 완료**: 100%

### 추가 구현 기능
- 반응형 디자인 및 다크 모드 지원
- 실시간 검색 기능
- 프로필 이미지 업로드
- 사용자 간 프로필 조회
- 베스트셀러 자동 업데이트 시스템

### 전체 구현 완료율: **100%**

---

## 🗄️ 데이터베이스 모델링 (ERD)

> **상세한 DBML 형식의 ERD는 [`ERD.md`](./ERD.md) 파일을 참고하세요.**

### 주요 테이블 구조 (DBML 형식)

#### 1. 사용자 (Users)
```python
User (사용자)
├── id (기본키)
├── username (고유, 로그인 ID)
├── email (고유)
├── nickname (고유, 닉네임)
├── bio (소개글)
├── profile_image (프로필 이미지)
├── favorite_country (선호 국가)
├── favorite_genre (선호 장르)
└── exp_total (총 경험치)

Follow (팔로우)
├── id (기본키)
├── from_user (외래키 → User, 팔로우하는 사용자)
├── to_user (외래키 → User, 팔로우받는 사용자)
└── created_at (생성일시)
```

#### 2. 도서 (Books)
```python
Book (도서)
├── id (기본키)
├── isbn13 (고유, ISBN-13)
├── title (제목)
├── author (저자)
├── publisher (출판사)
├── pub_date (출판일)
├── description (설명)
├── cover (표지 이미지 URL)
├── sales_point (판매지수)
├── category_id (카테고리 ID)
└── category_name (카테고리명)

AladinListItem (알라딘 베스트셀러 캐시)
├── id (기본키)
├── query_type (쿼리 타입: Bestseller, ItemNewAll 등)
├── item_id (알라딘 상품 ID)
├── isbn13 (ISBN-13)
├── title, author, publisher (도서 정보)
├── best_rank (베스트셀러 순위)
└── sales_point (판매지수)

Bookmark (북마크)
├── id (기본키)
├── user (외래키 → User)
├── book (외래키 → Book)
└── created_at (생성일시)
```

#### 3. 커뮤니티 (Community)
```python
Board (게시판)
├── id (기본키)
├── slug (고유: 'free', 'review')
├── name (게시판 이름)
└── board_type (게시판 타입)

Post (게시글)
├── id (기본키)
├── board (외래키 → Board)
├── user (외래키 → User)
├── prefix (외래키 → Prefix, 말머리)
├── title (제목)
├── content (내용)
├── created_at (작성일시)
└── updated_at (수정일시)

Review (리뷰)
├── id (기본키)
├── board (외래키 → Board)
├── user (외래키 → User)
├── book_title, book_author (도서 정보)
├── isbn13, publisher, cover (도서 상세)
├── content (리뷰 내용)
├── rating (평점 1-5)
├── created_at (작성일시)
└── updated_at (수정일시)

Comment (댓글, Generic Relation)
├── id (기본키)
├── user (외래키 → User)
├── content_type (외래키 → ContentType)
├── object_id (Post 또는 Review의 ID)
├── parent_comment (외래키 → Comment, 대댓글용)
├── content (댓글 내용)
└── created_at (작성일시)

Like (좋아요, Generic Relation)
├── id (기본키)
├── user (외래키 → User)
├── content_type (외래키 → ContentType)
├── object_id (대상 객체 ID)
└── created_at (생성일시)
```

#### 4. 독서 활동 (Grass)
```python
GrassDaily (일일 활동)
├── id (기본키)
├── user (외래키 → User)
├── date (날짜 YYYY-MM-DD)
├── points (일일 활동 점수)
└── updated_at (갱신일시)
```

### ERD 다이어그램
```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    User     │◄───────►│    Follow    │         │    Book     │
│  (사용자)    │         │   (팔로우)    │         │   (도서)     │
└─────────────┘         └──────────────┘         └─────────────┘
       │                                                  │
       │                                                  │
       ├──────────────────────────────────────────────────┤
       │                                                  │
       ▼                                                  ▼
┌─────────────┐                                   ┌─────────────┐
│  Bookmark   │                                   │AladinListItem│
│  (북마크)    │                                   │(베스트셀러)  │
└─────────────┘                                   └─────────────┘
       │
       │
       ├──────────────┬──────────────┬──────────────┐
       │              │              │              │
       ▼              ▼              ▼              ▼
┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐
│    Post     │ │  Review  │ │ Comment  │ │ GrassDaily  │
│  (게시글)    │ │  (리뷰)   │ │  (댓글)   │ │(일일 활동)  │
└─────────────┘ └──────────┘ └──────────┘ └─────────────┘
       │              │              │
       └──────────────┴──────────────┘
                      │
                      ▼
               ┌──────────┐
               │   Like   │
               │ (좋아요)  │
               └──────────┘
```

---

## 🧠 추천 알고리즘에 대한 기술적 설명

### 1. 취향 기반 초기 추천 (Taste Test)

#### 알고리즘 흐름
1. **사용자 입력 수집**
   - 선호 장르 (소설/시/희곡, 경제/경영, 자기계발, 인문/교양, 만화/eBook, 과학)
   - 선호 국가 (한국, 일본, 중화권, 영미권, 기타)
   - 독서 스타일 (빠른 전개, 깊은 사색, 감성적, 논리적 등)

2. **OpenAI GPT-4 활용 추천**
   ```python
   # ai_curator/views.py
   def generate_taste_recommendations(user_preferences):
       prompt = f"""
       사용자 취향:
       - 선호 장르: {user_preferences['genre']}
       - 선호 국가: {user_preferences['country']}
       - 독서 스타일: {user_preferences['style']}
       
       위 취향에 맞는 도서 10권을 추천하고, 각 도서에 대해
       제목, 저자, 출판사, 추천 이유를 JSON 형식으로 반환하세요.
       """
       
       response = openai.chat.completions.create(
           model="gpt-4",
           messages=[{"role": "user", "content": prompt}]
       )
       
       return parse_recommendations(response)
   ```

3. **알라딘 API 연동**
   - AI가 추천한 도서를 알라딘 API로 검색
   - ISBN13, 표지 이미지, 상세 정보 수집
   - DB에 저장 및 사용자에게 제공

### 2. 활동 기반 맞춤 추천

#### 데이터 수집
- 북마크한 도서
- 작성한 리뷰 (평점 포함)
- 좋아요 누른 게시글/리뷰
- 팔로우한 사용자의 활동

#### 추천 로직
```python
def get_personalized_recommendations(user):
    # 1. 사용자 활동 분석
    bookmarked_books = user.bookmarks.all()
    reviewed_books = user.book_reviews.all()
    
    # 2. 선호 장르/저자 추출
    preferred_genres = extract_genres(bookmarked_books)
    preferred_authors = extract_authors(reviewed_books)
    
    # 3. AI 프롬프트 생성
    prompt = f"""
    사용자가 좋아한 도서:
    {format_books(bookmarked_books)}
    
    사용자가 높은 평점을 준 도서:
    {format_reviews(reviewed_books)}
    
    이 사용자에게 추천할 만한 도서 10권을 제안하세요.
    """
    
    # 4. OpenAI API 호출 및 결과 반환
    return call_openai_api(prompt)
```

### 3. Book Travel 추천

#### 국가별 베스트셀러 분석
```python
def get_country_bestsellers(country_code):
    # 1. OpenAI에 국가별 베스트셀러 요청
    prompt = f"""
    {country_code} 국가의 현재 베스트셀러 도서 10권을 
    제목, 저자, 출판사 정보와 함께 JSON 형식으로 제공하세요.
    """
    
    bestsellers = openai_api_call(prompt)
    
    # 2. 알라딘 API로 도서 정보 보강
    for book in bestsellers:
        aladin_data = search_aladin(book['title'], book['author'])
        book.update(aladin_data)
    
    return bestsellers
```

#### 문학 가이드 생성
```python
def generate_literary_guide(country_code):
    prompt = f"""
    {country_code} 국가의 문학적 특징, 대표 작가, 
    추천 도서를 포함한 문학 가이드를 작성하세요.
    """
    
    return openai_api_call(prompt)
```

### 4. 협업 필터링 (Collaborative Filtering)

#### 유사 사용자 기반 추천
```python
def find_similar_users(user):
    # 1. 공통 북마크 수 계산
    similar_users = User.objects.annotate(
        common_bookmarks=Count(
            'bookmarks',
            filter=Q(bookmarks__book__in=user.bookmarks.all())
        )
    ).exclude(id=user.id).order_by('-common_bookmarks')[:10]
    
    # 2. 유사 사용자가 북마크한 도서 추천
    recommended_books = Book.objects.filter(
        bookmarked_by__user__in=similar_users
    ).exclude(
        bookmarked_by__user=user
    ).distinct()
    
    return recommended_books
```

---

## ⚙️ 핵심 기능에 대한 설명

### 1. 인증 시스템

#### JWT 기반 인증
```javascript
// frontend/src/api/axios.js
// 요청 인터셉터: 모든 API 요청에 JWT 토큰 자동 첨부
api.interceptors.request.use((config) => {
  const auth = useAuthStore();
  const token = auth.access;
  
  if (token && config.auth !== false) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 응답 인터셉터: 401 에러 시 자동 로그아웃
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const auth = useAuthStore();
      auth.logout();
      router.push({ name: "login" });
    }
    return Promise.reject(error);
  }
);
```

#### 회원가입 및 프로필 설정
- 이메일 중복 검사
- 닉네임 중복 검사
- 프로필 이미지 업로드 (Pillow 활용)
- 선호 장르/국가 설정

### 2. 도서 검색 및 상세 정보

#### 실시간 검색
```javascript
// frontend/src/stores/bookSearch.js
// Debounce를 활용한 실시간 검색 최적화
const searchBooks = debounce(async (query) => {
  if (!query.trim()) return;
  
  const response = await api.get('/books/search/', {
    params: { query, maxResults: 20 }
  });
  
  searchResults.value = response.data;
}, 300);
```

#### 도서 상세 페이지
- 알라딘 API를 통한 실시간 정보 조회
- 북마크 추가/제거
- 리뷰 작성 링크
- 관련 도서 추천

### 3. 커뮤니티 시스템

#### Generic Relation을 활용한 댓글 시스템
```python
# backend/community/models.py
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")
    parent_comment = models.ForeignKey("self", null=True, blank=True)
    content = models.TextField()
```

이를 통해 Post(게시글)와 Review(리뷰) 모두에 댓글을 달 수 있으며, 대댓글도 지원합니다.

#### 좋아요 시스템
```python
# backend/community/views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, content_type_str, object_id):
    content_type = ContentType.objects.get(model=content_type_str)
    
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    )
    
    if not created:
        like.delete()
        return Response({'liked': False})
    
    return Response({'liked': True})
```

### 4. 독서 활동 추적 (Grass System)

#### 일일 활동 점수 계산
```python
# backend/grass/utils.py
def add_grass_points(user, date, points):
    grass, created = GrassDaily.objects.get_or_create(
        user=user,
        date=date,
        defaults={'points': 0}
    )
    
    grass.points += points
    grass.save()
    
    # 경험치 추가
    user.exp_total += points
    user.save()
```

#### 활동별 점수
- 리뷰 작성: 10점
- 댓글 작성: 5점
- 게시글 작성: 5점
- 좋아요 받기: 1점

#### 프론트엔드 시각화
```vue
<!-- frontend/src/views/MyLibraryView.vue -->
<CalendarHeatmap
  :values="grassData"
  :end-date="new Date()"
  :range-color="['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']"
/>
```

### 5. 마이페이지 및 나의 서재

#### 프로필 편집
- 닉네임, 소개글 수정
- 프로필 이미지 업로드
- 선호 장르/국가 변경

#### 독서 통계
```javascript
// 레벨 계산
const level = computed(() => Math.floor(user.exp_total / 100) + 1);
const currentLevelExp = computed(() => user.exp_total % 100);
const nextLevelExp = 100;

// 진행률
const progress = computed(() => (currentLevelExp / nextLevelExp) * 100);
```

#### 활동 내역
- 북마크한 도서 목록
- 작성한 리뷰 목록
- 커뮤니티 게시글 및 댓글 목록
- 팔로워/팔로잉 관리

### 6. Book Travel

#### 국가 검색 및 베스트셀러 조회
```javascript
// frontend/src/views/BookTravelView.vue
const searchCountry = async (countryName) => {
  const response = await api.post('/ai/book-travel/', {
    country: countryName
  });
  
  bestsellers.value = response.data.bestsellers;
  literaryGuide.value = response.data.guide;
  representativeAuthor.value = response.data.author;
};
```

#### AI 문학 가이드
- 국가별 문학적 특징
- 대표 작가 소개
- 추천 도서 리스트
- 문화적 배경 설명

---

## 🤖 생성형 AI를 활용한 부분

### 1. 도서 추천 시스템

#### 사용 모델
- **OpenAI GPT-4** (또는 GPT-4.1 Nano)

#### 활용 방식
```python
# backend/ai_curator/services.py
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_ai_recommendations(user_profile):
    prompt = f"""
    당신은 전문 서점 직원입니다. 다음 사용자 정보를 바탕으로 
    도서 10권을 추천해주세요.
    
    사용자 정보:
    - 선호 장르: {user_profile['genre']}
    - 선호 국가: {user_profile['country']}
    - 최근 읽은 책: {user_profile['recent_books']}
    - 평균 평점: {user_profile['avg_rating']}
    
    각 도서에 대해 다음 정보를 JSON 형식으로 제공하세요:
    - title: 도서 제목
    - author: 저자
    - publisher: 출판사
    - reason: 추천 이유 (50자 이내)
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 도서 추천 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return json.loads(response.choices[0].message.content)
```

### 2. Book Travel 큐레이션

#### 국가별 베스트셀러 생성
```python
def generate_country_bestsellers(country):
    prompt = f"""
    {country}의 현재 베스트셀러 도서 10권을 추천해주세요.
    각 도서는 다음 정보를 포함해야 합니다:
    
    - title: 도서 제목 (원제)
    - author: 저자명
    - publisher: 출판사
    - isbn13: ISBN-13 (가능한 경우)
    
    JSON 배열 형식으로 반환하세요.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    bestsellers = json.loads(response.choices[0].message.content)
    
    # 알라딘 API로 실제 도서 정보 검색
    for book in bestsellers:
        aladin_data = search_aladin_book(book['title'], book['author'])
        if aladin_data:
            book.update(aladin_data)
    
    return bestsellers
```

#### 문학 가이드 생성
```python
def generate_literary_guide(country):
    prompt = f"""
    {country}의 문학에 대한 가이드를 작성해주세요.
    
    포함할 내용:
    1. 문학적 특징 (200자 이내)
    2. 대표 작가 3명과 그들의 대표작
    3. 추천 도서 5권과 간단한 소개
    4. 문화적 배경 설명
    
    마크다운 형식으로 작성하세요.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    
    return response.choices[0].message.content
```

### 3. 리뷰 요약 및 분석

#### 리뷰 감성 분석
```python
def analyze_review_sentiment(review_content):
    prompt = f"""
    다음 도서 리뷰의 감성을 분석하고 1-5점 척도로 평가하세요:
    
    리뷰: {review_content}
    
    다음 형식으로 응답하세요:
    {{
        "sentiment": "긍정적/중립적/부정적",
        "score": 1-5,
        "keywords": ["키워드1", "키워드2", "키워드3"]
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return json.loads(response.choices[0].message.content)
```

### 4. 프롬프트 엔지니어링 기법

#### Few-Shot Learning (예시 기반 학습)
```python
def get_genre_recommendations(genre):
    prompt = f"""
    다음은 장르별 추천 도서의 예시입니다:
    
    장르: 소설/시/희곡
    추천: [
        {{"title": "1984", "author": "조지 오웰", "reason": "디스토피아 소설의 고전"}},
        {{"title": "노르웨이의 숲", "author": "무라카미 하루키", "reason": "청춘의 아픔을 섬세하게 그린 작품"}}
    ]
    
    장르: {genre}
    추천: 
    """
    # ... OpenAI API 호출
```

#### Chain of Thought (단계별 사고)
```python
def get_detailed_recommendations(user_data):
    prompt = f"""
    사용자 분석을 단계별로 수행하세요:
    
    1단계: 사용자의 독서 패턴 분석
    - 최근 읽은 책: {user_data['recent_books']}
    - 평균 평점: {user_data['avg_rating']}
    
    2단계: 선호 장르 및 스타일 파악
    - 선호 장르: {user_data['genre']}
    - 독서 스타일: {user_data['style']}
    
    3단계: 추천 도서 선정 (각 단계의 분석을 바탕으로)
    
    최종 추천:
    """
    # ... OpenAI API 호출
```

### 5. AI 활용 최적화

#### 캐싱 전략
```python
from django.core.cache import cache

def get_cached_recommendations(cache_key, generator_func, *args):
    # 캐시 확인
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result
    
    # AI 호출
    result = generator_func(*args)
    
    # 캐시 저장 (24시간)
    cache.set(cache_key, result, 60 * 60 * 24)
    
    return result
```

#### 비용 최적화
- 동일한 요청에 대한 캐싱
- 토큰 수 제한 (max_tokens 설정)
- 필요한 경우에만 GPT-4 사용, 간단한 작업은 GPT-3.5 사용
- 배치 처리를 통한 API 호출 최소화

---

## 🌐 서비스 URL

### 개발 환경

#### Backend
- **URL**: `http://127.0.0.1:8000`
- **API 문서**: `http://127.0.0.1:8000/swagger/`
- **관리자 페이지**: `http://127.0.0.1:8000/admin/`

#### Frontend
- **URL**: `http://localhost:5173`

### 배포 환경 (예정)
- **Frontend**: Vercel / Netlify
- **Backend**: AWS EC2 / Heroku
- **Database**: PostgreSQL (AWS RDS)
- **Media Files**: AWS S3

---

## 📦 설치 및 실행 방법

### 1. 저장소 클론
```bash
git clone <repository-url>
cd ssafy_pjt01
```

### 2. Backend 설정

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정 (.env 파일 생성)
cat > .env << EOF
ALADIN_TTB_KEY=your_aladin_api_key
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_django_secret_key
EOF

# 데이터베이스 마이그레이션
python manage.py migrate

# 슈퍼유저 생성 (선택사항)
python manage.py createsuperuser

# 개발 서버 실행
python manage.py runserver
```

### 3. Frontend 설정

```bash
cd frontend

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```

### 주요 API 엔드포인트

#### 인증
- `POST /accounts/signup/` - 회원가입
- `POST /accounts/login/` - 로그인
- `GET /api/mypage/me/` - 현재 사용자 정보

#### 도서
- `GET /api/books/` - 도서 목록
- `GET /api/books/search/` - 도서 검색
- `GET /api/books/{isbn13}/` - 도서 상세
- `POST /api/books/{isbn13}/bookmark/` - 북마크 토글

#### 커뮤니티
- `GET /api/community/boards/` - 게시판 목록
- `GET /api/community/posts/` - 게시글 목록
- `POST /api/community/posts/` - 게시글 작성
- `GET /api/community/posts/{id}/` - 게시글 상세
- `POST /api/community/posts/{id}/comments/` - 댓글 작성

#### 리뷰
- `GET /api/review/` - 리뷰 목록
- `POST /api/review/` - 리뷰 작성
- `GET /api/review/{id}/` - 리뷰 상세

#### AI 큐레이션
- `POST /api/ai/taste-test/` - 취향 테스트 기반 추천
- `POST /api/ai/book-travel/` - 국가별 베스트셀러 조회
- `GET /api/ai/recommendations/` - 개인화 추천

### 환경 변수 설정

#### Backend (.env)
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# 알라딘 API
ALADIN_TTB_KEY=your-aladin-api-key
ALADIN_API_VERSION=20131101

# OpenAI
OPENAI_API_KEY=your-openai-api-key
```

### 테스트 계정
```
아이디: user1
비밀번호: test1234!
닉네임: 금잔디
```

### 프로젝트 구조

```
ssafy_pjt01/
├── backend/
│   ├── config/              # Django 설정
│   ├── users/               # 사용자 관리
│   ├── books/               # 도서 관리
│   ├── community/           # 커뮤니티 (게시판, 댓글, 좋아요)
│   ├── reviews/             # 리뷰
│   ├── grass/               # 독서 활동 추적
│   ├── ai_curator/          # AI 추천 시스템
│   ├── mypage/              # 마이페이지
│   ├── media/               # 업로드 파일
│   ├── requirements.txt     # Python 패키지
│   └── .env                 # 환경 변수 (gitignore)
│
├── frontend/
│   ├── src/
│   │   ├── api/             # API 호출 함수
│   │   ├── components/      # 재사용 컴포넌트
│   │   ├── views/           # 페이지 컴포넌트
│   │   ├── stores/          # Pinia 스토어
│   │   ├── router/          # Vue Router 설정
│   │   ├── styles/          # CSS 파일
│   │   └── main.js          # 앱 진입점
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

### 향후 개선 계획

1. **성능 최적화**
   - Redis 캐싱 도입
   - 이미지 최적화 (WebP 변환)
   - 무한 스크롤 페이지네이션

2. **기능 추가**
   - 독서 모임 기능
   - 도서 대여/교환 시스템
   - 독서 챌린지 및 뱃지 시스템
   - 알림 기능 (팔로워 활동, 댓글 등)

3. **AI 고도화**
   - 사용자 행동 기반 실시간 추천
   - 리뷰 자동 요약 기능
   - 도서 간 유사도 분석

4. **모바일 앱**
   - React Native / Flutter 기반 모바일 앱 개발
   - 푸시 알림 지원

### 라이선스
MIT License

---

**잔디북** - 당신의 독서 여정을 함께합니다 📚✨
