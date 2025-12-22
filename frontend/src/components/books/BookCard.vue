<template>
  <article class="card">
    <router-link v-if="isbn13" class="link" :to="`/books/${isbn13}`">
      <div class="thumb">
        <img v-if="cover" :src="cover" class="img" alt="cover" />
        <div v-else class="placeholder"></div>
      </div>

      <div class="meta">
        <div class="title">{{ title }}</div>
        <div class="author">{{ authorOrDash }}</div>
      </div>
    </router-link>

    <div v-else class="link disabled">
      <div class="thumb">
        <img v-if="cover" :src="cover" class="img" alt="cover" />
        <div v-else class="placeholder"></div>
      </div>

      <div class="meta">
        <div class="title">{{ title }}</div>
        <div class="author">{{ authorOrDash }}</div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  book: { type: Object, required: true },
});

const cover = computed(() => props.book?.cover || "");
const title = computed(() => props.book?.title || "");
const isbn13 = computed(() => props.book?.isbn13 || "");
const authorOrDash = computed(() => props.book?.author || props.book?.book_author || "-");
</script>

<style scoped>
.card {
  width: 170px;            /* ✅ 카드 폭(원하면 160~190 조절) */
  flex: 0 0 auto;
}

.link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.link.disabled {
  cursor: default;
}

.thumb {
  width: 100%;
  aspect-ratio: 3 / 4;     /* ✅ 책 표지 비율 */
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #eee;
  background: #fafafa;
}

.img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.placeholder {
  width: 100%;
  height: 100%;
  background: #f0f0f0;
}

.meta {
  margin-top: 10px;
}

.title {
  font-size: 14px;
  font-weight: 800;
  line-height: 1.35;

  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;   /* ✅ 제목 2줄 */
  -webkit-box-orient: vertical;
  min-height: 38px;
}

.author {
  margin-top: 6px;
  font-size: 12px;
  color: #777;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;     /* ✅ 저자 1줄 */
}
</style>
