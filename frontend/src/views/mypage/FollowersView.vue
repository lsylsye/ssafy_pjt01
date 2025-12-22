<!-- src/views/mypage/FollowersView.vue -->
<template>
  <section class="wrap">
    <h2 class="title">팔로워</h2>

    <p v-if="store.loadingFollowers" class="msg">불러오는 중...</p>
    <p v-else-if="store.errorFollowers" class="msg error">{{ store.errorFollowers }}</p>

    <ul v-else class="list">
      <li v-for="u in store.followers" :key="u.id" class="item" @click="goUser(u.id)">
        <img :src="imgUrl(u.profile_image)" class="avatar" alt="profile" />
        <span class="nick">{{ u.nickname }}</span>
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

onMounted(() => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }

  const loadFollowers = (myId) => {
    store.fetchFollowers(myId).catch(() => {});
  };

  if (!my.me?.id) {
    my.fetchMe()
      .then((me) => {
        if (me?.id) loadFollowers(me.id);
      })
      .catch(() => {});
  } else {
    loadFollowers(my.me.id);
  }
});
</script>

<style scoped>
.wrap { padding: 20px; max-width: 900px; }
.title { margin: 0 0 12px; font-size: 22px; font-weight: 900; }
.msg { color: #666; }
.msg.error { color: #d33; }

.list { list-style: none; padding: 0; margin: 0; border: 1px solid #eee; border-radius: 14px; overflow: hidden; }
.item { display:flex; gap:12px; align-items:center; padding: 12px 14px; cursor: pointer; }
.item + .item { border-top: 1px solid #eee; }
.item:hover { background: #fafafa; }

.avatar { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 1px solid #eee; }
.nick { font-weight: 700; color: #111; }
</style>
