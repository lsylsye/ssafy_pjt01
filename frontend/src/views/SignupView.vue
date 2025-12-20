<template>
  <div class="signup">
    <h1>회원가입</h1>

    <!-- 아이디 -->
    <input v-model="username" placeholder="아이디" />
    <p v-if="errors.username" class="error">
      {{ errors.username[0] }}
    </p>

    <!-- 이메일 -->
    <input v-model="email" placeholder="이메일" />
    <p v-if="errors.email" class="error">
      {{ errors.email[0] }}
    </p>

    <!-- 비밀번호 -->
    <input
      v-model="password1"
      type="password"
      placeholder="비밀번호"
    />

    <!-- 비밀번호 조건 안내 -->
    <p class="password-hint">
      비밀번호는 8자 이상이며,<br />
      영문과 숫자를 함께 사용해야 합니다.<br />
      너무 쉬운 비밀번호(예: 12341234)는 사용할 수 없습니다.
    </p>

    <p v-if="errors.password1" class="error">
      {{ errors.password1[0] }}
    </p>

    <!-- 비밀번호 확인 -->
    <input
      v-model="password2"
      type="password"
      placeholder="비밀번호 확인"
    />
    <p v-if="errors.password2" class="error">
      {{ errors.password2[0] }}
    </p>

    <!-- 닉네임 -->
    <input v-model="nickname" placeholder="닉네임" />
    <p v-if="errors.nickname" class="error">
      {{ errors.nickname[0] }}
    </p>

    <!-- 선호 국가 -->
    <select v-model="favorite_country">
      <option :value="null">선호 국가 선택</option>
      <option value="KR">한국</option>
      <option value="JP">일본</option>
      <option value="CN">중화권</option>
      <option value="EN">영미권</option>
      <option value="OTHER">기타</option>
    </select>

    <p v-if="errors.favorite_country" class="error">
      {{ errors.favorite_country[0] }}
    </p>

    <!-- 기타 국가 -->
    <input
      v-if="favorite_country === 'OTHER'"
      v-model="other_country"
      placeholder="기타 국가 입력"
    />
    <p v-if="errors.other_country" class="error">
      {{ errors.other_country[0] }}
    </p>

    <!-- 선호 장르 -->
    <select v-model="favorite_genre">
      <option :value="null">선호 장르 선택</option>
      <option value="novel_poem_drama">소설/시/희곡</option>
      <option value="business">경제/경영</option>
      <option value="self_help">자기계발</option>
      <option value="humanities">인문/교양</option>
      <option value="comic_ebook">만화/eBook</option>
      <option value="science">과학</option>
    </select>

    <p v-if="errors.favorite_genre" class="error">
      {{ errors.favorite_genre[0] }}
    </p>

    <!-- 필드 공통 에러 -->
    <p v-if="errors.non_field_errors" class="error">
      {{ errors.non_field_errors[0] }}
    </p>

    <button @click="signup">회원가입</button>
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
.signup {
  max-width: 360px;
  margin: 0 auto;
}

input,
select {
  width: 100%;
  padding: 8px;
  margin-top: 8px;
}

button {
  margin-top: 16px;
  padding: 10px;
  width: 100%;
}

.error {
  color: #e53935;
  font-size: 13px;
  margin: 4px 0;
}

.password-hint {
  font-size: 13px;
  color: #666;
  margin: 6px 0 8px;
  line-height: 1.4;
}
</style>
