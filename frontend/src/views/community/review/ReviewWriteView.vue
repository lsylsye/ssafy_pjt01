<template>
  <section class="wrap">
    <!-- ✅ 도서 검색 영역 (선택된 책이 있으면 기본 숨김) -->
    <div v-if="showSearch">
      <h2 class="h2">도서 검색</h2>

      <div class="searchbar">
        <input
          v-model="bookQ"
          class="searchInput"
          placeholder="책 제목/저자 검색"
          @keyup.enter="searchBook"
        />
        <button class="searchBtn" @click="searchBook" :disabled="bookSearching">
          검색
        </button>
      </div>

      <div v-if="bookSearching" class="msg">검색 중...</div>
      <div v-else-if="bookError" class="error">{{ bookError }}</div>

      <ul v-else class="resultList">
        <li
          v-for="b in bookResults"
          :key="b._key"
          class="resultItem"
          @click="selectBook(b)"
        >
          <img v-if="b.cover" :src="b.cover" class="cover" alt="cover" />
          <div v-else class="cover placeholder"></div>

          <div class="info">
            <div class="title">{{ b.title }}</div>
            <div class="author">{{ b.author }}</div>
            <div class="pub">{{ b.publisher || "-" }}</div>
          </div>
        </li>
      </ul>

      <p v-if="!bookSearching && !bookError && bookResults.length === 0" class="hint">
        검색 결과를 클릭하면 아래 리뷰 작성 폼에 자동 입력돼.
      </p>

      <hr class="hr" />
    </div>

    <!-- ✅ 선택된 책이 있으면 요약 + 다시 검색 버튼 -->
    <div v-else class="selectedBar">
      <div class="selectedText">
        선택된 도서: {{ book_title || "-" }} / {{ book_author || "-" }}
      </div>
      <button class="btn" @click="openSearch">다른 도서 선택</button>
    </div>

    <h3 class="h3">리뷰 작성</h3>

    <div class="form">
      <div class="row">
        <label class="label">책 제목(필수)</label>
        <input v-model="book_title" class="input" placeholder="도서 검색으로 자동 입력 가능" />
      </div>

      <div class="row">
        <label class="label">저자(필수)</label>
        <input v-model="book_author" class="input" placeholder="도서 검색으로 자동 입력 가능" />
      </div>

      <div class="row">
        <label class="label">평점(선택)</label>
        <input
          v-model.number="rating"
          class="input"
          type="number"
          min="1"
          max="5"
          placeholder="1~5"
        />
      </div>

      <div class="row">
        <label class="label">리뷰 내용(필수)</label>
        <textarea v-model="content" class="textarea" placeholder="리뷰 내용을 입력하세요"></textarea>
      </div>

      <div class="extra">
        <div>isbn13: {{ isbn13 || "-" }}</div>
        <div>출판사: {{ publisher || "-" }}</div>
        <div>출간일: {{ pub_date || "-" }}</div>
      </div>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

      <div class="actions">
        <button class="btn" @click="submit" :disabled="saving">등록</button>
        <button class="btn" @click="goBack" :disabled="saving">취소</button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/api/axios";
import { createReview } from "@/api/review";

const route = useRoute();
const router = useRouter();
const country = computed(() => String(route.params.country || "kr"));
const apiCountry = (c) => String(c || "kr").toLowerCase();

// ✅ 검색영역 표시 여부 (query로 책이 들어오면 기본 false)
const showSearch = ref(true);

// 도서 검색 상태
const bookQ = ref("");
const bookSearching = ref(false);
const bookError = ref("");
const bookResults = ref([]);

// 리뷰 입력값
const book_title = ref("");
const book_author = ref("");
const rating = ref(null);
const content = ref("");

// 자동 채움 옵션
const isbn13 = ref("");
const publisher = ref("");
const pub_date = ref("");
const cover = ref("");

// 저장 상태
const saving = ref(false);
const errorMsg = ref("");

// ✅ 다양한 응답 키를 흡수해서 통일
const normalizeBook = (raw) => {
  const title = raw.title || raw.book_title || raw.bookTitle || "";
  const author = raw.author || raw.book_author || raw.bookAuthor || "";
  const publisher = raw.publisher || "";
  const pub_date = raw.pub_date || raw.pubDate || raw.pubdate || "";
  const cover = raw.cover || raw.cover_url || raw.coverUrl || "";
  const isbn13 = raw.isbn13 || raw.isbn || raw.isbn_13 || "";

  return {
    _key: isbn13 || `${title}_${author}`,
    title,
    author,
    publisher,
    pub_date,
    cover,
    isbn13,
  };
};

// ✅ 200 OK인데 안 뜨는 원인: res.data가 배열이 아닐 때가 많음
const extractArray = (raw) => {
  if (!raw) return [];
  if (Array.isArray(raw)) return raw;

  // DRF pagination
  if (Array.isArray(raw.results)) return raw.results;

  // 흔한 케이스들
  if (Array.isArray(raw.items)) return raw.items;
  if (Array.isArray(raw.item)) return raw.item;

  // 감싸진 data
  if (raw.data && Array.isArray(raw.data)) return raw.data;

  return [];
};

