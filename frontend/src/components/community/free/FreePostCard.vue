<template>
  <li class="item">
    <router-link :to="to" class="link">
      <div class="row">
        <span v-if="post.prefix_name" class="prefix">[{{ post.prefix_name }}]</span>
        <span class="title">{{ post.title }}</span>
      </div>

      <div class="meta">
        <span>{{ post.user_nickname }}</span>
        <span>· {{ formatDate(post.created_at) }}</span>
        <span>· 좋아요 {{ post.like_count }}</span>
        <span>· 댓글 {{ post.comment_count }}</span>
      </div>

      <p class="content">{{ post.content }}</p>
    </router-link>
  </li>
</template>

<script setup>
const props = defineProps({
  post: { type: Object, required: true },
  to: { type: String, required: true },
});

const formatDate = (iso) => (typeof iso === "string" ? iso.slice(0, 10) : "");
</script>

<style scoped>
.item { border:1px solid #eee; border-radius:12px; padding:12px 14px; }
.link { text-decoration:none; color:inherit; display:block; }
.row { display:flex; gap:8px; align-items:center; margin-bottom:6px; }
.prefix { color:#1a73e8; font-weight:700; }
.title { font-weight:800; }
.meta { color:#666; font-size:14px; display:flex; gap:8px; flex-wrap:wrap; margin-bottom:8px; }
.content { margin:0; color:#333; }
</style>
