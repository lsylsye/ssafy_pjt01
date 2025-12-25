<!-- src/views/SearchView.vue -->
<template>
  <div class="container">
    <!-- 1. 검색 결과 헤더 -->
    <header class="result-header">
      <div class="result-title">
        '<span class="highlight">{{ q }}</span>' 검색 결과
        <span class="count">{{ total }}</span>개의 씨앗을 찾았어요.
      </div>

      <div class="filter-bar">
        <div class="chips">
          <button class="chip" :class="{ active: scope === 'all' }" @click="scope = 'all'">전체</button>
          <button class="chip" :class="{ active: scope === 'title' }" @click="scope = 'title'">제목</button>
          <button class="chip" :class="{ active: scope === 'author' }" @click="scope = 'author'">저자</button>
          <button class="chip" :class="{ active: scope === 'publisher' }" @click="scope = 'publisher'">출판사</button>
        </div>

        <select class="sort-select" v-model="sortKey">
          <option value="relevance">정확도순</option>
          <option value="latest">최신순</option>
          <option value="popular">리뷰많은순</option>
        </select>
      </div>
    </header>

    <!-- 상태 -->
    <div v-if="books.searchLoading" class="state">검색 중…</div>
    <div v-else-if="books.searchError" class="state error">{{ books.searchError }}</div>

    <!-- 2. 도서 리스트 -->
    <div v-else class="book-list">
      <article
        v-for="b in shownItems"
        :key="b.isbn13 || b.title"
        class="book-card"
        @click="goWrite(b)"
      >
        <div class="cover-wrapper" :style="coverStyle(b)"></div>

        <div class="info-col">
          <div>
            <div class="badges">
              <span v-if="isBest(b)" class="badge best">베스트</span>
              <span class="badge cat">도서</span>
            </div>

            <h3 class="book-title">{{ b.title }}</h3>

            <div class="book-meta">
              {{ b.author || "-" }}
              <span class="divider">|</span>
              {{ b.publisher || "-" }}
              <span class="divider">|</span>
              {{ b.pub_date || "-" }}
            </div>

            <p class="book-desc">
              판매지수 {{ formatNum(b.sales_point) }} · 평점 {{ formatRank(b.customer_review_rank) }}
              (상세 설명은 도서 상세에서 제공 예정)
            </p>
          </div>

          <div class="card-bottom">
            <div class="rating">
              <span class="star">★</span>
              {{ formatRank(b.customer_review_rank) }}
              <span class="review-count">(판매지수 {{ formatNum(b.sales_point) }})</span>
            </div>

            <div class="btn-group" @click.stop>
              <button 
                class="btn btn-outline" 
                :class="{ 'is-bookmarked': b.is_bookmarked }"
                @click="bookmark(b)"
              >
                <Bookmark :size="16" :fill="b.is_bookmarked ? 'currentColor' : 'none'" />
                {{ b.is_bookmarked ? '북마크됨' : '북마크' }}
              </button>
              <button class="btn btn-fill" @click="goWrite(b)">🌱 심기</button>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- 더보기 -->
    <div v-if="canLoadMore" class="load-more">
      <button class="btn-more" @click="loadMore">결과 더 보기 +</button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBooksStore } from "@/stores/books.store";
import { toggleBookmark } from "@/api/books";
import { Bookmark } from "lucide-vue-next";

const route = useRoute();
const router = useRouter();
const books = useBooksStore();

const q = ref(String(route.query.q || "").trim());
const scope = ref("all"); // all | title | author | publisher
const sortKey = ref("relevance"); // relevance | latest | popular

// pagination (백엔드가 page/size 지원하면 사용, 아니면 그냥 1페이지 고정이어도 UI는 안 깨짐)
const page = ref(1);
const size = ref(10);

