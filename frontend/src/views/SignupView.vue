<!-- src/views/SignupView.vue -->
<template>
  <div class="page">
    <div class="bg-blobs" aria-hidden="true">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <div class="signup-card">
      <h2>환영합니다 🌱</h2>
      <p class="sub-desc">나만의 독서 숲을 가꾸기 위한 첫 걸음입니다.</p>

      <form @submit.prevent="onSubmit">
        <div v-if="auth.error" class="err-box">{{ auth.error }}</div>

        <!-- 섹션 1: 계정 정보 -->
        <div class="form-section">
          <div class="section-title">계정 정보</div>

          <div class="input-group">
            <label class="label" for="username">아이디</label>
            <input id="username" v-model.trim="form.username" class="input-field" type="text" placeholder="영문, 숫자 포함 6자 이상" autocomplete="username" />
          </div>

          <div class="input-group">
            <label class="label" for="email">이메일</label>
            <input id="email" v-model.trim="form.email" class="input-field" type="email" placeholder="example@jandibook.com" autocomplete="email" />
          </div>

          <div class="input-group">
            <label class="label" for="pw1">비밀번호</label>
            <input id="pw1" v-model="form.password1" class="input-field" type="password" placeholder="비밀번호를 입력해주세요" autocomplete="new-password" />
          </div>

          <div class="input-group">
            <label class="label" for="pw2">비밀번호 확인</label>
            <input id="pw2" v-model="form.password2" class="input-field" type="password" placeholder="비밀번호를 한 번 더 입력해주세요" autocomplete="new-password" />
          </div>
        </div>

        <!-- 섹션 2: 프로필 & 취향 -->
        <div class="form-section">
          <div class="section-title">나의 취향</div>

          <div class="input-group">
            <label class="label" for="nickname">닉네임</label>
            <input id="nickname" v-model.trim="form.nickname" class="input-field" type="text" placeholder="잔디북에서 사용할 이름" />
          </div>

          <div class="input-group">
            <label class="label" for="country">좋아하는 나라 (문학)</label>
            <div class="select-wrapper">
              <select id="country" v-model="form.favorite_country" class="input-field">
                <option value="" disabled>나라를 선택해주세요</option>
                <option value="KR">🇰🇷 대한민국</option>
                <option value="JP">🇯🇵 일본</option>
                <option value="CN">🇨🇳 중화권</option>
                <option value="EN">🇺🇸 영미권</option>
                <option value="OTHER">🌍 기타</option>
              </select>
            </div>
          </div>

          <div v-if="form.favorite_country === 'OTHER'" class="input-group">
            <label class="label" for="otherCountry">기타 나라(직접 입력)</label>
            <input id="otherCountry" v-model.trim="form.other_country" class="input-field" type="text" placeholder="예) 스페인, 러시아, 브라질…" />
          </div>

          <div class="input-group">
            <label class="label" for="genre">가장 선호하는 장르</label>
            <div class="select-wrapper">
              <select id="genre" v-model="form.favorite_genre" class="input-field">
                <option value="" disabled>장르를 선택해주세요</option>
                <option value="novel_poem_drama">📖 소설/시/희곡</option>
                <option value="business">💰 경제/경영</option>
                <option value="self_help">🔥 자기계발</option>
                <option value="humanities">🧠 인문/철학</option>
                <option value="hobby_practical">🧩 취미/실용</option>
                <option value="comic_ebook">🧿 만화/eBook</option>
                <option value="science">🔭 과학</option>
              </select>
            </div>
          </div>
        </div>

        <button class="btn-submit" type="submit" :disabled="auth.loading || !canSubmit">
          <span v-if="auth.loading">가입 중…</span>
          <span v-else>가입 완료하기</span>
        </button>
      </form>

      <div class="login-link">
        이미 계정이 있으신가요?
        <button class="link" type="button" @click="$router.push('/login')">로그인</button>
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
  email: "",
  password1: "",
  password2: "",
  nickname: "",
  favorite_country: "",
  other_country: "",
  favorite_genre: "",
});

