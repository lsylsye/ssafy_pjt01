<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { useBookmarkStore } from '@/stores/bookmark'

const auth = useAuthStore()
const bookmarkStore = useBookmarkStore()

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
    auth.setTokens({ access: res.data.access, refresh: res.data.refresh })
    bookmarkStore.sync()

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
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">로그인</h1>
      <p class="auth-subtitle">계정으로 로그인하세요</p>

      <input
        v-model="username"
        placeholder="아이디"
        class="auth-input"
      />

      <input
        v-model="password"
        type="password"
        placeholder="비밀번호"
        class="auth-input"
      />

      <button @click="login" class="auth-button">로그인</button>

      <div class="auth-footer">
        <p>계정이 없으신가요? <router-link to="/signup">회원가입</router-link></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
  background: linear-gradient(135deg, var(--primary-lighter) 0%, rgba(255, 255, 255, 0.8) 100%);
  padding: 20px;
}

.auth-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 48px 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: var(--shadow-lg);
  backdrop-filter: var(--blur-sm);
  border: 1px solid rgba(34, 197, 94, 0.1);
}

.auth-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px;
  text-align: center;
  letter-spacing: -0.5px;
}

.auth-subtitle {
  font-size: 15px;
  color: var(--text-secondary);
  margin: 0 0 32px;
  text-align: center;
  font-weight: 500;
}

.auth-input {
  width: 100%;
  padding: 14px 16px;
  margin-bottom: 16px;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-size: 15px;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: var(--text-primary);
  transition: var(--transition);
  background: var(--bg-secondary);
}

.auth-input:focus {
  outline: none;
  border-color: var(--primary-color);
  background: var(--bg-primary);
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.auth-button {
  width: 100%;
  padding: 14px 16px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  margin-top: 8px;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
}

.auth-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.auth-button:active {
  transform: translateY(0);
}

.auth-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: var(--text-secondary);
}

.auth-footer a {
  color: var(--primary-color);
  font-weight: 600;
  transition: var(--transition);
}

.auth-footer a:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}
</style>
