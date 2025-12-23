<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">회원가입</h1>
      <p class="auth-subtitle">새로운 계정을 만드세요</p>

      <div class="form-group">
        <label>아이디</label>
        <input v-model="username" placeholder="아이디를 입력하세요" class="auth-input" />
        <p v-if="errors.username" class="error-message">{{ errors.username[0] }}</p>
      </div>

      <div class="form-group">
        <label>이메일</label>
        <input v-model="email" placeholder="이메일을 입력하세요" class="auth-input" />
        <p v-if="errors.email" class="error-message">{{ errors.email[0] }}</p>
      </div>

      <div class="form-group">
        <label>비밀번호</label>
        <input v-model="password1" type="password" placeholder="비밀번호를 입력하세요" class="auth-input" />
        <p class="password-hint">
          8자 이상, 영문과 숫자를 함께 사용해주세요
        </p>
        <p v-if="errors.password1" class="error-message">{{ errors.password1[0] }}</p>
      </div>

      <div class="form-group">
        <label>비밀번호 확인</label>
        <input v-model="password2" type="password" placeholder="비밀번호를 다시 입력하세요" class="auth-input" />
        <p v-if="errors.password2" class="error-message">{{ errors.password2[0] }}</p>
      </div>

      <div class="form-group">
        <label>닉네임</label>
        <input v-model="nickname" placeholder="닉네임을 입력하세요" class="auth-input" />
        <p v-if="errors.nickname" class="error-message">{{ errors.nickname[0] }}</p>
      </div>

      <div class="form-group">
        <label>선호 국가</label>
        <select v-model="favorite_country" class="auth-input">
          <option :value="null">선호 국가를 선택하세요</option>
          <option value="KR">한국</option>
          <option value="JP">일본</option>
          <option value="CN">중화권</option>
          <option value="EN">영미권</option>
          <option value="OTHER">기타</option>
        </select>
        <p v-if="errors.favorite_country" class="error-message">{{ errors.favorite_country[0] }}</p>
      </div>

      <div v-if="favorite_country === 'OTHER'" class="form-group">
        <label>국가명 입력</label>
        <input v-model="other_country" placeholder="국가명을 입력하세요" class="auth-input" />
        <p v-if="errors.other_country" class="error-message">{{ errors.other_country[0] }}</p>
      </div>

      <div class="form-group">
        <label>선호 장르</label>
        <select v-model="favorite_genre" class="auth-input">
          <option :value="null">선호 장르를 선택하세요</option>
          <option value="novel_poem_drama">소설/시/희곡</option>
          <option value="business">경제/경영</option>
          <option value="self_help">자기계발</option>
          <option value="humanities">인문/교양</option>
          <option value="comic_ebook">만화/eBook</option>
          <option value="science">과학</option>
        </select>
        <p v-if="errors.favorite_genre" class="error-message">{{ errors.favorite_genre[0] }}</p>
      </div>

      <p v-if="errors.non_field_errors" class="error-message">
        {{ errors.non_field_errors[0] }}
      </p>

      <button @click="signup" class="auth-button">회원가입</button>

      <div class="auth-footer">
        <p>이미 계정이 있으신가요? <router-link to="/login">로그인</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '@/api/axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 입력값
const username = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')
const nickname = ref('')
const favorite_country = ref(null)
const favorite_genre = ref(null)
const other_country = ref('')

// 백엔드 에러 메시지
const errors = ref({})

// 회원가입 요청
const signup = () => {
  errors.value = {}

  api.post('/accounts/signup/', {
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    favorite_country: favorite_country.value,
    favorite_genre: favorite_genre.value,
    other_country: other_country.value,
  })
  .then(() => {
    alert('회원가입 성공')
    router.push('/login')
  })
  .catch((error) => {
    console.error('[회원가입 실패]', error.response?.data)
    errors.value = error.response?.data || {
      non_field_errors: ['회원가입 중 오류가 발생했습니다.']
    }
  })
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
  background: linear-gradient(135deg, var(--primary-lighter) 0%, rgba(255, 255, 255, 0.8) 100%);
  padding: 40px 20px;
}

.auth-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 48px 40px;
  width: 100%;
  max-width: 500px;
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

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.auth-input {
  padding: 12px 14px;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-size: 14px;
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

.error-message {
  color: #ef4444;
  font-size: 13px;
  margin-top: 6px;
  font-weight: 500;
}

.password-hint {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 6px;
  font-weight: 400;
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
  margin-top: 16px;
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
