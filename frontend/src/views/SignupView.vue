<script setup>
import api from '@/api/axios'
import { ref } from 'vue'
import axios from 'axios'
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

// 회원가입 요청
const signup = () => {
  axios.post('/accounts/signup/', {
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
    alert('회원가입 성공!')
    router.push('/login')
  })
  .catch((error) => {
    console.error(error.response?.data)
    alert('회원가입 실패')
  })
}
</script>

<template>
  <div>
    <h1>회원가입</h1>

    <input v-model="username" placeholder="아이디" />
    <input v-model="email" placeholder="이메일" />
    <input v-model="password1" type="password" placeholder="비밀번호" />
    <input v-model="password2" type="password" placeholder="비밀번호 확인" />
    <input v-model="nickname" placeholder="닉네임" />

    <select v-model="favorite_country">
      <option :value="null">선호 국가 선택</option>
      <option value="KR">한국</option>
      <option value="JP">일본</option>
      <option value="CN">중화권</option>
      <option value="EN">영미권</option>
      <option value="OTHER">기타</option>
    </select>

    <input
      v-if="favorite_country === 'OTHER'"
      v-model="other_country"
      placeholder="기타 국가 입력"
    />

    <select v-model="favorite_genre">
      <option :value="null">선호 장르 선택</option>
      <option value="novel">소설</option>
      <option value="comic">만화</option>
      <option value="essay">에세이</option>
      <option value="issue">시사·이슈</option>
      <option value="etc">기타</option>
    </select>

    <button @click="signup">회원가입</button>
  </div>
</template>
