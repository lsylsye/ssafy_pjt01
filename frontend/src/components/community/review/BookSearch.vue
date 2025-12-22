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
.wrap { border:1px solid #eee; border-radius:12px; padding:12px 14px; margin-bottom:14px; }
.h3 { margin:0 0 12px; }
.searchbar { display:flex; gap:8px; align-items:center; margin-bottom:12px; }
.searchInput { flex:1; height:42px; padding:0 10px; border:1px solid #ddd; border-radius:8px; }
.searchBtn { height:42px; padding:0 12px; border:1px solid #ddd; background:#f5f5f5; border-radius:8px; cursor:pointer; }
.msg { margin:8px 0; }
.hint { margin:8px 0; color:#666; }
.error { color:#d33; margin:8px 0; }
.resultList { list-style:none; padding:0; margin:0; }
.resultItem { display:flex; gap:12px; padding:12px 0; border-bottom:1px solid #eee; cursor:pointer; }
.resultItem:hover { background:#fafafa; }
.cover { width:70px; height:96px; object-fit:cover; border-radius:8px; }
.cover.placeholder { background:#e9e9e9; }
.info { min-width:0; }
.title { font-weight:800; margin-bottom:6px; }
.author { color:#333; margin-bottom:6px; }
.pub { color:#666; }
</style>
