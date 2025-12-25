<!-- src/views/BookDetailView.vue -->
<template>
  <div class="page">
    <div class="container">
      <!-- LEFT: 메인 정보 (헤더 + AI 인사이트) -->
      <div class="main-content">
        <!-- 1. 도서 헤더 -->
        <section class="book-header-section">
          <div v-if="bookLoading" class="header-skeleton">
            <div class="sk-cover"></div>
            <div class="sk-lines">
              <div class="sk-line w60"></div>
              <div class="sk-actions"></div>
            </div>
          </div>

          <div v-else class="book-header">
            <div class="cover-wrap">
              <img v-if="book.cover" :src="book.cover" class="cover-img" alt="" />
              <div v-else class="cover-ph">No Cover</div>
            </div>

            <div class="info-wrap">
              <h1 class="book-title">{{ book.title || "-" }}</h1>
              <div class="book-meta">
                <span>{{ book.author || "-" }}</span>
                <span class="dot">·</span>
                <span>{{ book.publisher || "-" }}</span>
              </div>

              <div class="book-rating-info">
                <span class="star-icon">★</span>
                <span class="rating-val">{{ (book.customerReviewRank / 2).toFixed(1) }}</span>
                <span class="sales-val">(판매지수 {{ book.sales_point?.toLocaleString() }})</span>
              </div>

              <div class="action-row">
                <button class="btn-primary" type="button" @click="goWriteReview">
                  <PenLine :size="18" /> 기록 심기
                </button>
                <button class="btn-secondary" type="button" @click="toggleBookmark" :disabled="bookmarking">
                  <Bookmark :size="18" :fill="book.is_bookmarked ? 'currentColor' : 'none'" /> 북마크
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- 2. AI 큐레이팅 그리드 (한 줄에 2개씩) -->
        <div class="ai-grid">
          <article class="ai-card">
            <div class="ai-header">✨ AI 3줄 요약</div>
            <div v-if="aiLoading" class="ai-loading-box">
              <div class="sk-box"></div>
              <p class="loading-txt">AI가 책을 분석하고 있어요...</p>
            </div>
            <div v-else-if="aiError" class="ai-error">{{ aiError }}</div>
            <div v-else>
              <div v-for="(line, i) in ai3Lines" :key="i" class="summary-box">{{ line }}</div>
              <div class="keyword-row">
                <span v-for="k in ai.keywords.slice(0, 6)" :key="k" class="keyword-chip">#{{ k }}</span>
              </div>
            </div>
          </article>

          <article class="ai-card">
            <div class="ai-header">👍 추천 대상</div>
            <div v-if="aiLoading" class="ai-loading-box">
              <div class="sk-box"></div>
            </div>
            <div v-else-if="aiError" class="ai-error">{{ aiError }}</div>
            <div v-else class="target-stack">
              <div v-for="(t, i) in ai.recommend_targets.slice(0, 4)" :key="i" class="target-bubble">
                <span class="bubble-txt">{{ t }}</span>
              </div>
            </div>
          </article>

          <article class="ai-card">
            <div class="ai-header">💬 독자 반응</div>
            <div v-if="aiLoading" class="ai-loading-box">
              <div class="sk-box"></div>
            </div>
            <div v-else-if="aiError" class="ai-error">{{ aiError }}</div>
            <div v-else class="reaction-stack">
              <div v-for="(r, i) in ai.summary_reviews.slice(0, 3)" :key="i" class="reaction-bubble">
                <span class="bubble-txt">{{ r }}</span>
              </div>
            </div>
          </article>

          <article class="ai-card">
            <div class="ai-header">✒️ 작가 소개</div>
            <div v-if="aiLoading" class="ai-loading-box">
              <div class="sk-box"></div>
            </div>
            <div v-else-if="aiError" class="ai-error">{{ aiError }}</div>
            <div v-else class="author-box">
              <div class="author-top">
                <img v-if="ai.author_image" :src="ai.author_image" class="author-img" />
                <div v-else class="author-img ph"><User :size="18" /></div>
                <div class="author-name">{{ authorName }}</div>
              </div>
              <p class="author-info">{{ authorInfoText }}</p>
            </div>
          </article>
        </div>
      </div>

      <!-- RIGHT: 플로팅 리뷰 사이드바 -->
      <aside class="review-aside">
        <div class="side-header">
          <h2 class="side-title">심어진 잔디들 🌱</h2>
          <span class="side-count">{{ book.review_count }}</span>
        </div>

        <div class="side-scroll-area">
          <div v-if="bookLoading" class="sk-r-list">
             <div v-for="i in 3" :key="i" class="sk-r-item"></div>
          </div>

          <div v-else-if="book.reviews && book.reviews.length > 0" class="review-list">
            <div v-for="rev in book.reviews" :key="rev.id" class="r-card" @click="goReviewDetail(rev.id)">
              <div class="r-top">
                <div class="r-avatar" @click.stop="goProfile(rev.user_id)">
                  <img v-if="rev.user_profile_image" :src="getProfileImage(rev.user_profile_image)" />
                  <User v-else :size="14" />
                </div>
                <div class="r-meta">
                  <div class="r-nick" @click.stop="goProfile(rev.user_id)">{{ rev.user_nickname }}</div>
                  <div class="r-stars">
                    <Star v-for="i in 5" :key="i" :size="10" 
                      :fill="i <= rev.rating ? '#FFD700' : 'none'" 
                      :color="i <= rev.rating ? '#FFD700' : '#e5e8eb'" />
                  </div>
                </div>
                <div class="r-date">{{ formatDate(rev.created_at) }}</div>
              </div>
              <p class="r-content">{{ rev.content }}</p>
            </div>
          </div>

          <div v-else class="r-empty">
             아직 이야기가 없어요.<br/>첫 잔디를 심어보세요!
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/api/axios";
import { Star, User, Bookmark, PenLine } from "lucide-vue-next";

