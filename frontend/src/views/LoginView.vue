<!-- src/views/LoginView.vue -->
<template>
  <div class="page">
    <div class="bg-blobs" aria-hidden="true">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <div class="login-card">

      <h1>로그인</h1>
      <!-- <p>오늘도 마음의 양식을 심어보세요.</p> -->

      <form @submit.prevent="onSubmit">
        <div v-if="auth.error" class="err-box">{{ auth.error }}</div>

        <div class="input-group">
          <label class="label" for="username">아이디</label>
          <input
            id="username"
            v-model.trim="form.username"
            type="text"
            class="input-field"
            placeholder="아이디를 입력해주세요"
            autocomplete="username"
          />
        </div>

        <div class="input-group">
          <label class="label" for="password">비밀번호</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="input-field"
            placeholder="비밀번호를 입력해주세요"
            autocomplete="current-password"
          />
        </div>

        <button class="btn-login" type="submit" :disabled="auth.loading || !canSubmit">
          <span v-if="auth.loading">로그인 중…</span>
          <span v-else>입장하기</span>
        </button>
      </form>

      <div class="footer-links">
        아직 정원사가 아니신가요?
        <button class="link" type="button" @click="$router.push('/signup')">회원가입</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth.store";

const router = useRouter();
const auth = useAuthStore();

const form = reactive({
  username: "",
  password: "",
});

const canSubmit = computed(() => {
  return form.username.trim().length >= 1 && form.password.length >= 1;
});

async function onSubmit() {
  if (!canSubmit.value) return;
  const ok = await auth.login({ username: form.username.trim(), password: form.password });
  if (ok) router.push("/");
}
</script>

<style scoped>
:root { --primary: #00D15B; --text: #191F28; }

.page{
  min-height: 100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  background:#F2F4F6;
  overflow:hidden;
  position:relative;
  padding: 24px 16px;
}

.bg-blobs{ position:absolute; inset:0; z-index:0; }
.blob{ position:absolute; border-radius:50%; filter: blur(60px); opacity:0.6; }
.blob-1{ width: 400px; height: 400px; background:#D1F7C4; top:-100px; left:-100px; animation: move 20s infinite alternate; }
.blob-2{ width: 300px; height: 300px; background:#E0F2FE; bottom:-50px; right:-50px; animation: move 15s infinite alternate-reverse; }
@keyframes move{ from{ transform: translate(0,0); } to{ transform: translate(50px,50px); } }

.login-card{
  width:100%;
  max-width:420px;
  background: rgba(255,255,255,0.75);
  backdrop-filter: blur(20px);
  border-radius: 30px;
  padding: 56px 40px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.05);
  border: 1px solid rgba(255,255,255,0.8);
  text-align:center;
  position:relative;
  z-index:1;
}

h1{ font-size: 1.8rem; margin: 0 0 10px; color: var(--text); font-weight: 800; line-height: 1.2; }
p{ color:#8B95A1; margin: 0 0 34px; font-size: 1rem; font-weight: 500; }

.err-box{
  background: rgba(255,64,64,0.10);
  border: 1px solid rgba(255,64,64,0.18);
  color:#c81e1e;
  padding: 12px 14px;
  border-radius: 14px;
  margin-bottom: 16px;
  font-weight: 600;
  text-align:left;
}

.input-group{ margin-bottom: 18px; text-align:left; }
.label{ font-size:0.9rem; font-weight: 600; color:#4E5968; margin-bottom: 8px; display:block; margin-left:4px; }

.input-field{
  width:100%;
  padding: 18px 20px;
  border-radius: 16px;
  border: 1px solid #E5E8EB;
  background: white;
  font-size: 1rem;
  outline: none;
  transition: 0.2s;
  box-sizing: border-box;
  font-weight: 500;
}
.input-field:focus{ border-color: var(--primary); box-shadow: 0 0 0 3px rgba(0,209,91,0.10); }
.input-field::placeholder{ color:#C0C5C9; }

.btn-login{
  width:100%;
  padding: 18px;
  border-radius: 16px;
  border:none;
  background: var(--primary);
  color:white;
  font-size: 1.05rem;
  font-weight: 800;
  cursor:pointer;
  margin-top: 18px;
  transition: 0.2s;
  box-shadow: 0 10px 20px rgba(0,209,91,0.20);
}
.btn-login:hover{ background:#00B54F; transform: translateY(-2px); }
.btn-login:disabled{ opacity:0.55; cursor:not-allowed; transform:none; }

.footer-links{ margin-top: 26px; font-size: 0.92rem; color:#8B95A1; font-weight: 500; }
.link{
  margin-left: 6px;
  color:#4E5968;
  font-weight: 600;
}
.link:hover{ color: var(--primary); text-decoration: underline; }

</style>
