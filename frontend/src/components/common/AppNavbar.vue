<!-- src/components/common/AppNavbar.vue -->
<template>
  <header class="nav">
    <div class="inner">
      <!-- Left -->
      <div class="left">
        <RouterLink class="logo" :to="{ name: 'home' }">
          <span class="logo-text">잔디북</span>
        </RouterLink>

        <nav class="gnb">
          <RouterLink class="gnb-link" :to="{ name: 'taste' }">취향 분석</RouterLink>
          <RouterLink class="gnb-link" :to="{ name: 'community' }">커뮤니티</RouterLink>
          <RouterLink class="gnb-link" :to="{ name: 'travel' }">문학 여행</RouterLink>
          <RouterLink class="gnb-link" :to="{ name: 'mylibrary' }">내 서재</RouterLink>
        </nav>
      </div>

      <!-- Right -->
      <div class="right">
        <SearchCapsule />
        <RouterLink v-if="isLoggedIn" :to="{ name: 'review-write' }" class="record-btn">
          <PenLine :size="18" />
          기록 심기
        </RouterLink>

        <!-- 로그인 전 -->
        <template v-if="!isLoggedIn">
          <RouterLink class="ghost" :to="{ name: 'login' }">로그인</RouterLink>
          <RouterLink class="primary" :to="{ name: 'signup' }">회원가입</RouterLink>
        </template>

        <!-- 로그인 후 -->
        <template v-else>
          <!-- 드롭다운 외부클릭 감지를 위해 ref로 래핑 -->
          <div class="profile-wrap" ref="dropdownRef">
            <button
              class="avatar-btn"
              type="button"
              aria-label="profile"
              @click="toggleMenu"
            >
              <img class="avatar" :src="profileSrc" alt="profile" />
            </button>

            <div v-show="menuOpen" class="menu">
              <div class="menu-head">
                <div class="nick">{{ nickname }} 님</div>
                <div class="level-badge">Lv.{{ level }} {{ levelLabel }}</div>
              </div>

              <div class="divider"></div>

              <RouterLink class="menu-item" :to="{ name: 'mylibrary' }" @click="closeMenu">📚 내 서재</RouterLink>
              <RouterLink class="menu-item" :to="{ name: 'mypage' }" @click="closeMenu">⚙️ 마이페이지</RouterLink>

              <div class="divider"></div>

              <button class="menu-item danger" type="button" @click="logout">
                로그아웃
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth.store";      // ✅ Pinia auth 단일 소스
import { useMypageStore } from "@/stores/mypage.store";  // ✅ level/profile 단일 소스(/api/mypage/me/)
import SearchCapsule from "@/components/ui/SearchCapsule.vue";
import { PenLine } from "lucide-vue-next";

const router = useRouter();
const auth = useAuthStore();
const mypage = useMypageStore();

const menuOpen = ref(false);
const dropdownRef = ref(null);

const isLoggedIn = computed(() => !!auth.access); // ✅ localStorage 제거 (비동기 즉시 반영)
const nickname = computed(() => mypage.me?.nickname || auth.me?.nickname || "정원사"); // 닉네임은 mypage 우선
const level = computed(() => (typeof mypage.me?.level === "number" ? mypage.me.level : 1));

const levelLabel = computed(() => {
  if (mypage.me?.level_title) return mypage.me.level_title;

  const l = level.value;
  if (l <= 1) return "새싹";
  if (l === 2) return "줄기";
  if (l === 3) return "잎새";
  if (l === 4) return "나무";
  return "숲";
});

const profileSrc = computed(() => {
  const v = mypage.me?.profile_image;
  if (!v) return "https://via.placeholder.com/80";

  // 백엔드가 full url 주면 그대로
  if (String(v).startsWith("http")) return v;

  // 상대경로로 오는 경우만 보정 (png/jpg 강제변환 ❌)
  return `http://127.0.0.1:8000${String(v).startsWith("/") ? "" : "/"}${v}`;
});

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}
function closeMenu() {
  menuOpen.value = false;
}