const route = useRoute();
const router = useRouter();

const isbn13 = computed(() => String(route.params.isbn13 || route.query.isbn13 || "").trim());

const bookLoading = ref(true);
const bookError = ref("");
const book = ref({
  title: "",
  author: "",
  publisher: "",
  pub_date: "",
  cover: "",
  description: "",
  is_bookmarked: false,
  customerReviewRank: 0,
  sales_point: 0,
  review_count: 0,
  reviews: []
});

const aiLoading = ref(false);
const aiError = ref("");
const ai = ref({
  story_summary: "",
  summary_reviews: [],
  keywords: [],
  recommend_targets: [],
  author_info: "",
  author_image: "",
});

const bookmarking = ref(false);

const authorOpen = ref(false);
const AUTHOR_LIMIT = 280;

const isAuthorInfoLong = computed(() => (ai.value.author_info || "").length > AUTHOR_LIMIT);

const authorInfoText = computed(() => {
  const t = (ai.value.author_info || "").replace(/\s+/g, " ").trim();
  if (!t) return "작가 정보가 없어요.";
  if (authorOpen.value) return t;
  return t.length > AUTHOR_LIMIT ? t.slice(0, AUTHOR_LIMIT) + "…" : t;
});

const authorName = computed(() => {
  const a = (book.value.author || "").trim();
  if (a) return a.replace(/\s*\(.*?\)\s*/g, "").trim();
  const info = (ai.value.author_info || "").trim();
  if (!info) return "작가";
  return info.split(/[（(,]/)[0].slice(0, 20);
});

const ai3Lines = computed(() => {
  const raw = (ai.value.story_summary || "").trim();
  if (!raw) return ["AI 요약 정보가 없어요."];
  const parts = raw
    .replace(/\s+/g, " ")
    .split(/(?<=[.!?。])\s+/)
    .map((s) => s.trim())
    .filter(Boolean);

  if (parts.length >= 3) return parts.slice(0, 3);

  if (raw.length > 180) {
    return [raw.slice(0, 70) + "…", raw.slice(70, 140) + "…", raw.slice(140, 210) + "…"].map((s) => s.trim());
  }
  return [raw];
});

async function fetchBook() {
  bookLoading.value = true;
  bookError.value = "";

  try {
    if (!isbn13.value) throw new Error("isbn13가 없습니다.");

    const res = await api.get(`books/${encodeURIComponent(isbn13.value)}/`);
    const d = res?.data || {};

    book.value = {
      title: d.title || "",
      author: d.author || "",
      publisher: d.publisher || "",
      pub_date: d.pub_date || d.pubDate || "",
      cover: d.cover || "",
      description: d.description || "",
      is_bookmarked: !!d.is_bookmarked,
      customerReviewRank: d.customerReviewRank || 0,
      sales_point: d.sales_point || 0,
      review_count: d.review_count || 0,
      reviews: Array.isArray(d.reviews) ? d.reviews : []
    };
  } catch (e) {
    bookError.value = "도서 정보를 불러오지 못했습니다.";
    console.error("[BookDetail] fetchBook error:", e?.response?.status, e?.response?.data || e?.message);
  } finally {
    bookLoading.value = false;
  }
}

async function fetchAi() {
  aiLoading.value = true;
  aiError.value = "";
  authorOpen.value = false;

  try {
    if (!isbn13.value) throw new Error("isbn13가 없습니다.");

    const res = await api.get(`ai_curator/${encodeURIComponent(isbn13.value)}/`);
    const d = res?.data || {};

    ai.value = {
      story_summary: d.story_summary || "",
      summary_reviews: Array.isArray(d.summary_reviews) ? d.summary_reviews : [],
      keywords: Array.isArray(d.keywords) ? d.keywords : [],
      recommend_targets: Array.isArray(d.recommend_targets) ? d.recommend_targets : [],
      author_info: d.author_info || "",
      author_image: d.author_image || "",
    };
  } catch (e) {
    aiError.value = "AI 정보를 불러오지 못했습니다.";
    console.error("[BookDetail] fetchAi error:", e?.response?.status, e?.response?.data || e?.message);
  } finally {
    aiLoading.value = false;
  }
}

function goWriteReview() {
  if (!isbn13.value) return;
  router.push({
    path: "/review/write",
    query: {
      isbn13: isbn13.value,
      title: book.value.title,
      author: book.value.author,
      publisher: book.value.publisher,
      cover: book.value.cover,
    },
  });
}

async function toggleBookmark() {
  if (!isbn13.value || bookmarking.value) return;

  bookmarking.value = true;
  try {
    const res = await api.post(`books/${encodeURIComponent(isbn13.value)}/bookmark/`);
    if (res?.data && typeof res.data.bookmarked === "boolean") {
      book.value.is_bookmarked = res.data.bookmarked;
    } else {
      book.value.is_bookmarked = !book.value.is_bookmarked;
    }
  } catch (e) {
    console.error("[BookDetail] toggleBookmark error:", e?.response?.status, e?.response?.data || e?.message);
  } finally {
    bookmarking.value = false;
  }
}

const getProfileImage = (url) => {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  const path = String(url).startsWith("/") ? url : `/${url}`;
  return `http://127.0.0.1:8000${path}`;
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString();
};

const goProfile = (userId) => {
  if (!userId) return;
  router.push(`/profile/${userId}`);
};

const goReviewDetail = (reviewId) => {
  if (!reviewId) return;
  router.push(`/reviews/${reviewId}`);
};

onMounted(async () => {
  await fetchBook();
  fetchAi();
});

watch(
  () => isbn13.value,
  async (v, oldV) => {
    if (!v || v === oldV) return;
    await fetchBook();
    fetchAi();
  }
);
</script>

<style scoped>
.page { 
  min-height: calc(100vh - 70px);
  padding: 40px 0;
}
.container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

/* LEFT: Main Content */
.main-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.book-header {
  display: flex;
  gap: 32px;
  background: white;
  padding: 32px;
  border-radius: 24px;
  border: 1px solid rgba(0,0,0,0.03);
}
.cover-img {
  width: 160px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.info-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.book-title {
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 8px;
  color: #191f28;
}
.book-meta {
  color: #8b95a1;
  font-size: 1rem;
  margin-bottom: 24px;
}
.dot { margin: 0 4px; opacity: 0.5; }

.rating-max {
  font-size: 0.95rem;
  color: #8b95a1;
  font-weight: 500;
}

.book-rating-info {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 24px;
}
.star-icon {
  color: #FFD700;
  font-size: 1.2rem;
}
.rating-val {
  font-size: 1.15rem;
  font-weight: 800;
  color: #191f28;
}
.sales-val {
  font-size: 0.95rem;
  color: #8b95a1;
  font-weight: 400;
}

.action-row { display: flex; gap: 10px; }
.btn-primary, .btn-secondary {
  display: flex; align-items: center; gap: 6px;
  padding: 10px 20px; border-radius: 12px;
  font-weight: 700; font-size: 0.95rem;
  transition: 0.2s;
}
.btn-primary { background: #00D15B; color: white; }
.btn-secondary { background: white; color: #4e5968; border: 1px solid #e5e8eb; }

/* AI Cards Grid */
.ai-grid { 
  display: grid; 
  grid-template-columns: repeat(2, 1fr); 
  gap: 16px; 
}
.ai-card {
  background: white; padding: 22px; border-radius: 20px;
  border: 1px solid rgba(0,0,0,0.03);
  display: flex;
  flex-direction: column;
  transition: 0.3s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.01);
}
.ai-card:hover { 
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.04);
}

/* Recommend & Reaction Shared Bubble Style */
.target-stack, .reaction-stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.target-bubble, .reaction-bubble {
  background: #f9fafb;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #f2f4f6;
}
.target-bubble { border-radius: 12px 12px 2px 12px; } /* Slightly different notch for distinction */
.reaction-bubble { border-radius: 12px 12px 12px 2px; }

.bubble-txt {
  font-size: 0.88rem;
  line-height: 1.5;
  color: #4e5968;
  font-weight: 500;
  display: block;
}

.ai-header { font-weight: 800; color: #00d15b; margin-bottom: 16px; font-size: 0.95rem; }
.summary-box {
  background: #f9fafb; padding: 12px; border-radius: 12px;
  font-size: 0.88rem; line-height: 1.5; color: #4e5968; margin-bottom: 8px;
}
.keyword-chip {
  display: inline-block; background: #f2f4f6; padding: 4px 10px;
  border-radius: 6px; font-size: 0.8rem; font-weight: 700; margin-right: 4px; margin-bottom: 4px;
}
.recommend-list { padding: 0; margin: 0; list-style: none; }
.recommend-list li { margin-bottom: 8px; font-weight: 600; font-size: 0.88rem; display: flex; align-items: flex-start; }
.check { color: #00d15b; font-weight: 800; margin-right: 6px; flex-shrink: 0; }

.reaction-item { display: flex; gap: 10px; margin-bottom: 14px; }
.quote-mark { font-family: serif; color: #00d15b; font-size: 1.5rem; font-weight: 800; }
.quote-txt { font-size: 0.92rem; color: #4e5968; line-height: 1.5; margin: 0; font-weight: 500; }

.author-top { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.author-img { 
  width: 48px; 
  height: 48px; 
  border-radius: 50%; 
  object-fit: cover; 
  background: #f2f4f6;
  flex-shrink: 0;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.author-img.ph {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  color: #00d15b;
}
.author-name { font-weight: 800; font-size: 1.05rem; color: #191f28; }
.author-info { font-size: 0.9rem; line-height: 1.6; color: #6b7684; font-weight: 500; }

/* RIGHT: Review Sidebar */
.review-aside {
  width: 360px;
  position: sticky;
  top: 90px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 10px 40px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 120px);
}
.side-header {
  padding: 20px 24px;
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}
.side-title { font-size: 1.1rem; font-weight: 800; }
.side-count { 
  background: #00d15b; color: white; border-radius: 99px;
  padding: 2px 10px; font-size: 0.8rem; font-weight: 700;
}

.side-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}
.side-scroll-area::-webkit-scrollbar { width: 6px; }
.side-scroll-area::-webkit-scrollbar-thumb { 
  background: rgba(0,0,0,0.08); border-radius: 10px; 
}

.r-card {
  background: white; padding: 16px; border-radius: 16px;
  margin-bottom: 12px; border: 1px solid rgba(0,0,0,0.02);
  box-shadow: 0 2px 8px rgba(0,0,0,0.01);
  cursor: pointer;
  transition: 0.2s;
}
.r-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border-color: #00D15B;
  background: #f9fffb;
}
.r-top { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.r-avatar { width: 32px; height: 32px; border-radius: 50%; overflow: hidden; background: #f2f4f6; cursor: pointer; }
.r-avatar img { width: 100%; height: 100%; object-fit: cover; }
.r-meta { flex: 1; }
.r-nick { font-weight: 800; font-size: 0.85rem; color: #191f28; cursor: pointer; }
.r-stars { display: flex; gap: 1px; }
.r-date { font-size: 0.75rem; color: #b0b8c1; }
.r-content { font-size: 0.88rem; line-height: 1.5; color: #4e5968; word-break: break-all; }

.r-empty { text-align: center; padding: 60px 20px; color: #b0b8c1; font-weight: 600; font-size: 0.9rem; line-height: 1.6; }

/* Skeletons */
.header-skeleton { display: flex; gap: 32px; }
.sk-cover { width: 160px; height: 230px; border-radius: 12px; background: #f2f4f6; }
.sk-lines { flex: 1; display: flex; flex-direction: column; gap: 16px; justify-content: center; }
.sk-line { height: 24px; border-radius: 12px; background: #f2f4f6; }
.ai-loading-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
}
.loading-txt {
  font-size: 0.85rem;
  color: #adb5bd;
  font-weight: 600;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}

.sk-box { 
  width: 100%;
  height: 60px; 
  border-radius: 12px; 
  background: linear-gradient(90deg, #f2f4f6 25%, #f9fafb 50%, #f2f4f6 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}
@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (max-width: 1024px) {
  .container { flex-direction: column; align-items: stretch; }
  .review-aside { width: 100%; position: static; max-height: none; }
}
</style>
```
