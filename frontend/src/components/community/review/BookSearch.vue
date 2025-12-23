<template>
  <div class="wrap">
    <h3 class="h3">도서 검색</h3>

    <div class="searchbar">
      <input
        v-model="q"
        class="searchInput"
        placeholder="책 제목/저자 검색"
        @keyup.enter="search"
      />
      <button class="searchBtn" :disabled="loading" @click="search">검색</button>
    </div>

    <div v-if="loading" class="msg">검색 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <ul v-else class="resultList">
      <li v-for="b in results" :key="b._key" class="resultItem" @click="$emit('select', b)">
        <img v-if="b.cover" :src="b.cover" class="cover" alt="cover" />
        <div v-else class="cover placeholder"></div>

        <div class="info">
          <div class="title">{{ b.title }}</div>
          <div class="author">{{ b.author }}</div>
          <div class="pub">{{ b.publisher || "-" }}</div>
        </div>
      </li>
    </ul>

    <p v-if="!loading && !error && results.length === 0" class="hint">
      검색 결과를 클릭하면 아래 리뷰 작성 폼에 자동 입력돼.
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "@/api/axios";

defineEmits(["select"]);

const q = ref("");
const loading = ref(false);
const error = ref("");
const results = ref([]);

const normalizeBook = (raw) => {
  const title = raw.title || raw.book_title || raw.bookTitle || "";
  const author = raw.author || raw.book_author || raw.bookAuthor || "";
  const publisher = raw.publisher || "";
  const pub_date = raw.pub_date || raw.pubDate || raw.pubdate || "";
  const cover = raw.cover || raw.cover_url || raw.coverUrl || "";
  const isbn13 = raw.isbn13 || raw.isbn || raw.isbn_13 || "";
  return { _key: isbn13 || `${title}_${author}`, title, author, publisher, pub_date, cover, isbn13 };
};

const extractArray = (raw) => {
  if (!raw) return [];
  if (Array.isArray(raw)) return raw;
  if (Array.isArray(raw.results)) return raw.results;
  if (Array.isArray(raw.items)) return raw.items;
  if (Array.isArray(raw.item)) return raw.item;
  if (raw.data && Array.isArray(raw.data)) return raw.data;
  return [];
};

const search = async () => {
  const v = q.value.trim();
  if (!v) return;

  loading.value = true;
  error.value = "";
  results.value = [];

  try {
    const res = await api.get("/api/books/search/", { params: { q: v }, auth: false });
    const arr = extractArray(res.data);
    results.value = arr.map(normalizeBook);
  } catch (e) {
    error.value = "도서 검색에 실패했습니다.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.wrap {
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.h3 {
  margin: 0 0 12px;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
}

.searchbar {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 12px;
}

.searchInput {
  flex: 1;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
  background: #ffffff;
  color: var(--text-primary);
  transition: var(--transition);
  font-family: inherit;
}

.searchInput:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.1);
}

.searchBtn {
  height: 40px;
  padding: 0 16px;
  border: 1px solid var(--primary-color);
  background: var(--primary-lighter);
  color: var(--primary-dark);
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: var(--transition);
  font-size: 13px;
}

.searchBtn:hover {
  background: var(--primary-light);
}

.searchBtn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.msg {
  margin: 10px 0;
  color: #999;
  font-size: 13px;
}

.hint {
  margin: 10px 0;
  color: #999;
  font-size: 12px;
}

.error {
  color: #dc2626;
  background: #fee2e2;
  padding: 10px 12px;
  border-radius: 6px;
  margin: 10px 0;
  font-size: 12px;
}

.resultList {
  list-style: none;
  padding: 0;
  margin: 0;
}

.resultItem {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: var(--transition);
}

.resultItem:hover {
  background: #f9f9f9;
  padding: 12px 8px;
  border-radius: 6px;
}

.cover {
  width: 60px;
  height: 84px;
  object-fit: cover;
  border-radius: 4px;
  flex-shrink: 0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}

.cover.placeholder {
  background: #f0f0f0;
}

.info {
  min-width: 0;
  flex: 1;
}

.title {
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--text-primary);
  font-size: 13px;
}

.author {
  color: var(--text-primary);
  margin-bottom: 4px;
  font-size: 12px;
}

.pub {
  color: #999;
  font-size: 11px;
}
</style>
