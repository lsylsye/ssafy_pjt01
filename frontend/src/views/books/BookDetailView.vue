<template>
  <section class="book-detail">
    <p v-if="isLoading">불러오는 중...</p>
    <p v-else-if="errorMsg">{{ errorMsg }}</p>

    <div v-else-if="book">
      <h1 class="title">{{ book.title }}</h1>

      <div class="detail">
        <img :src="book.cover" alt="표지" class="cover" />

        <div class="info">
          <p><strong>저자</strong> {{ book.author }}</p>
          <p><strong>출판사</strong> {{ book.publisher }}</p>
          <p v-if="book.category_name">
            <strong>카테고리</strong> {{ book.category_name }}
          </p>

          <button
            class="bookmark-btn"
            :class="{ active: isBookmarked }"
            @click="handleBookmark"
          >
            {{ isBookmarked ? '북마크 해제' : '북마크 추가' }}
          </button>
        </div>
      </div>

      <div v-if="book.description" class="description">
        <h3>책 소개</h3>
        <p>{{ book.description }}</p>
      </div>
    </div>

    <p v-else>도서 정보를 찾을 수 없습니다.</p>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import { useBookmarkStore } from '@/stores/bookmark'

const route = useRoute()
const router = useRouter()
const bookmarkStore = useBookmarkStore()

const book = ref(null)
const isLoading = ref(false)
const errorMsg = ref('')

const isbn13 = computed(() => String(route.params.isbn13 || ''))
const isBookmarked = computed(() => bookmarkStore.isBookmarked(isbn13.value))

const isLoggedIn = () => !!localStorage.getItem('access_token')

const fetchBookDetail = (isbn) => {
  if (!isbn) return

  isLoading.value = true
  errorMsg.value = ''
  book.value = null

  api.get(`/api/books/${isbn}/`)
    .then((res) => {
      book.value = res.data
    })
    .catch((err) => {
      console.error('[도서 상세 조회 실패]', err.response?.data || err.message)
      errorMsg.value = '도서 정보를 불러오지 못했습니다.'
    })
    .finally(() => {
      isLoading.value = false
    })
}

const handleBookmark = () => {
  if (!isbn13.value) return

  if (!isLoggedIn()) {
    alert('로그인이 필요한 기능입니다.')
    router.push('/login')
    return
  }

  bookmarkStore.toggle(isbn13.value)
    .then(() => {
      // store가 상태 갱신까지 처리함
    })
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

const loadPage = (isbn) => {
  fetchBookDetail(isbn)
  bookmarkStore.sync()
}

onMounted(() => {
  loadPage(isbn13.value)
})

watch(
  () => isbn13.value,
  (newIsbn) => {
    loadPage(newIsbn)
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
