<!-- src/views/BookDetailView.vue -->
<template>
  <div class="page">
    <div class="container">
      <!-- LEFT / Sticky -->
      <aside class="sticky-side">
        <div v-if="bookLoading" class="hero-skeleton">
          <div class="sk-cover"></div>
          <div class="sk-line w80"></div>
          <div class="sk-line w60"></div>
          <div class="sk-actions"></div>
        </div>

        <div v-else class="book-hero">
          <div class="cover-wrap">
            <img v-if="book.cover" :src="book.cover" class="cover-img" alt="" />
            <div v-else class="cover-ph">No Cover</div>
          </div>

          <h1 class="book-title">{{ book.title || "-" }}</h1>
          <div class="book-meta">
            <span>{{ book.author || "-" }}</span>
            <span class="dot">·</span>
            <span>{{ book.publisher || "-" }}</span>
            <span v-if="book.pub_date" class="dot">·</span>
            <span v-if="book.pub_date">{{ book.pub_date }}</span>
          </div>

          <div class="action-row">
            <button class="btn-primary" type="button" @click="goWriteReview">
              🌱 리뷰 쓰기
            </button>
            <button class="btn-secondary" type="button" @click="toggleBookmark" :disabled="bookmarking">
              🔖 북마크
            </button>
          </div>
        </div>

        <!-- AI SECTION (only this area loads) -->
        <section class="ai-section">
          <div class="ai-header">✨ AI 3줄 요약</div>

          <div v-if="aiLoading" class="ai-skeleton">
            <div class="sk-box"></div>
            <div class="sk-box"></div>
            <div class="sk-box"></div>
          </div>

          <div v-else-if="aiError" class="ai-error">
            {{ aiError }}
          </div>

          <div v-else>
            <div v-for="(line, i) in ai3Lines" :key="i" class="summary-box">
              {{ line }}
            </div>

            <div v-if="ai.keywords && ai.keywords.length" class="keyword-row">
              <span v-for="k in ai.keywords.slice(0, 10)" :key="k" class="keyword">#{{ k }}</span>
            </div>
          </div>
        </section>

        <section class="ai-section">
          <div class="ai-header">👍 이런 분께 추천해요</div>

          <div v-if="aiLoading" class="ai-skeleton">
            <div class="sk-line w90"></div>
            <div class="sk-line w85"></div>
            <div class="sk-line w80"></div>
          </div>

          <div v-else-if="aiError" class="ai-error">{{ aiError }}</div>

          <ul v-else class="recommend-list">
            <li v-for="(t, i) in (ai.recommend_targets || []).slice(0, 6)" :key="i">
              <span class="check">✔</span>
              <span class="txt">{{ t }}</span>
            </li>
            <li v-if="!(ai.recommend_targets && ai.recommend_targets.length)" class="empty">
              추천 대상 정보가 없어요.
            </li>
          </ul>
        </section>

        <section class="ai-section">
          <div class="ai-header">💬 독자들의 반응</div>

          <div v-if="aiLoading" class="ai-skeleton">
            <div class="sk-card"></div>
            <div class="sk-card"></div>
            <div class="sk-card"></div>
          </div>

          <div v-else-if="aiError" class="ai-error">{{ aiError }}</div>

          <div v-else>
            <div
              v-for="(r, i) in (ai.summary_reviews || []).slice(0, 5)"
              :key="i"
              class="reaction-card"
            >
              “{{ r }}”
            </div>
            <div v-if="!(ai.summary_reviews && ai.summary_reviews.length)" class="empty">
              반응 요약이 없어요.
            </div>
          </div>
        </section>

        <section class="ai-section">
          <div class="ai-header">✒️ 작가 소개</div>

          <div v-if="aiLoading" class="ai-skeleton">
            <div class="sk-author"></div>
          </div>

          <div v-else-if="aiError" class="ai-error">{{ aiError }}</div>

          <div v-else class="author-box">
            <img v-if="ai.author_image" :src="ai.author_image" alt="" class="author-img" />
            <div v-else class="author-img ph"></div>

            <div class="author-meta">
              <div class="author-name">{{ authorName }}</div>
              <p class="author-info">
                {{ authorInfoText }}
              </p>

              <button
                v-if="isAuthorInfoLong"
                class="more-toggle"
                type="button"
                @click="authorOpen = !authorOpen"
              >
                {{ authorOpen ? "접기" : "더보기" }}
              </button>
            </div>
          </div>
        </section>
      </aside>

      <!-- RIGHT -->
      <main class="review-side">
        <h2 class="r-title">이 책에 심어진 잔디들</h2>
        <div class="r-empty">
          리뷰 목록은 다음 단계에서 붙일게. (지금은 상세/AI만)
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/api/axios";

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
  // book.author가 “성해나 (지은이)”처럼 올 수 있어서 앞부분만 정리
  const a = (book.value.author || "").trim();
  if (a) return a.replace(/\s*\(.*?\)\s*/g, "").trim();
  // fallback: author_info 첫 토큰
  const info = (ai.value.author_info || "").trim();
  if (!info) return "작가";
  return info.split(/[（(,]/)[0].slice(0, 20);
});