function runSearch(reset = true) {
  const query = String(q.value || "").trim();
  if (!query) return;

  if (reset) {
    page.value = 1;
    books.search(query, { page: page.value, size: size.value });
  } else {
    page.value += 1;
    books.search(query, { page: page.value, size: size.value, append: true });
  }
}

watch(
  () => route.query.q,
  (nv) => {
    q.value = String(nv || "").trim();
    runSearch(true);
  }
);

onMounted(() => {
  if (q.value) runSearch(true);
});

const rawItems = computed(() => books.searchResults || []);

const filteredItems = computed(() => {
  const query = String(q.value || "").trim().toLowerCase();
  if (!query) return rawItems.value;

  if (scope.value === "all") return rawItems.value;

  return rawItems.value.filter((b) => {
    const t = scope.value === "title" ? (b.title || "") : "";
    const a = scope.value === "author" ? (b.author || "") : "";
    const p = scope.value === "publisher" ? (b.publisher || "") : "";
    return (t + " " + a + " " + p).toLowerCase().includes(query);
  });
});

function toDateNum(s) {
  // "YYYY-MM-DD" -> number
  if (!s) return 0;
  const parts = String(s).slice(0, 10).split("-");
  if (parts.length !== 3) return 0;
  const y = Number(parts[0]), m = Number(parts[1]), d = Number(parts[2]);
  if (!y || !m || !d) return 0;
  return y * 10000 + m * 100 + d;
}

const sortedItems = computed(() => {
  const arr = filteredItems.value.slice();

  if (sortKey.value === "latest") {
    arr.sort((a, b) => toDateNum(b.pub_date) - toDateNum(a.pub_date));
  } else if (sortKey.value === "popular") {
    // “리뷰많은순” 대체: 판매지수(sales_point)로 정렬
    arr.sort((a, b) => (Number(b.sales_point) || 0) - (Number(a.sales_point) || 0));
  }
  // relevance: 원래 순서
  return arr;
});

const total = computed(() => {
  // 백엔드가 total 내려주면 store에 넣어도 되고, 일단 UI는 length로 표시
  return books.searchTotal || sortedItems.value.length;
});

const shownItems = computed(() => sortedItems.value);

const canLoadMore = computed(() => {
  // total이 있고, 현재 list 길이가 total보다 작으면 true
  if (books.searchTotal) return (books.searchResults?.length || 0) < books.searchTotal;
  return false;
});

function loadMore() {
  runSearch(false);
}

function coverStyle(b) {
  if (!b.cover) return { backgroundImage: "none" };
  return { backgroundImage: `url('${b.cover}')` };
}

function isBest(b) {
  return (Number(b.sales_point) || 0) >= 20000;
}

function formatNum(n) {
  const v = Number(n) || 0;
  return v.toLocaleString();
}

function formatRank(r) {
  const v = Number(r) || 0;
  if (!v) return "0.0";
  // 알라딘 customer_review_rank가 0~10 스케일인 경우가 많아서 10->5로 줄이기(보기 좋게)
  const score = Math.min(5, Math.max(0, v / 2));
  return score.toFixed(1);
}

function goWrite(b) {
  const isbn13 = b.isbn13 || "";
  if (!isbn13) return;
  router.push(`/books/${encodeURIComponent(isbn13)}`);
}

async function bookmark(b) {
  const isbn13 = b.isbn13 || "";
  if (!isbn13) return;
  
  try {
    const res = await toggleBookmark(isbn13);
    // res.data.bookmarked 가 참이면 북마크 설정됨
    b.is_bookmarked = !!(res.data.bookmarked ?? !b.is_bookmarked);
  } catch (e) {
    console.error(e);
    alert("북마크 처리에 실패했습니다.");
  }
}
</script>

<style scoped>
:root {
  --primary: #00D15B;
  --primary-dark: #00B54F;
  --bg: #FAFAFA;
  --text-main: #191F28;
  --text-sub: #6B7684;
  --border: #E5E8EB;
}

.container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }

