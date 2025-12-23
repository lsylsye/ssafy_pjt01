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
.item {
  border: none;
  border-radius: 8px;
  padding: 16px;
  background: #ffffff;
  transition: var(--transition);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  border-left: 4px solid #f0f0f0;
}

.item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  border-left-color: var(--primary-color);
  transform: translateY(-2px);
}

.link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.row {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.prefix {
  color: var(--primary-color);
  font-weight: 700;
  font-size: 11px;
  background: rgba(34, 197, 94, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
  flex-shrink: 0;
}

.title {
  font-weight: 700;
  font-size: 15px;
  color: var(--text-primary);
  flex: 1;
  word-break: break-word;
}

.meta {
  color: #999;
  font-size: 12px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 8px;
  margin-top: 6px;
}

.content {
  margin: 0;
  color: #666;
  font-size: 13px;
  line-height: 1.5;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  word-break: break-word;
}
</style>
