<template>
  <section>
    <div class="filters">
      <input v-model="q" class="input" placeholder="검색(제목+내용)" />
      <input v-model="prefix" class="input" placeholder="말머리(예: 잡담) - 선택" />
      <button class="btn" @click="fetchList">검색</button>
    </div>

    <p v-if="loading">불러오는 중...</p>
    <p v-else-if="errorMsg" class="error">{{ errorMsg }}</p>

    <div v-else>
      <p v-if="posts.length === 0">게시글이 없습니다.</p>

      <ul v-else class="list">
        <li v-for="p in posts" :key="p.id" class="item">
          <router-link :to="`/community/${country}/free/${p.id}`" class="link">
            <div class="row">
              <span v-if="p.prefix_name" class="prefix">[{{ p.prefix_name }}]</span>
              <span class="title">{{ p.title }}</span>
            </div>

            <div class="meta">
              <span>{{ p.user_nickname }}</span>
              <span>· {{ formatDate(p.created_at) }}</span>
              <span>· 좋아요 {{ p.like_count }}</span>
              <span>· 댓글 {{ p.comment_count }}</span>
            </div>

            <p class="content">{{ p.content }}</p>
          </router-link>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const country = computed(() => String(route.params.country || 'kr'))
const apiCountry = (c) => String(c || 'kr').toLowerCase()

const loading = ref(false)
const errorMsg = ref('')
const posts = ref([])

const q = ref('')
const prefix = ref('') // query key: prefix, value: prefix_name (예: "잡담")

const formatDate = (iso) => (typeof iso === 'string' ? iso.slice(0, 10) : '')

const fetchList = () => {
  loading.value = true
  errorMsg.value = ''
  posts.value = []

  const c = apiCountry(country.value)

  api.get(`/api/community/${c}/free/`, {   // ✅ trailing slash
    params: {
      q: q.value.trim() || undefined,
      prefix: prefix.value.trim() || undefined,
    },
  })
    .then((res) => {
      posts.value = Array.isArray(res.data) ? res.data : []
    })
    .catch((err) => {
      console.error('[자유 목록 실패]', err.response?.status, err.response?.data || err.message)
      errorMsg.value = '게시글을 불러오지 못했습니다.'
    })
    .finally(() => {
      loading.value = false
    })
}

onMounted(() => {
  fetchList()
})

watch(
  () => country.value,
  () => {
    q.value = ''
    prefix.value = ''
    fetchList()
  }
)
</script>

<style scoped>
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
  align-items: center;
}
.input {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.btn {
  border: 1px solid #ddd;
  background: white;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}
.btn:hover { border-color: #1a73e8; color: #1a73e8; }

.error { color: #d33; }

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 12px 14px;
}

.link { text-decoration: none; color: inherit; display: block; }

.row { display: flex; gap: 8px; align-items: center; margin-bottom: 6px; }
.prefix { color: #1a73e8; font-weight: 700; }
.title { font-weight: 800; }

.meta { color: #666; font-size: 14px; display: flex; gap: 8px; margin-bottom: 8px; }
.content { margin: 0; color: #333; }
</style>
