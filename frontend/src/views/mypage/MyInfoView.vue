<!-- src/views/mypage/MyInfoView.vue -->
<template>
  <section class="myinfo">
    <h2>내 정보</h2>

    <p v-if="my.loading">불러오는 중...</p>
    <p v-else-if="my.error">{{ my.error }}</p>

    <div v-else-if="my.me" class="card">
      <div class="row">
        <img :src="profileImageUrl" class="avatar" alt="profile" />

        <div class="info">
          <p>아이디: {{ my.me.username }}</p>
          <p>이메일: {{ my.me.email }}</p>
          <p>닉네임: {{ my.me.nickname }}</p>
          <p>선호 국가: {{ countryLabel(my.me.favorite_country) }}</p>
          <p>선호 장르: {{ genreLabel(my.me.favorite_genre) }}</p>

          <!-- ✅ 클릭 가능한 팔로워/팔로잉 -->
          <p class="follow-line">
            <button class="link" @click="goFollowers">
              팔로워 {{ my.me.followers_count ?? 0 }}
            </button>
            <span>·</span>
            <button class="link" @click="goFollowing">
              팔로잉 {{ my.me.following_count ?? 0 }}
            </button>
          </p>
        </div>
      </div>
    </div>

    <p v-else>정보가 없습니다.</p>
  </section>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import { useAuthStore } from "@/stores/auth";
import { useMyPageStore } from "@/stores/mypage";
import defaultProfile from "@/assets/default_profile.jpg";

const router = useRouter();
const auth = useAuthStore();
const my = useMyPageStore();

const countryMap = { KR: "한국", JP: "일본", CN: "중화권", EN: "영미권", OTHER: "기타" };
const genreMap = {
  novel_poem_drama: "소설/시/희곡",
  business: "경제/경영",
  self_help: "자기계발",
  humanities: "인문",
  hobby_practical: "취미/실용",
  comic_ebook: "만화/eBook",
  science: "과학",
};

const countryLabel = (code) => countryMap[code] || code || "-";
const genreLabel = (code) => genreMap[code] || code || "-";

const profileImageUrl = computed(() => {
  const p = my.me?.profile_image;

  if (!p) return defaultProfile;
  if (p.startsWith("http")) return p;

  const base = api.defaults.baseURL || "http://127.0.0.1:8000";
  return `${base}${p}`;
});

const goFollowers = () => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }
  router.push("/mypage/followers");
};

const goFollowing = () => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }
  router.push("/mypage/following");
};

onMounted(() => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }

  if (!my.me) {
    my.fetchMe().catch((err) => {
      if (err.response?.status === 401) router.push("/login");
    });
  }
});
</script>

<style scoped>
.myinfo { padding: 4px 0; }
.card { border: 1px solid #eee; border-radius: 12px; padding: 14px; }
.row { display: flex; gap: 16px; align-items: flex-start; }

.avatar {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #eee;
  background: #fafafa;
  flex: 0 0 auto;
}

.info p { margin: 8px 0; }

.follow-line { margin-top: 10px; color: #444; display:flex; gap:8px; align-items:center; }
.link {
  border: 0;
  background: transparent;
  padding: 0;
  cursor: pointer;
  color: #111;
  font-weight: 600;
}
.link:hover { text-decoration: underline; }
</style>