const ai3Lines = computed(() => {
  const raw = (ai.value.story_summary || "").trim();
  if (!raw) return ["AI 요약 정보가 없어요."];
  // 문장 단위로 잘라서 3줄 생성
  const parts = raw
    .replace(/\s+/g, " ")
    .split(/(?<=[.!?。])\s+/)
    .map((s) => s.trim())
    .filter(Boolean);

  if (parts.length >= 3) return parts.slice(0, 3);

  // 문장이 3개 미만이면 길이로 잘라 3등분 느낌
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

    // 공개 조회로 보고 싶으면 auth:false 권장
    const res = await api.get(`books/${encodeURIComponent(isbn13.value)}/`, { auth: false });
    const d = res?.data || {};

    book.value = {
      title: d.title || "",
      author: d.author || "",
      publisher: d.publisher || "",
      pub_date: d.pub_date || d.pubDate || "",
      cover: d.cover || "",
      description: d.description || "",
      is_bookmarked: !!d.is_bookmarked,
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

    const res = await api.get(`ai_curator/${encodeURIComponent(isbn13.value)}/`, { auth: false });
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
    path: "/reviews/write",
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
    // 인증 필요할 수 있음 (로그인 안했으면 401)
    const res = await api.post(`books/${encodeURIComponent(isbn13.value)}/bookmark/`);
    // 백엔드가 상태를 내려주면 그걸 쓰고, 아니면 토글
    if (res?.data && typeof res.data.is_bookmarked === "boolean") {
      book.value.is_bookmarked = res.data.is_bookmarked;
    } else {
      book.value.is_bookmarked = !book.value.is_bookmarked;
    }
  } catch (e) {
    console.error("[BookDetail] toggleBookmark error:", e?.response?.status, e?.response?.data || e?.message);
  } finally {
    bookmarking.value = false;
  }
}

onMounted(async () => {
  await fetchBook();
  // 책 정보 먼저 보여준 뒤, AI는 별도로 로드
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
.page{ background: var(--bg, #f2f4f6); min-height: 100vh; }
.container{
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 40px;
}

.sticky-side{
  position: sticky;
  top: 20px;
  height: fit-content;
  max-height: calc(100vh - 40px);
  overflow: auto;
  padding-right: 10px;
}
.sticky-side::-webkit-scrollbar{ width: 6px; }
.sticky-side::-webkit-scrollbar-thumb{ background: rgba(0,0,0,0.12); border-radius: 10px; }

.book-hero{ text-align: center; margin-bottom: 26px; }
.cover-wrap{ display:flex; justify-content:center; margin-bottom: 16px; }
.cover-img{
  width: 220px;
  border-radius: 12px;
  box-shadow: 0 18px 36px rgba(0,0,0,0.14);
  transition: 0.25s;
}
.cover-img:hover{ transform: translateY(-4px); }
.cover-ph{
  width:220px; height: 320px;
  border-radius: 12px;
  background: #e5e8eb;
  display:flex; align-items:center; justify-content:center;
  color:#6b7684;
}

.book-title{
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 8px;
  letter-spacing: -0.4px;
}
.book-meta{
  color: #6b7684;
  font-size: 1rem;
  margin-bottom: 18px;
  display:flex;
  justify-content:center;
  flex-wrap: wrap;
  gap: 6px;
}
.dot{ opacity: 0.6; }

.action-row{
  display:flex;
  gap: 10px;
  justify-content:center;
  margin-bottom: 14px;
}

.btn-primary{
  background: var(--primary, #00d15b);
  color: white;
  padding: 12px 22px;
  border-radius: 16px;
  font-weight: 600;
  transition: 0.18s;
}
.btn-primary:hover{
  transform: translateY(-2px);
  box-shadow: 0 10px 18px rgba(0,209,91,0.18);
}

.btn-secondary{
  background: white;
  color: var(--text, #191f28);
  padding: 12px 18px;
  border-radius: 16px;
  border: 1px solid rgba(0,0,0,0.10);
  font-weight: 600;
  transition: 0.18s;
}
.btn-secondary:hover{ border-color: rgba(0,0,0,0.18); }
.btn-secondary:disabled{ opacity: 0.6; cursor:not-allowed; }

.ai-section{
  background: rgba(255,255,255,0.94);
  border-radius: 20px;
  padding: 22px;
  margin-bottom: 16px;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 6px 16px rgba(0,0,0,0.03);
  backdrop-filter: blur(14px);
}

.ai-header{
  display:flex;
  align-items:center;
  gap: 8px;
  font-weight: 800;
  font-size: 1.05rem;
  margin-bottom: 14px;
  color: var(--primary, #00d15b);
}

.summary-box{
  background: #f9fafb;
  padding: 14px;
  border-radius: 12px;
  font-size: 0.95rem;
  line-height: 1.65;
  color: #4e5968;
  margin-bottom: 10px;
  border: 1px solid rgba(0,0,0,0.04);
}

.keyword-row{
  display:flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 10px;
}
.keyword{
  background: rgba(0,209,91,0.10);
  color: #0b7a34;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 600;
}

.recommend-list{ padding: 0; margin: 0; }
.recommend-list li{
  display:flex;
  gap: 8px;
  align-items:flex-start;
  margin-bottom: 8px;
  font-size: 0.95rem;
  color: #333;
}
.check{ color: #0b7a34; }
.txt{ line-height: 1.5; }

.reaction-card{
  background: #f2f4f6;
  padding: 12px 14px;
  border-radius: 12px;
  margin-bottom: 8px;
  font-size: 0.92rem;
  color: #555;
  border: 1px solid rgba(0,0,0,0.04);
}

.author-box{
  display:flex;
  gap: 14px;
  align-items:flex-start;
}
.author-img{
  width: 62px;
  height: 62px;
  border-radius: 50%;
  object-fit: cover;
  background: #e5e8eb;
  border: 1px solid rgba(0,0,0,0.06);
  flex: 0 0 auto;
}
.author-img.ph{ display:block; }
.author-meta{ min-width:0; }
.author-name{ font-weight: 800; }
.author-info{
  margin-top: 6px;
  font-size: 0.88rem;
  color: #4e5968;
  line-height: 1.55;
  white-space: pre-line;
}
.more-toggle{
  margin-top: 8px;
  color: #0b7a34;
  font-weight: 600;
}

.ai-error{
  color: #ff4040;
  font-size: 0.92rem;
  font-weight: 600;
}
.empty{
  color: #8b95a1;
  font-size: 0.92rem;
  font-weight: 500;
}

/* RIGHT */
.review-side h2{
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 14px;
  letter-spacing: -0.3px;
}
.r-empty{
  background: rgba(255,255,255,0.9);
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 20px;
  padding: 22px;
  color: #6b7684;
}

/* Skeletons */
.hero-skeleton{ text-align:center; margin-bottom: 18px; }
.sk-cover{
  width: 220px; height: 320px;
  margin: 0 auto 16px;
  border-radius: 12px;
  background: linear-gradient(90deg, #e9edf1, #f6f8fa, #e9edf1);
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite;
}
.sk-line{
  height: 14px;
  margin: 10px auto;
  border-radius: 999px;
  background: linear-gradient(90deg, #e9edf1, #f6f8fa, #e9edf1);
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite;
}
.w80{ width: 80%; }
.w60{ width: 60%; }
.w90{ width: 90%; }
.w85{ width: 85%; }

.sk-actions{
  width: 90%;
  height: 44px;
  margin: 14px auto 0;
  border-radius: 16px;
  background: linear-gradient(90deg, #e9edf1, #f6f8fa, #e9edf1);
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite;
}
.ai-skeleton .sk-box,
.ai-skeleton .sk-card,
.ai-skeleton .sk-author{
  border-radius: 12px;
  background: linear-gradient(90deg, #e9edf1, #f6f8fa, #e9edf1);
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite;
  border: 1px solid rgba(0,0,0,0.04);
}
.ai-skeleton .sk-box{ height: 74px; margin-bottom: 10px; }
.ai-skeleton .sk-card{ height: 56px; margin-bottom: 10px; }
.ai-skeleton .sk-author{ height: 96px; }

@keyframes shimmer{
  0%{ background-position: 0% 0; }
  100%{ background-position: -200% 0; }
}

@media (max-width: 900px){
  .container{ grid-template-columns: 1fr; }
  .sticky-side{ position: static; max-height: none; overflow: visible; padding-right: 0; }
}
</style>
