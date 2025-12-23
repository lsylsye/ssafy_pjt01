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
  width: 170px;
  flex: 0 0 auto;
  transition: var(--transition);
}

.link {
  display: block;
  text-decoration: none;
  color: inherit;
  border-radius: 12px;
  overflow: hidden;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: var(--transition);
}

.link:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
}

.link.disabled {
  cursor: default;
}

.thumb {
  width: 100%;
  aspect-ratio: 3 / 4;
  border-radius: 0;
  overflow: hidden;
  border: none;
  background: var(--bg-secondary);
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
  background: linear-gradient(135deg, var(--primary-lighter) 0%, var(--bg-tertiary) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.meta {
  padding: 12px;
}

.title {
  font-size: 13px;
  font-weight: 700;
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  min-height: 36px;
  color: var(--text-primary);
}

.author {
  margin-top: 6px;
  font-size: 12px;
  color: var(--text-light);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.link:hover .title {
  color: var(--primary-color);
}
</style>