/** 드롭다운 밖 클릭하면 닫기 (내부 클릭은 무시) */
function onDocumentMouseDown(e) {
  if (!menuOpen.value) return;
  const root = dropdownRef.value;
  if (!root) return;
  const target = e.target;
  if (root === target || root.contains(target)) return;
  closeMenu();
}

async function syncMypageMe() {
  // level/profile은 /api/mypage/me/가 단일 소스
  if (!isLoggedIn.value) return;
  if (!mypage.me) await mypage.fetchMe();
}

onMounted(async () => {
  await syncMypageMe();
  document.addEventListener("mousedown", onDocumentMouseDown);
});

onBeforeUnmount(() => {
  document.removeEventListener("mousedown", onDocumentMouseDown);
});

/** 로그인/로그아웃 즉시 반영 (새로고침 필요 없음) */
watch(
  isLoggedIn,
  async (v) => {
    if (v) {
      await mypage.fetchMe();
    } else {
      mypage.clear?.();
      closeMenu();
    }
  },
  { immediate: true }
);

function logout() {
  closeMenu();
  auth.logout();          // ✅ 토큰/유저 상태는 auth.store가 관리
  mypage.clear?.();       // ✅ mypage 상태 초기화
  router.push("/");
}
</script>

<style scoped>
.nav{
  position: sticky;
  top: 0;
  z-index: 100;
  height: 70px;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
}
.inner{
  max-width: 1100px;
  margin: 0 auto;
  height: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.left{
  display: flex;
  align-items: center;
  gap: 28px;
}
.logo{
  display: flex;
  align-items: center;
  gap: 10px;
}
.logo-text{
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.4px;
}
.gnb{
  display: flex;
  gap: 18px;
}
.gnb-link{
  font-size: 0.95rem;
  color: #6B7684;
  font-weight: 600;
  padding: 8px 0;
  transition: 0.15s;
}
.gnb-link:hover{ color: #191F28; }

.right{
  display: flex;
  align-items: center;
  gap: 12px;
}

.ghost{
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid rgba(0,0,0,0.08);
  background: rgba(255,255,255,0.9);
  font-weight: 600;
  color: #4E5968;
}
.primary{
  padding: 10px 14px;
  border-radius: 999px;
  background: #00D15B;
  color: #fff;
  font-weight: 600;
  border: 1px solid #00D15B;
}
.record-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #00D15B;
  color: #fff;
  padding: 10px 18px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.95rem;
  transition: 0.2s;
  box-shadow: 0 4px 12px rgba(0, 209, 91, 0.2);
}
.record-btn:hover {
  background: #00b54f;
  transform: translateY(-1px);
}

.profile-wrap{
  position: relative;
}
.avatar-btn{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  padding: 2px;
  border: 1px solid rgba(0,0,0,0.08);
  background: rgba(255,255,255,0.9);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: 0.15s;
}
.avatar-btn:hover{
  border-color: rgba(0, 209, 91, 0.6);
}
.avatar{
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.menu{
  position: absolute;
  top: 48px;
  right: 0;
  width: 180px;
  background: #fff;
  border-radius: 16px;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 18px 50px rgba(0,0,0,0.12);
  padding: 8px;
}
.menu-head{
  padding: 10px 10px 8px;
  border-radius: 12px;
  background: #F9FAFB;
  text-align: center;
}
.nick{
  font-weight: 600;
  color: #191F28;
}
.level-badge{
  margin-top: 6px;
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #fff;
  background: #00D15B;
  padding: 2px 8px;
  border-radius: 999px;
}
.divider{
  height: 1px;
  background: rgba(0,0,0,0.06);
  margin: 6px 0;
}
.menu-item{
  width: 100%;
  display: block;
  padding: 10px 10px;
  border-radius: 12px;
  font-weight: 600;
  color: #4E5968;
  text-align: left;
}
.menu-item:hover{
  background: #F2F4F6;
  color: #191F28;
}
.danger{
  color: #FF4040;
}
.danger:hover{
  background: rgba(255,64,64,0.10);
}
</style>
