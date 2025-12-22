<!-- src/views/mypage/FollowingView.vue -->
<template>
  <section class="wrap">
    <h2 class="title">팔로잉</h2>

    <p v-if="store.loadingFollowing" class="msg">불러오는 중...</p>
    <p v-else-if="store.errorFollowing" class="msg error">{{ store.errorFollowing }}</p>

    <ul v-else class="list">
      <li v-for="u in store.following" :key="u.id" class="item">
        <div class="left" @click="goUser(u.id)">
          <img :src="imgUrl(u.profile_image)" class="avatar" alt="profile" />
          <span class="nick">{{ u.nickname }}</span>
        </div>

        <button
          class="btn danger"
          :disabled="store.togglingId === u.id"
          @click="onUnfollow(u.id)"
        >
          {{ store.togglingId === u.id ? "처리 중..." : "언팔로우" }}
        </button>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import defaultProfile from "@/assets/default_profile.jpg";
import { useAuthStore } from "@/stores/auth";
import { useMyPageStore } from "@/stores/mypage";
import { useFollowListStore } from "@/stores/followList";

const router = useRouter();
const auth = useAuthStore();
const my = useMyPageStore();
const store = useFollowListStore();

const imgUrl = (p) => {
  if (!p) return defaultProfile;
  if (p.startsWith("http")) return p;
  const base = api.defaults.baseURL || "http://127.0.0.1:8000";
  return `${base}${p}`;
};

const goUser = (id) => router.push(`/users/${id}`);

const onUnfollow = (targetId) => {
  if (!confirm("팔로우를 취소할까요?")) return;
  const myId = my.me?.id;
  store.unfollow(targetId, myId).catch(() => alert("언팔로우에 실패했습니다."));
};

onMounted(() => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }

  const loadFollowing = (myId) => {
    store.fetchFollowing(myId).catch(() => {});
  };

  if (!my.me?.id) {
    my.fetchMe()
      .then((me) => {
        if (me?.id) loadFollowing(me.id);
      })
      .catch(() => {});
  } else {
    loadFollowing(my.me.id);
  }
});
</script>

<style scoped>
.wrap { padding: 20px; max-width: 900px; }
.title { margin: 0 0 12px; font-size: 22px; font-weight: 900; }
.msg { color: #666; }
.msg.error { color: #d33; }

.list { list-style: none; padding: 0; margin: 0; border: 1px solid #eee; border-radius: 14px; overflow: hidden; }

.item { display:flex; align-items:center; justify-content:space-between; padding: 12px 14px; }
.item + .item { border-top: 1px solid #eee; }

.left { display:flex; gap:12px; align-items:center; cursor:pointer; }
.left:hover { text-decoration: underline; }

.avatar { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 1px solid #eee; }
.nick { font-weight: 700; color: #111; }

.btn {
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 10px;
  padding: 8px 12px;
  cursor: pointer;
}
.btn.danger { border-color: #f2b8b5; }
.btn.danger:hover { border-color: #d33; color: #d33; }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