const searchBook = () => {
  const q = bookQ.value.trim();
  if (!q) return;

  bookSearching.value = true;
  bookError.value = "";
  bookResults.value = [];

  api
    .get("/api/books/search/", { params: { q }, auth: false })
    .then((res) => {
      const raw = res.data;
      const arr = extractArray(raw);

      console.log("books search raw:", raw);
      console.log("books search arr length:", arr.length);

      bookResults.value = arr.map(normalizeBook);
    })
    .catch((err) => {
      console.error("[도서 검색 실패]", err.response?.status, err.response?.data || err.message);
      bookError.value = "도서 검색에 실패했습니다.";
      bookResults.value = [];
    })
    .finally(() => {
      bookSearching.value = false;
    });
};

const selectBook = (b) => {
  book_title.value = b.title || "";
  book_author.value = b.author || "";
  isbn13.value = b.isbn13 || "";
  publisher.value = b.publisher || "";
  pub_date.value = b.pub_date || "";
  cover.value = b.cover || "";

  // ✅ 클릭하면 검색 결과/검색창 정리 + 검색영역 닫기
  bookResults.value = [];
  bookQ.value = "";
  bookError.value = "";
  showSearch.value = false;
};

const openSearch = () => {
  showSearch.value = true;
};

const applyQueryPrefill = () => {
  const q = route.query || {};

  // BookDetailView에서 보내는 키 기준
  const qt = String(q.book_title || "");
  const qa = String(q.book_author || "");

  if (qt || qa) {
    book_title.value = qt;
    book_author.value = qa;

    isbn13.value = String(q.isbn13 || "");
    publisher.value = String(q.publisher || "");
    pub_date.value = String(q.pub_date || "");
    cover.value = String(q.cover || "");

    // ✅ query로 들어오면 검색영역 기본 숨김
    showSearch.value = false;
    bookResults.value = [];
    bookQ.value = "";
    bookError.value = "";
  }
};

const submit = () => {
  errorMsg.value = "";

  const payload = {
    book_title: book_title.value.trim(),
    book_author: book_author.value.trim(),
    content: content.value.trim(),
  };

  if (!payload.book_title || !payload.book_author || !payload.content) {
    errorMsg.value = "필수 항목(책 제목/저자/내용)을 입력해줘.";
    return;
  }

  if (rating.value !== null && rating.value !== "" && !Number.isNaN(Number(rating.value))) {
    payload.rating = Number(rating.value);
  }

  if (isbn13.value) payload.isbn13 = isbn13.value;
  if (publisher.value) payload.publisher = publisher.value;
  if (pub_date.value) payload.pub_date = pub_date.value;
  if (cover.value) payload.cover = cover.value;

  saving.value = true;

  const c = apiCountry(country.value);
  createReview(c, payload)
    .then((res) => {
      const newId = res.data?.id;
      router.replace(newId ? `/community/${c}/review/${newId}` : `/community/${c}/review`);
    })
    .catch((err) => {
      console.error("[리뷰 작성 실패]", err.response?.status, err.response?.data || err.message);
      errorMsg.value = "등록에 실패했어.";
    })
    .finally(() => {
      saving.value = false;
    });
};

const goBack = () => router.back();

onMounted(() => {
  applyQueryPrefill();
});
</script>

<style scoped>
.wrap { max-width: 860px; }

.h2 { font-size: 44px; margin: 0 0 16px; }
.h3 { margin: 0 0 12px; }

.searchbar { display: flex; gap: 8px; align-items: center; margin-bottom: 16px; }
.searchInput {
  flex: 1;
  height: 42px;
  padding: 0 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.searchBtn {
  height: 42px;
  padding: 0 12px;
  border: 1px solid #aaa;
  background: #f5f5f5;
  border-radius: 4px;
  cursor: pointer;
}

.msg { margin: 8px 0; }
.hint { margin: 8px 0; color: #666; }

.error { color: #d33; margin: 8px 0; }

.resultList { list-style: none; padding: 0; margin: 0; }
.resultItem {
  display: flex;
  gap: 16px;
  padding: 18px 0;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}
.resultItem:hover { background: #fafafa; }

.cover { width: 90px; height: 120px; object-fit: cover; }
.cover.placeholder { background: #e9e9e9; }

.info { min-width: 0; }
.title { font-size: 22px; font-weight: 800; margin-bottom: 8px; }
.author { font-size: 16px; color: #333; margin-bottom: 8px; }
.pub { font-size: 16px; color: #666; }

.hr { margin: 24px 0; }

.selectedBar{
  display:flex;
  align-items:center;
  justify-content: space-between;
  gap: 10px;
  margin: 0 0 16px;
  padding: 12px 14px;
  border: 1px solid #eee;
  border-radius: 12px;
  background: #fafafa;
}
.selectedText{ color:#333; }

.form { border: 1px solid #eee; border-radius: 12px; padding: 12px 14px; }
.row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px; }
.label { font-size: 13px; color: #444; }

.input, .textarea {
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.textarea { min-height: 160px; resize: vertical; }

.extra {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 10px;
  background: #fafafa;
  color: #555;
  font-size: 13px;
  margin-top: 10px;
}

.actions { display: flex; gap: 10px; margin-top: 12px; }
.btn {
  border: 1px solid #ddd;
  background: white;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}
.btn:hover { border-color: #1a73e8; color: #1a73e8; }
</style>
