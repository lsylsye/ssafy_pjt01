<template>
  <section class="bookmarks">
    <h2>북마크</h2>

    <p v-if="loading">불러오는 중...</p>
    <p v-else-if="errorMsg">{{ errorMsg }}</p>

    <div v-else>
      <p v-if="items.length === 0">북마크가 없습니다.</p>

      <ul v-else class="list">
        <li v-for="b in items" :key="b.isbn13" class="item">
          <router-link :to="`/books/${b.isbn13}`" class="left">
            <img :src="b.cover" alt="표지" class="cover" />
            <div class="meta">
              <p class="title">{{ b.title }}</p>
              <p class="sub">{{ b.author }}</p>
              <p class="sub">{{ b.publisher }}</p>
            </div>
          </router-link>

          <button class="btn" @click="toggleOff(b.isbn13)">해제</button>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { useBookmarkStore } from '@/stores/bookmark'

const router = useRouter()
const auth = useAuthStore()
const bookmarkStore = useBookmarkStore()

const loading = ref(false)
const errorMsg = ref('')
const items = ref([])

const fetchBookmarks = () => {
  if (!auth.isLoggedIn) {
    router.push('/login')
    return
  }

  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  loading.value = true
  errorMsg.value = ''
  items.value = []

  api.get('/api/mypage/bookmarks/', {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((res) => {
      // ✅ 명세 그대로 배열 응답
      items.value = Array.isArray(res.data) ? res.data : []
      // ✅ 다른 화면과 별표 일치시키기
      bookmarkStore.sync()
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[북마크 목록 조회 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout()
        router.push('/login')
        return
      }

      errorMsg.value = '북마크 목록을 불러오지 못했습니다.'
    })
    .finally(() => {
      loading.value = false
    })
}

const toggleOff = (isbn13) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  api.post(
    `/api/books/${isbn13}/bookmark/`,
    {},
    { headers: { Authorization: `Bearer ${token}` } }
  )
    .then((res) => {
      // res: { bookmarked: false, created: false }가 와야 정상
      const on = !!res.data.bookmarked

      // ✅ store 동기화(별표 상태)
      if (on) bookmarkStore.isbnSet.add(String(isbn13))
      else bookmarkStore.isbnSet.delete(String(isbn13))

      // ✅ “해제” 버튼이니까 꺼졌을 때만 목록에서 제거
      if (!on) {
        items.value = items.value.filter((x) => String(x.isbn13) !== String(isbn13))
      }
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[북마크 토글 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout()
        router.push('/login')
        return
      }

      alert('북마크 해제에 실패했습니다.')
    })
}

onMounted(() => {
  fetchBookmarks()
})
</script>

<style scoped>
.bookmarks {
  padding: 4px 0;
}

.list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.item {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 12px;
  flex: 1;
  min-width: 140px;
  max-width: 180px;
}

.left {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  text-decoration: none;
  color: inherit;
  flex: 1;
  min-width: 0;
  width: 100%;
  text-align: center;
  width: 100%;
}

.cover {
  width: 54px;
  height: auto;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.meta {
  min-width: 0;
}

.title {
  margin: 0;
  font-weight: 700;
  font-size: 13px;
  line-height: 1.3;
  word-break: break-word;
}

.sub {
  margin: 2px 0 0;
  color: #666;
  font-size: 14px;
}

.btn {
  border: 1px solid #ddd;
  background: white;
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
  margin-left: 0;
  margin-top: 8px;
  flex-shrink: 0;
  width: 100%;
  font-size: 12px;
}

.btn:hover {
  border-color: #1a73e8;
  color: #1a73e8;
}
</style>