const canSubmit = computed(() => {
  if (!form.username.trim()) return false;
  if (!form.email.trim()) return false;
  if (!form.password1 || !form.password2) return false;
  if (form.password1 !== form.password2) return false;
  if (!form.nickname.trim()) return false;
  if (!form.favorite_country) return false;
  if (form.favorite_country === "OTHER" && !form.other_country.trim()) return false;
  if (!form.favorite_genre) return false;
  return true;
});

async function onSubmit() {
  if (!canSubmit.value) return;

  const payload = {
    username: form.username.trim(),
    email: form.email.trim(),
    password1: form.password1,
    password2: form.password2,
    nickname: form.nickname.trim(),
    favorite_country: form.favorite_country,
    favorite_genre: form.favorite_genre,
  };

  if (form.favorite_country === "OTHER") payload.other_country = form.other_country.trim();

  const ok = await auth.signup(payload);

  // 회원가입 직후 토큰이 안 오면 로그인 페이지로 보내도 됨
  if (ok) {
    if (auth.access) router.push("/");
    else router.push("/login");
  }
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
  position:relative;
  padding: 40px 16px;
}

.bg-blobs{ position: fixed; inset:0; z-index:-1; }
.blob{ position:absolute; border-radius:50%; filter: blur(80px); opacity:0.5; }
.blob-1{ width: 500px; height: 500px; background:#D1F7C4; top:-100px; left:-200px; }
.blob-2{ width: 400px; height: 400px; background:#E0F2FE; bottom:-50px; right:-100px; }

.signup-card{
  width:100%;
  max-width: 520px;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(20px);
  border-radius: 30px;
  padding: 50px 40px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.05);
  border: 1px solid rgba(255,255,255,1);
}

h2{ font-size: 1.8rem; font-weight: 800; margin:0 0 10px; color: var(--text); }
.sub-desc{ color:#8B95A1; margin-bottom: 34px; font-size: 1rem; font-weight: 500; }

.err-box{
  background: rgba(255,64,64,0.10);
  border: 1px solid rgba(255,64,64,0.18);
  color:#c81e1e;
  padding: 12px 14px;
  border-radius: 14px;
  margin-bottom: 16px;
  font-weight: 600;
}

.form-section{ margin-bottom: 26px; }
.section-title{
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 14px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.input-group{ margin-bottom: 18px; }
.label{ display:block; font-size:0.9rem; font-weight: 600; color:#333; margin-bottom: 8px; margin-left: 4px; }

.input-field{
  width:100%;
  padding: 16px;
  border-radius: 14px;
  border: 1px solid #E5E8EB;
  background: white;
  font-size: 1rem;
  outline: none;
  transition: 0.2s;
  box-sizing: border-box;
  font-family: inherit;
  color: var(--text);
  font-weight: 500;
}
.input-field:focus{ border-color: var(--primary); box-shadow: 0 0 0 3px rgba(0,209,91,0.10); }

.select-wrapper{ position: relative; }
.select-wrapper::after{
  content:"▼";
  position:absolute;
  right: 18px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.8rem;
  color: #888;
  pointer-events:none;
}
select.input-field{ appearance:none; cursor:pointer; }

.btn-submit{
  width:100%;
  padding: 18px;
  border-radius: 16px;
  border:none;
  background: var(--primary);
  color:white;
  font-size: 1.05rem;
  font-weight: 800;
  cursor:pointer;
  margin-top: 6px;
  transition: 0.2s;
  box-shadow: 0 10px 20px rgba(0,209,91,0.20);
}
.btn-submit:hover{ background:#00B54F; transform: translateY(-2px); }
.btn-submit:disabled{ opacity:0.55; cursor:not-allowed; transform:none; }

.login-link{
  text-align:center;
  margin-top: 22px;
  font-size: 0.92rem;
  color:#8B95A1;
  font-weight: 500;
}
.link{
  margin-left: 6px;
  color:#333;
  font-weight: 600;
}
.link:hover{ text-decoration: underline; color: var(--primary); }
</style>
