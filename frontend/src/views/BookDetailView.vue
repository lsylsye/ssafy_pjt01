<template>
  <section class="book-detail">
    <!-- 로딩 -->
    <p v-if="isLoading">불러오는 중...</p>

    <!-- 에러 -->
    <p v-else-if="errorMsg">{{ errorMsg }}</p>

    <!-- 도서 상세 -->
    <div v-else-if="book">
      <h1 class="title">{{ book.title }}</h1>

      <div class="detail">
        <!-- 표지 -->
        <img :src="book.cover" alt="표지" class="cover" />

        <!-- 정보 -->
        <div class="info">
          <p><strong>저자</strong> {{ book.author }}</p>
          <p><strong>출판사</strong> {{ book.publisher }}</p>
          <p v-if="book.category_name">
            <strong>카테고리</strong> {{ book.category_name }}
          </p>

          <!-- ⭐ 북마크 버튼 -->
          <button
            class="bookmark-btn"
            :class="{ active: isBookmarked }"
            @click="handleBookmark"
          >
            {{ isBookmarked ? '북마크 해제' : '북마크 추가' }}
          </button>
        </div>
      </div>

      <!-- 📖 설명 -->
      <div v-if="book.description" class="description">
        <h3>책 소개</h3>
        <p>{{ book.description }}</p>
      </div>
    </div>

    <!-- 데이터 없음 -->
    <p v-else>도서 정보를 찾을 수 없습니다.</p>
  </section>
</template>


<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()

const book = ref(null)
const isLoading = ref(false)
const errorMsg = ref('')
const isBookmarked = ref(false)

/* ===============================
   로그인 여부 판단
================================ */
const isLoggedIn = () => {
  const token = localStorage.getItem('access_token')
  console.log('[북마크] access_token:', token)
  return !!token
}

/* ===============================
   도서 상세 조회
================================ */
const fetchBookDetail = (isbn13) => {
  if (!isbn13) return

  console.log('[도서 상세 요청]', isbn13)

  isLoading.value = true
  errorMsg.value = ''
  book.value = null

  api.get(`/api/books/${isbn13}/`)
    .then((res) => {
      book.value = res.data
      console.log('[도서 상세 응답]', res.data)
    })
    .catch((err) => {
      console.error('[도서 상세 조회 실패]', err)
      errorMsg.value = '도서 정보를 불러오지 못했습니다.'
    })
    .finally(() => {
      isLoading.value = false
    })
}

/* ===============================
   북마크 클릭 처리
================================ */
const handleBookmark = () => {
  console.log('--- 북마크 버튼 클릭 ---')

  // 로그인 안 됐을 때
  if (!isLoggedIn()) {
    console.warn('[북마크 실패] 로그인 필요')
    alert('로그인이 필요한 기능입니다.')
    router.push('/login')
    return
  }

  // 로그인 된 경우 (지금은 UI 토글만)
  isBookmarked.value = !isBookmarked.value

  console.log('[북마크 토글]')
  console.log('책 제목:', book.value?.title)
  console.log('ISBN:', route.params.isbn13)
  console.log('현재 북마크 상태:', isBookmarked.value)
}

/* ===============================
   생명주기
================================ */
onMounted(() => {
  console.log('[BookDetailView mounted]')
  fetchBookDetail(route.params.isbn13)
})

watch(
  () => route.params.isbn13,
  (newIsbn) => {
    console.log('[도서 변경 감지]', newIsbn)
    isBookmarked.value = false
    fetchBookDetail(newIsbn)
  }
)
</script>


<style scoped>
.book-detail {
  padding: 24px;
}

.title {
  margin-bottom: 16px;
}

.detail {
  display: flex;
  gap: 24px;
}

.cover {
  width: 180px;
  height: auto;
}

.info p {
  margin-bottom: 6px;
}

.bookmark-btn {
  margin-top: 12px;
  padding: 6px 14px;
  border: 1px solid #aaa;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.bookmark-btn.active {
  background: #1a73e8;
  color: white;
  border-color: #1a73e8;
}

.description {
  margin-top: 32px;
  line-height: 1.6;
}

.description h3 {
  margin-bottom: 8px;
}
</style>