.result-header { margin-bottom: 24px; }
  .result-title { font-size: 1.5rem; font-weight: 400; margin-bottom: 20px; }
.highlight { color: var(--primary); }
.count { font-weight: 800; }

.filter-bar {
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid var(--border); padding-bottom: 16px;
  gap: 12px;
}

.chips { display: flex; gap: 8px; flex-wrap: wrap; }
.chip {
  padding: 8px 16px; border-radius: 20px; background: white; border: 1px solid var(--border);
  color: var(--text-sub); font-weight: 400; font-size: 0.9rem; transition: 0.2s;
}
.chip:hover { background: #F2F4F6; }
.chip.active { background: #191F28; color: white; border-color: #191F28; }

.sort-select {
  font-size: 0.9rem; font-weight: 800; color: var(--text-sub);
  border: none; background: transparent; outline: none; cursor: pointer;
}

.book-list { display: flex; flex-direction: column; gap: 16px; }

.book-card {
  display: flex; gap: 24px; background: white; border-radius: 20px; padding: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid white;
  transition: 0.2s ease; cursor: pointer; position: relative;
}
.book-card:hover {
  transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); border-color: var(--primary);
}

.cover-wrapper {
  width: 120px; height: 174px; flex-shrink: 0; border-radius: 8px;
  background-color: #eee; background-size: cover; background-position: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid #f0f0f0;
}

.info-col { flex: 1; display: flex; flex-direction: column; justify-content: space-between; min-width: 0; }

.badges { margin-bottom: 8px; display: flex; gap: 6px; flex-wrap: wrap; }
.badge { font-size: 0.75rem; font-weight: 900; padding: 4px 8px; border-radius: 6px; }
.badge.best { background: #E8F5E9; color: var(--primary-dark); }
.badge.cat { background: #F2F4F6; color: #666; }

.book-title { font-size: 1.3rem; font-weight: 900; margin-bottom: 6px; line-height: 1.3; }
.book-meta { font-size: 0.95rem; color: var(--text-sub); margin-bottom: 12px; }
.divider { margin: 0 6px; color: #ddd; }

.book-desc {
  font-size: 0.95rem; color: #4E5968; line-height: 1.6; margin-bottom: 16px;
  display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

.card-bottom { display: flex; justify-content: space-between; align-items: flex-end; gap: 12px; flex-wrap: wrap; }

.rating { font-size: 1rem; font-weight: 900; color: #333; display: flex; align-items: center; gap: 6px; }
.star { color: #FFD700; font-size: 1.2rem; }
  .review-count { font-weight: 400; color: #888; font-size: 0.9rem; }

.btn-group { display: flex; gap: 10px; }
.btn {
  padding: 10px 20px; border-radius: 20px; font-weight: 900; font-size: 0.9rem; transition: 0.2s;
}
.btn-outline { border: 1px solid #ddd; color: #666; background: white; display: flex; align-items: center; gap: 6px; }
.btn-outline:hover { border-color: var(--primary); color: var(--primary); }
.btn-outline.is-bookmarked { color: var(--primary); border-color: var(--primary); background: #f0fdf4; }

.btn-fill { background: var(--primary); color: white; border: 1px solid var(--primary); }
.btn-fill:hover { background: var(--primary-dark); transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,209,91,0.2); }

.load-more { text-align: center; margin-top: 50px; }
.btn-more {
  padding: 12px 40px; border-radius: 30px; background: white; border: 1px solid #ddd;
  font-weight: 900; color: #666; transition: 0.2s;
}
.btn-more:hover { background: #f9f9f9; color: #333; }

.state { padding: 16px 4px; font-weight: 900; color: var(--text-sub); }
.state.error { color: #ff4040; }

@media (max-width: 680px){
  .container{ padding: 24px 14px; }
  .book-card{ gap: 16px; padding: 18px; }
  .cover-wrapper{ width: 96px; height: 140px; }
  .book-title{ font-size: 1.1rem; }
}
</style>
