<template>
  <section>
    <h2>자유게시판 글쓰기</h2>

    <p v-if="loading">처리 중...</p>
    <p v-else-if="errorMsg" class="error">{{ errorMsg }}</p>

    <div class="form">
      <!-- ✅ 말머리 직접 입력 -->
      <input v-model="prefixName" class="input" placeholder="말머리(예: 잡담, 경제) - 선택" />

      <input v-model="title" class="input" placeholder="제목" />
      <textarea v-model="content" class="textarea" placeholder="내용"></textarea>

      <button class="btn" @click="submit">등록</button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const country = computed(() => String(route.params.country || 'kr'))
const apiCountry = (c) => String(c || 'kr').toUpperCase()

const loading = ref(false)
const errorMsg = ref('')

const prefixName = ref('') // ✅ 직접 입력
const title = ref('')
const content = ref('')

const submit = () => {
  if (!auth.isLoggedIn) {
    router.push('/login')
    return
  }

  const t = title.value.trim()
  const ctt = content.value.trim()
  if (!t || !ctt) {
    alert('제목/내용은 필수입니다.')
    return
  }

  const token = localStorage.getItem('access_token')
  const c = apiCountry(country.value)

  loading.value = true
  errorMsg.value = ''

  api.post(
    `/api/community/${c}/free/write`,
    {
      title: t,
      content: ctt,
      prefix_name: prefixName.value.trim() || null,
    },
    { headers: { Authorization: `Bearer ${token}` } }
  )
    .then((res) => {
      const id = res.data?.id
      if (id) router.push(`/community/${country.value}/free/${id}`)
      else router.push(`/community/${country.value}/free`)
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[글 작성 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout()
        router.push('/login')
        return
      }
      errorMsg.value = '글 작성에 실패했습니다.'
    })
    .finally(() => {
      loading.value = false
    })
}
</script>

<style scoped>
.error { color: #d33; }
.form { display: flex; flex-direction: column; gap: 10px; max-width: 680px; }
.input, .textarea {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 10px 12px;
}
.textarea { min-height: 180px; resize: vertical; }
.btn {
  width: 120px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 10px;
  padding: 10px 12px;
  cursor: pointer;
}
.btn:hover { border-color: #1a73e8; color: #1a73e8; }
</style>
