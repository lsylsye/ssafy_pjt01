<!-- BookDetailView.vue -->
<template>
  <section class="page">
    <!-- ✅ 기본 도서 정보 로딩/에러 -->
    <div v-if="bookLoading" class="state">
      <div class="spinner"></div>
      <p>도서 정보를 불러오는 중...</p>
    </div>

    <div v-else-if="bookError" class="state">
      <p>{{ bookError }}</p>
      <button class="btn" @click="loadPage(isbn13)">다시 시도</button>
    </div>

    <!-- ✅ 기본 도서 정보 -->
    <div v-else-if="book" class="container">
      <!-- 상단 2컬럼: 왼쪽(텍스트) / 오른쪽(표지) -->
      <header class="top">
        <div class="left">
          <p v-if="book.category_name" class="category">
            {{ book.category_name }}
          </p>

          <h1 class="title">{{ book.title }}</h1>

          <div class="meta">
            <p><strong>저자</strong> {{ book.author }}</p>
            <p><strong>출판사</strong> {{ book.publisher }}</p>

            <!-- ✅ 독자 별점(별) -->
            <p v-if="hasRank">
              <strong>독자 별점</strong>
              <span class="stars" :aria-label="`독자 별점 ${ratingText}`">
                <span class="stars-back">★★★★★</span>
                <span class="stars-front" :style="{ width: starFillWidth }">★★★★★</span>
              </span>
              <span class="rating-num">{{ ratingText }}</span>
            </p>
          </div>

          <!-- ✅ 버튼: 북마크 + 리뷰작성 유지 -->
          <div class="btn-row">
            <button class="btn" :class="{ active: isBookmarked }" @click="handleBookmark">
              {{ isBookmarked ? '북마크 해제' : '북마크 추가' }}
            </button>
            <button class="btn" @click="goReviewWrite">
              리뷰 작성
            </button>
          </div>

          <!-- 기본 책 소개 -->
          <div v-if="book.description" class="desc">
            <h3>책 소개</h3>
            <p>{{ book.description }}</p>
          </div>
        </div>

        <div class="right">
          <img :src="book.cover" alt="표지" class="cover" />
        </div>
      </header>

      <!-- ✅ AI 큐레이팅(기본 정보와 분리, 여기만 별도 로딩) -->
      <section class="ai-wrap">
        <div class="ai-head">
          <h2>AI 큐레이팅</h2>
          <button v-if="aiError" class="btn subtle" @click="fetchAiCuration(isbn13)">다시 시도</button>
        </div>

        <!-- AI 로딩 -->
        <div v-if="aiLoading" class="ai-state">
          <div class="spinner small"></div>
          <p>도서 정보를 큐레이팅 하고 있어요...</p>
        </div>

        <!-- AI 에러 -->
        <div v-else-if="aiError" class="ai-state error">
          <p>{{ aiError }}</p>
        </div>

        <!-- AI 성공 -->
        <div v-else-if="aiData" class="ai-grid">
          <!-- 1) 요약 + 키워드 -->
          <div class="card">
            <h3>✨ AI 3줄 요약</h3>
            <p class="ai-text">{{ aiData.story_summary }}</p>

            <div v-if="aiData.keywords?.length" class="chips">
              <span v-for="k in aiData.keywords" :key="k" class="chip">#{{ k }}</span>
            </div>
          </div>

          <!-- 2) 추천 대상 -->
          <div class="card">
            <h3>이런 분께 추천해요</h3>
            <ul class="list">
              <li v-for="(t, idx) in aiData.recommend_targets || []" :key="idx">
                ✔ {{ t }}
              </li>
            </ul>
          </div>

          <!-- 3) 리뷰 요약 -->
          <div class="card">
            <h3>독자들의 반응</h3>
            <div class="bubbles">
              <div v-for="(r, idx) in aiData.summary_reviews || []" :key="idx" class="bubble">
                "{{ r }}"
              </div>
            </div>
          </div>

          <!-- 4) 작가 소개(위키 연결) -->
          <div class="card author">
            <h3>작가 소개</h3>

            <div class="author-row">
              <img
                :src="aiData?.author_image || defaultProfile"
                alt="작가 사진"
                class="author-img"
              />

              <div class="author-body">
                <div class="author-title">
                  <span class="author-name">{{ extractAuthorName(book.author) }}</span>

                  <!-- 백엔드에서 page_url 내려주면 링크 -->
                  <a
                    v-if="aiData.author_page_url"
                    class="wiki-link"
                    :href="aiData.author_page_url"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    위키에서 보기 →
                  </a>
                </div>

                <p class="author-desc">{{ aiData.author_info }}</p>

                <div v-if="aiData.author_works?.length" class="works">
                  <span class="works-label">대표작</span>
                  <div class="chips">
                    <span v-for="w in aiData.author_works" :key="w" class="chip subtle"> {{ w }} </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <p class="disclaimer">
            * 제공된 요약/키워드/리뷰/작가 정보는 AI가 분석 및 생성한 정보로 실제 내용과 다를 수 있습니다.
          </p>
        </div>
      </section>
    </div>

    <div v-else class="state">
      <p>도서 정보를 찾을 수 없습니다.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import { useBookmarkStore } from '@/stores/bookmark'
