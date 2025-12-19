<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()

const username = ref('')
const password = ref('')

const login = () => {
  api.post('/accounts/login/', {
    username: username.value,
    password: password.value,
  })
  .then((res) => {
    // ✅ JWT 토큰 저장
    const access = res.data.access
    const refresh = res.data.refresh

    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)

    alert('로그인 성공')
    router.push('/')   // 메인 페이지 이동
  })
  .catch((error) => {
    console.error(error.response?.data)
    alert('아이디 또는 비밀번호가 올바르지 않습니다.')
  })
}
</script>

<template>
  <div>
    <h1>로그인</h1>

    <input
      v-model="username"
      placeholder="아이디"
    />

    <input
      v-model="password"
      type="password"
      placeholder="비밀번호"
    />

    <button @click="login">로그인</button>
  </div>
</template>
