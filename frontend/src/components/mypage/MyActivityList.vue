<template>
  <section class="my-activity">

    <div class="tabs">
      <button :class="{ on: tab === 'posts' }" @click="tab = 'posts'">내 게시글</button>
      <button :class="{ on: tab === 'comments' }" @click="tab = 'comments'">내 댓글</button>
    </div>

    <!-- 게시글 -->
    <div v-if="tab === 'posts'">
      <p v-if="loadingPosts" class="msg">불러오는 중...</p>
      <p v-else-if="errorPosts" class="msg error">{{ errorPosts }}</p>
      <p v-else-if="posts.length === 0" class="msg">작성한 게시글이 없습니다.</p>

      <ul v-else class="list">
        <li v-for="p in posts" :key="p.detail_url" class="item" @click="goPost(p)">
          <div class="row1">
            <span class="badge">{{ p.type_name }}</span>
            <span class="date">{{ fmt(p.created_at) }}</span>
          </div>
          <div class="row2">{{ p.title }}</div>
        </li>
      </ul>
    </div>

    <!-- 댓글 -->
    <div v-else>
      <p v-if="loadingComments" class="msg">불러오는 중...</p>
      <p v-else-if="errorComments" class="msg error">{{ errorComments }}</p>
      <p v-else-if="comments.length === 0" class="msg">작성한 댓글이 없습니다.</p>

      <ul v-else class="list">
        <li v-for="c in comments" :key="c.comment_id" class="item" @click="goComment(c)">
          <div class="row1">
            <span class="badge">{{ c.type }}</span>
            <span class="date">{{ fmt(c.created_at) }}</span>
          </div>
          <div class="row2">{{ c.post_title }}</div>
          <div class="row3">“{{ c.content }}”</div>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getMyPosts, getMyComments } from "@/api/mypage";

const router = useRouter();

const tab = ref("posts");

const posts = ref([]);
const comments = ref([]);

const loadingPosts = ref(false);
const loadingComments = ref(false);

const errorPosts = ref("");
const errorComments = ref("");

const fmt = (iso) => {
  if (!iso) return "-";
  return String(iso).replace("T", " ").slice(0, 16);
};

const trimSlash = (s) => String(s || "").replace(/\/+$/, "");

const toFrontPathFromPost = (p) => {
  const url = trimSlash(p?.detail_url || "");
  // 1) "/api/community/kr/free/3" -> "/community/kr/free/3"
  if (url.startsWith("/api/community/")) return url.replace(/^\/api/, "");

  // 2) 혹시 다른 형태면: country/board_slug + 마지막 id 파싱해서 조립
  const parts = url.split("/").filter(Boolean);
  const last = parts[parts.length - 1];
  const id = Number(last);
  if (p?.country && p?.board_slug && Number.isFinite(id)) {
    return `/community/${p.country}/${p.board_slug}/${id}`;
  }

  return null;
};

const toFrontPathFromComment = (c) => {
  const url = trimSlash(c?.detail_url || "");
  // 명세서: "/community/kr/free/3"
  if (url.startsWith("/community/")) return url;
  // 혹시 API로 오면 보정
  if (url.startsWith("/api/community/")) return url.replace(/^\/api/, "");
  return null;
};

const goPost = (p) => {
  const path = toFrontPathFromPost(p);
  if (path) router.push(path);
};

const goComment = (c) => {
  const path = toFrontPathFromComment(c);
  if (path) router.push(path);
};

const fetchPosts = async () => {
  loadingPosts.value = true;
  errorPosts.value = "";
  try {
    const { data } = await getMyPosts();
    posts.value = data || [];
  } catch (e) {
    errorPosts.value = "내 게시글을 불러오지 못했습니다.";
    posts.value = [];
  } finally {
    loadingPosts.value = false;
  }
};

const fetchComments = async () => {
  loadingComments.value = true;
  errorComments.value = "";
  try {
    const { data } = await getMyComments();
    comments.value = data || [];
  } catch (e) {
    errorComments.value = "내 댓글을 불러오지 못했습니다.";
    comments.value = [];
  } finally {
    loadingComments.value = false;
  }
};

onMounted(async () => {
  await Promise.all([fetchPosts(), fetchComments()]);
});
</script>

<style scoped>
.my-activity { margin-top: 18px; }
.title { margin: 16px 0 10px; }

.tabs { display: flex; gap: 8px; margin: 8px 0 12px; }
.tabs button { padding: 8px 10px; border: 1px solid #ddd; border-radius: 10px; background: #fff; cursor: pointer; }
.tabs button.on { border-color: #1a73e8; color: #1a73e8; font-weight: 700; }

.msg { padding: 10px 0; color: #555; }
.msg.error { color: #c00; }

.list { list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }
.item { border: 1px solid #eee; border-radius: 12px; padding: 12px; cursor: pointer; }
.row1 { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.badge { font-size: 12px; opacity: 0.85; }
.date { font-size: 12px; opacity: 0.7; }
.row2 { margin-top: 6px; font-size: 14px; }
.row3 { margin-top: 6px; font-size: 13px; opacity: 0.85; }
</style>