import defaultProfile from '@/assets/default_profile.jpg'

const route = useRoute()
const router = useRouter()
const bookmarkStore = useBookmarkStore()

const book = ref(null)
const bookLoading = ref(false)
const bookError = ref('')

const aiData = ref(null)
const aiLoading = ref(false)
const aiError = ref('')

const isbn13 = computed(() => String(route.params.isbn13 || ''))
const isBookmarked = computed(() => bookmarkStore.isBookmarked(isbn13.value))
const isLoggedIn = () => !!localStorage.getItem('access_token')

/** "황석영 (지은이)" -> "황석영" */
const extractAuthorName = (authorString) => {
  if (!authorString) return '작가'
  return String(authorString).split('(')[0].trim()
}

/** ✅ 별점: 10점(customerReviewRank) -> 5점 */
const hasRank = computed(() => book.value?.customerReviewRank !== undefined && book.value?.customerReviewRank !== null)

const rating10 = computed(() => {
  const v = Number(book.value?.customerReviewRank)
  return Number.isFinite(v) ? Math.max(0, Math.min(10, v)) : null
})

const rating5 = computed(() => {
  if (rating10.value === null) return null
  return rating10.value / 2
})

const ratingText = computed(() => {
  if (rating5.value === null) return ''
  return `${rating5.value.toFixed(1)} / 5`
})

const starFillWidth = computed(() => {
  if (rating5.value === null) return '0%'
  return `${(rating5.value / 5) * 100}%`
})

/** ✅ 기본 도서 정보: /api/books/${isbn13}/ */
const fetchBookDetail = async (isbn) => {
  if (!isbn) return
  bookLoading.value = true
  bookError.value = ''
  book.value = null

  try {
    const res = await api.get(`/api/books/${isbn}/`)
    book.value = res.data
  } catch (err) {
    console.error('[도서 상세 조회 실패]', err.response?.data || err.message)
    bookError.value = '도서 정보를 불러오지 못했습니다.'
  } finally {
    bookLoading.value = false
  }
}

/** ✅ AI 큐레이팅: /api/ai_curator/${isbn13}/ (기본 정보와 분리 로딩) */
const fetchAiCuration = async (isbn) => {
  if (!isbn) return
  aiLoading.value = true
  aiError.value = ''
  aiData.value = null

  try {
    const res = await api.get(`/api/ai_curator/${isbn}/`)
    aiData.value = res.data
  } catch (err) {
    console.error('[AI 큐레이팅 실패]', err.response?.data || err.message)
    aiError.value = 'AI 큐레이팅 정보를 불러오지 못했습니다.'
  } finally {
    aiLoading.value = false
  }
}

const handleBookmark = () => {
  if (!isbn13.value) return

  if (!isLoggedIn()) {
    alert('로그인이 필요한 기능입니다.')
    router.push('/login')
    return
  }

  bookmarkStore.toggle(isbn13.value)
    .catch((err) => {
      if (err?.code === 'LOGIN_REQUIRED') {
        alert('로그인이 필요한 기능입니다.')
        router.push('/login')
        return
      }
      if (err?.response?.status === 401) {
        alert('로그인이 만료되었습니다. 다시 로그인해주세요.')
        router.push('/login')
        return
      }
      console.error('[북마크 토글 실패]', err?.response?.data || err?.message || err)
      alert('북마크 처리에 실패했습니다.')
    })
}

/** ✅ 리뷰 작성 페이지 이동(기본 정보 기반) */
const goReviewWrite = () => {
  if (!book.value) return
  router.push({
    path: '/community/kr/review/write',
    query: {
      book_title: book.value.title || '',
      book_author: book.value.author || '',
      isbn13: book.value.isbn13 || isbn13.value || '',
      publisher: book.value.publisher || '',
      pub_date: book.value.pub_date || '',
      cover: book.value.cover || '',
    },
  })
}

/** ✅ 기본 정보 먼저 띄우고, AI는 뒤에서 따로 로딩 */
const loadPage = async (isbn) => {
  bookmarkStore.sync()

  await fetchBookDetail(isbn)
  // 기본 정보 성공했을 때만 AI 호출(원하면 실패해도 호출하도록 바꿔도 됨)
  if (book.value) fetchAiCuration(isbn)
}

