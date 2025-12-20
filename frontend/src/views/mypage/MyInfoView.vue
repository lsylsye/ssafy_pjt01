<template>
  <section class="myinfo">
    <h2>내 정보</h2>

    <p v-if="loading">불러오는 중...</p>
    <p v-else-if="errorMsg">{{ errorMsg }}</p>

    <div v-else-if="me" class="card">
      <p>아이디: {{ me.username }}</p>
      <p>이메일: {{ me.email }}</p>
      <p>닉네임: {{ me.nickname }}</p>
      <p>선호 국가: {{ countryLabel(me.favorite_country) }}</p>
      <p>선호 장르: {{ genreLabel(me.favorite_genre) }}</p>

      <!-- 나중에 수정 UI 들어갈 자리(편집모드) -->
      <!--
      <label>
        닉네임
        <input v-model="form.nickname" />
      </label>

      <label>
        선호 국가
        <select v-model="form.favorite_country">
          <option v-for="c in countryOptions" :key="c.value" :value="c.value">
            {{ c.label }}
          </option>
        </select>
      </label>

      <label>
        선호 장르
        <select v-model="form.favorite_genre">
          <option v-for="g in genreOptions" :key="g.value" :value="g.value">
            {{ g.label }}
          </option>
        </select>
      </label>
      -->
    </div>

    <p v-else>정보가 없습니다.</p>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const errorMsg = ref('')
const me = ref(null)

/* ===============================
   코드 -> 한글 라벨 매핑
================================ */
const countryMap = {
  KR: '한국',
  JP: '일본',
  CN: '중화권',
  EN: '영미권',
  OTHER: '기타',
}

const genreMap = {
  novel_poem_drama: '소설/시/희곡',
  business: '경제/경영',
  self_help: '자기계발',
  humanities: '인문',
  hobby_practical: '취미/실용',
  comic_ebook: '만화/eBook',
  science: '과학',
}

const countryLabel = (code) => countryMap[code] || code || '-'
const genreLabel = (code) => genreMap[code] || code || '-'

/* ===============================
   내 정보 조회
================================ */
const fetchMe = () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  loading.value = true
  errorMsg.value = ''
  me.value = null

  api.get('/api/mypage/me/', {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((res) => {
      me.value = res.data
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[내 정보 조회 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout()
        router.push('/login')
        return
      }

      errorMsg.value = '내 정보를 불러오지 못했습니다.'
    })
    .finally(() => {
      loading.value = false
    })
}

onMounted(() => {
  fetchMe()
})
</script>

<style scoped>
.myinfo {
  padding: 4px 0;
}

.card {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 14px;
}
</style>
