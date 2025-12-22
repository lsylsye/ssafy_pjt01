<template>
  <section class="wrap">
    <p v-if="store.loading" class="msg">불러오는 중...</p>
    <p v-else-if="store.error" class="msg error">{{ store.error }}</p>

    <div v-else-if="store.profile" class="card">
      <div class="top">
        <!-- ✅ 마이페이지랑 동일: 없으면 기본이미지, 깨지면 기본이미지 -->
        <img :src="profileImageUrl" class="avatar" alt="profile" @error="onImgError" />

        <div class="info">
          <div class="nickname">{{ store.profile.nickname }}</div>

          <div class="meta">
            <span>
              선호 국가:
              {{ COUNTRY_LABEL[store.profile.favorite_country] || store.profile.favorite_country || "-" }}
            </span>
            <span>·</span>
            <span>
              선호 장르:
              {{ GENRE_LABEL[store.profile.favorite_genre] || store.profile.favorite_genre || "-" }}
            </span>
          </div>

          <div class="counts">
            <span>팔로워 {{ store.profile.followers_count }}</span>
            <span>·</span>
            <span>팔로잉 {{ store.profile.following_count }}</span>
          </div>

          <div class="actions">
            <button
              class="btn"
              :class="{ danger: store.profile.is_following }"
              :disabled="store.toggling"
              @click="onToggleFollow"
            >
              {{ store.profile.is_following ? "언팔로우" : "팔로우" }}
            </button>

            <span v-if="store.toggleError" class="hint error">{{ store.toggleError }}</span>
          </div>
        </div>
      </div>
    </div>

    <p v-else class="msg">유저 정보가 없습니다.</p>
  </section>
</template>

<script setup>
import { computed, onMounted, watch, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/api/axios";
import { useAuthStore } from "@/stores/auth";
import { useUserProfileStore } from "@/stores/userProfile";

// ✅ 마이페이지에서 만든 기본 이미지 그대로 사용
import defaultProfile from "@/assets/default_profile.jpg";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const store = useUserProfileStore();

const userId = computed(() => String(route.params.userId || ""));

// ✅ 라벨 매핑 (너가 해둔거 유지)
const COUNTRY_LABEL = {
  KR: "한국",
  JP: "일본",
  CN: "중화권",
  EN: "영미권",
  OTHER: "기타",
};

const GENRE_LABEL = {
  novel_poem_drama: "소설/시/희곡",
  business: "경제/경영",
  self_help: "자기계발",
  humanities: "인문/교양",
  comic_ebook: "만화/eBook",
  science: "과학",
};

// ✅ 마이페이지 방식 그대로: baseURL + /media 처리 + 기본이미지
const imgOk = ref(true);

const profileImageUrl = computed(() => {
  if (!imgOk.value) return defaultProfile;

  const p = store.profile?.profile_image || "";
  if (!p) return defaultProfile;
  if (p.startsWith("http")) return p;

  // "/media/..." 형태면 baseURL 붙여서 표시
  const base = api.defaults.baseURL || "http://127.0.0.1:8000";
  const path = p.startsWith("/") ? p : `/${p}`; // ✅ 슬래시 보정(마이페이지에도 이거 있으면 더 안전)
  return `${base}${path}`;
});

const onImgError = () => {
  imgOk.value = false; // ✅ 깨지면 기본 이미지로 고정
};

const goLogin = () => {
  router.push({ path: "/login", query: { redirect: route.fullPath } });
};

const onToggleFollow = () => {
  if (!auth.isLoggedIn) {
    goLogin();
    return;
  }
  store.toggleFollow(userId.value);
};

const load = () => {
  if (!userId.value) return;
  imgOk.value = true; // ✅ 다른 유저로 이동 시 다시 시도
  store.fetchProfile(userId.value);
};

onMounted(load);

watch(
  () => userId.value,
  () => load()
);
</script>

<style scoped>
.wrap { padding: 20px; max-width: 900px; }
.msg { margin: 10px 0; color: #666; }
.msg.error { color: #d33; }

.card { border: 1px solid #eee; border-radius: 14px; padding: 16px; background: #fff; }
.top { display: flex; gap: 14px; align-items: flex-start; }

.avatar {
  width: 86px;
  height: 86px;
  object-fit: cover;
  border-radius: 50%;
  border: 1px solid #eee;
  background: #fafafa;
}

.info { flex: 1; min-width: 0; }
.nickname { font-size: 22px; font-weight: 900; color: #111; margin-bottom: 6px; }

.meta { color: #666; display: flex; gap: 8px; flex-wrap: wrap; }
.counts { margin-top: 8px; color: #444; display: flex; gap: 8px; flex-wrap: wrap; }

.actions { margin-top: 12px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }

.btn {
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 10px;
  padding: 8px 14px;
  cursor: pointer;
}
.btn:hover { border-color: #1a73e8; color: #1a73e8; }
.btn.danger { border-color: #f2b8b5; }
.btn.danger:hover { border-color: #d33; color: #d33; }

.hint { font-size: 13px; color: #666; }
.hint.error { color: #d33; }
</style>