onMounted(() => {
  loadPage(isbn13.value)
})

watch(
  () => isbn13.value,
  (newIsbn) => {
    if (!newIsbn) return
    loadPage(newIsbn)
  }
)
</script>

<style scoped>
.page {
  width: 100%;
  padding: 40px 32px 80px;
  box-sizing: border-box;
  background: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 45vh;
  gap: 16px;
  color: var(--text-secondary);
}

.top {
  width: 100%;
  display: grid;
  grid-template-columns: 1.5fr 0.5fr;
  gap: 40px;
  align-items: start;
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 40px;
  box-shadow: var(--shadow-sm);
  margin-bottom: 40px;
}

.left {
  min-width: 0;
}

.right {
  display: flex;
  justify-content: center;
}

.cover {
  width: 240px;
  height: auto;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  box-shadow: var(--shadow-md);
}

.category {
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 12px;
  word-break: keep-all;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 20px;
  line-height: 1.3;
  letter-spacing: -0.5px;
}

.meta {
  margin: 0 0 24px;
}

.meta p {
  margin: 10px 0;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
}

.meta strong {
  color: var(--text-primary);
  font-weight: 600;
  margin-right: 8px;
}

.desc {
  margin-top: 24px;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border-left: 4px solid var(--primary-color);
}

.desc h3 {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.desc p {
  margin: 0;
  line-height: 1.7;
  color: var(--text-secondary);
}

.btn-row {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
  border-radius: 10px;
  font-weight: 600;
  font-size: 15px;
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
}

.btn.subtle {
  border-color: var(--border-color);
  color: var(--text-secondary);
}

.stars {
  position: relative;
  display: inline-block;
  font-size: 18px;
  line-height: 1;
  vertical-align: middle;
  margin: 0 10px 0 0;
}

.stars-back {
  color: var(--border-color);
}

.stars-front {
  position: absolute;
  left: 0;
  top: 0;
  overflow: hidden;
  white-space: nowrap;
  color: #fbbf24;
}

.rating-num {
  font-size: 15px;
  color: var(--text-secondary);
  vertical-align: middle;
  font-weight: 600;
}

.ai-wrap {
  margin-top: 0;
}

.ai-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--primary-color);
}

.ai-head h2 {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.ai-state {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  font-weight: 500;
}

.ai-state.error {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.ai-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

.card {
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 24px;
  background: var(--bg-primary);
  box-shadow: var(--shadow-sm);
  transition: var(--transition);
}

.card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.card h3 {
  margin: 0 0 16px;
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
}

.ai-text {
  line-height: 1.8;
  margin: 0 0 16px;
  color: var(--text-secondary);
  font-size: 15px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  padding: 8px 12px;
  border-radius: 999px;
  background: var(--primary-lighter);
  border: 1px solid var(--primary-color);
  font-size: 13px;
  color: var(--primary-dark);
  font-weight: 500;
}

.chip.subtle {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-secondary);
}

.list {
  padding-left: 0;
  list-style: none;
  margin: 0;
}

.list li {
  margin: 12px 0;
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.6;
}

.bubbles {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bubble {
  padding: 16px;
  border-radius: 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  line-height: 1.6;
  color: var(--text-secondary);
  font-style: italic;
  font-size: 14px;
}

.author-row {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.author-img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--border-color);
  background: var(--bg-secondary);
  flex-shrink: 0;
  box-shadow: var(--shadow-md);
}

.author-body {
  min-width: 0;
  flex: 1;
}

.author-title {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.author-name {
  font-weight: 700;
  font-size: 18px;
  color: var(--text-primary);
}

.wiki-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  transition: var(--transition);
  padding: 4px 8px;
  border-radius: 6px;
}

.wiki-link:hover {
  background: var(--primary-lighter);
  text-decoration: underline;
}

.author-desc {
  margin: 0 0 12px;
  line-height: 1.8;
  white-space: pre-wrap;
  color: var(--text-secondary);
  font-size: 14px;
}

.works {
  margin-top: 12px;
}

.works-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.disclaimer {
  margin-top: 20px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 10px;
  font-size: 13px;
  color: var(--text-light);
  border-left: 3px solid var(--primary-color);
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner.small {
  width: 24px;
  height: 24px;
  border-width: 2px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .page {
    padding: 20px 16px 40px;
  }

  .top {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 24px;
  }

  .right {
    justify-content: center;
  }

  .cover {
    width: 200px;
  }

  .title {
    font-size: 24px;
  }

  .ai-grid {
    grid-template-columns: 1fr;
  }
}
</style>
