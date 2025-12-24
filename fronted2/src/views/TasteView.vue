<!-- src/views/TasteView.vue -->
<template>
  <div class="page">
    <div class="container">
      <!-- 취향 테스트 배너 -->
      <section class="test-banner">
        <div class="banner-deco"></div>

        <div class="banner-text">
          <h1 class="banner-title">내 독서 취향은 무슨 색일까요?</h1>
          <p class="banner-desc">간단한 테스트로 나만의 독서 DNA를 찾아보세요.</p>
        </div>

        <button class="btn-test" type="button" @click="goTasteTest">
          테스트 시작하기 &gt;
        </button>
      </section>

       <!-- 알고리즘 1: 북마크 기반 -->
      <section class="algo-section">
        <div class="algo-header">
          <div>
            <div class="algo-title">
              {{ nicknameForTitle }} {{ pickedAuthorLabel }} 작가님 어떠세요? 🔭
            </div>
            <div class="algo-subtitle">북마크 기록을 기반으로 분석했어요.</div>
          </div>

          <button
            class="btn-refresh"
            type="button"
            :disabled="loadingBookmark"
            @click="refreshBookmark"
          >
            <span class="refresh-icon" :class="{ spinning: loadingBookmark }">🔄</span>
            <span>새로고침</span>
          </button>
        </div>

        <div v-if="errorBookmark" class="error">{{ errorBookmark }}</div>

        <div class="book-scroller" v-else>
          <template v-if="loadingBookmark">
            <div v-for="i in 6" :key="'sk-bm-' + i" class="book-card skeleton">
              <div class="cover sk"></div>
              <div class="b-title skline"></div>
              <div class="b-author skline sm"></div>
            </div>
          </template>

          <template v-else>
            <div
              v-for="b in bookmarkBooks"
              :key="'bm-' + (b.isbn13 || b.id || b.title)"
              class="book-card"
              role="button"
              tabindex="0"
              @click="goBook(b)"
              @keydown.enter="goBook(b)"
            >
              <img class="cover img" :src="b.cover" :alt="b.title" v-if="b.cover" />
              <div class="cover" v-else></div>

              <div class="b-title" :title="b.title">{{ b.title || "제목 없음" }}</div>
              <div class="b-author" :title="b.author">{{ b.author || "-" }}</div>
            </div>

            <div v-if="!bookmarkBooks.length" class="empty">
              아직 추천할 데이터가 부족해요. 북마크를 조금 더 추가해보세요 🌱
            </div>
          </template>
        </div>
      </section>

      <!-- 알고리즘 2: 팔로우 기반 -->
      <section class="algo-section">
        <div class="algo-header">
          <div>
            <div class="algo-title">함께 읽어볼까요? 🌿</div>
            <div class="algo-subtitle">팔로워들이 최근 가장 많이 심은 책들이에요.</div>
          </div>

          <button
            class="btn-refresh"
            type="button"
            :disabled="loadingFollow"
            @click="refreshFollow"
            aria-label="refresh follow recommendation"
          >
            <span class="refresh-icon" :class="{ spinning: loadingFollow }">🔄</span>
            <span>새로고침</span>
          </button>
        </div>

        <div v-if="errorFollow" class="error">{{ errorFollow }}</div>

        <div class="book-scroller" v-else>
          <template v-if="loadingFollow">
            <div v-for="i in 6" :key="'sk-fw-' + i" class="book-card skeleton">
              <div class="cover sk"></div>
              <div class="b-title skline"></div>
              <div class="b-author skline sm"></div>
            </div>
          </template>

          <template v-else>
            <div
              v-for="b in followBooks"
              :key="'fw-' + (b.isbn13 || b.id || b.title)"
              class="book-card"
              role="button"
              tabindex="0"
              @click="goBook(b)"
              @keydown.enter="goBook(b)"
            >
              <img class="cover img" :src="b.cover" :alt="b.title" v-if="b.cover" />
              <div class="cover" v-else style="background:#fafafa;border:1px solid #eee;"></div>

              <div class="b-title" :title="b.title">{{ b.title || "제목 없음" }}</div>
              <div class="b-author" :title="b.author">{{ b.author || "-" }}</div>
            </div>

            <div v-if="!followBooks.length" class="empty">
              아직 팔로우 기반 추천이 준비되지 않았어요. 팔로우를 늘려보세요 🌿
            </div>
          </template>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";

const router = useRouter();

const me = ref(null);
const isLoggedIn = computed(() => !!localStorage.getItem("access_token"));
const nicknameForTitle = computed(() => (me.value?.nickname ? `${me.value.nickname}님,` : ""));

const bookmarkBooks = ref([]);
const followBooks = ref([]);

const loadingBookmark = ref(false);
const loadingFollow = ref(false);

const errorBookmark = ref("");
const errorFollow = ref("");

// ✅ 북마크 추천 타이틀용 picked_author
const pickedAuthor = ref("");
const pickedAuthorLabel = computed(() => pickedAuthor.value || "추천 작가");

function cleanAuthorName(s) {
  if (!s) return "";
  // "데니스 존슨 (지은이), 박아람 (옮긴이)" -> "데니스 존슨"
  const first = String(s).split(",")[0].trim();
  return first.replace(/\s*\(.*?\)\s*/g, "").trim();
}

function normalizeItems(items) {
  const arr = Array.isArray(items) ? items : [];
  return arr.map((x) => ({
    id: x.id,
    isbn13: x.isbn13,
    title: x.title,
    author: x.author,
    cover: x.cover,
  }));
}

async function fetchMe() {
  if (!isLoggedIn.value) return;
  try {
    // baseURL이 /api 라면 => /api/mypage/me/
    const res = await api.get("mypage/me/");
    me.value = res.data || null;
  } catch {
    me.value = null;
  }
}

async function refreshBookmark() {
  if (loadingBookmark.value) return;
  loadingBookmark.value = true;
  errorBookmark.value = "";

  try {
    // ❗ baseURL이 /api면 "/api/books..."로 쓰면 /api/api/books...가 됨
    const res = await api.get("books/recommend/bookmark/");
    const data = res.data || {};

    // ✅ picked_author 반영
    pickedAuthor.value = cleanAuthorName(data.picked_author);

    // ✅ items 반영
    bookmarkBooks.value = normalizeItems(data.items);
  } catch (e) {
    console.error("[bookmark recommend fail]", e);
    errorBookmark.value = "추천을 불러오지 못했습니다.";
    pickedAuthor.value = "";
    bookmarkBooks.value = [];
  } finally {
    loadingBookmark.value = false;
  }
}

async function refreshFollow() {
  if (loadingFollow.value) return;
  loadingFollow.value = true;
  errorFollow.value = "";

  try {
    const res = await api.get("books/recommend/follow/");
    // 팔로우 응답이 배열이면 그대로, {items:[...]}면 items 사용
    const data = res.data;
    const items = Array.isArray(data) ? data : data?.items;
    followBooks.value = normalizeItems(items);
  } catch (e) {
    console.error("[follow recommend fail]", e);
    errorFollow.value = "추천을 불러오지 못했습니다.";
    followBooks.value = [];
  } finally {
    loadingFollow.value = false;
  }
}

function goBook(b) {
  const isbn13 = b?.isbn13;
  if (!isbn13) return;
  router.push(`/books/${isbn13}`);
}

function goTasteTest() {
  router.push("/taste/test");
}

onMounted(async () => {
  await fetchMe();
  refreshBookmark();
  refreshFollow();
});
</script>

<style scoped>
:root{
  --primary:#00d15b;
  --bg:#fafafa;
  --text:#191f28;
}

.page{
  background: var(--bg);
  min-height: calc(100vh - 70px);
}
.container{
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* 1. 취향 테스트 배너 */
.test-banner{
  background: linear-gradient(120deg, #191f28 0%, #2b3340 100%);
  border-radius: 24px;
  padding: 50px;
  color: #fff;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 60px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}
.banner-deco{
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
  top: -50%;
  right: -10%;
  opacity: 0.28;
  filter: blur(50px);
}
.banner-text{ position: relative; z-index: 1; }
.banner-title{
  margin: 0 0 10px 0;
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.5px;
}
.banner-desc{
  margin: 0;
  opacity: 0.82;
  font-size: 1rem;
  font-weight: 500;
}
.btn-test{
  position: relative;
  z-index: 1;
  background: var(--primary);
  color: #fff;
  padding: 14px 30px;
  border-radius: 30px;
  border: none;
  font-weight: 600; /* 700 지양 */
  font-size: 1.05rem;
  cursor: pointer;
  transition: 0.18s;
}
.btn-test:hover{
  transform: scale(1.04);
  box-shadow: 0 0 20px rgba(0, 209, 91, 0.35);
}

/* 2. 알고리즘 섹션 */
.algo-section{ margin-bottom: 60px; }
.algo-header{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 20px;
}
.algo-title{
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.4px;
}
.algo-subtitle{
  font-size: 1rem;
  color: #666;
  margin-top: 6px;
  font-weight: 500;
}
.btn-refresh{
  border: 1px solid #ddd;
  background: #fff;
  padding: 10px 14px;
  border-radius: 999px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #555;
  transition: 0.18s;
  user-select: none;
}
.btn-refresh:hover{ background: #f5f5f5; }
.btn-refresh:disabled{
  opacity: 0.6;
  cursor: not-allowed;
}
.refresh-icon{
  display: inline-block;
  transition: transform 0.18s;
}
.refresh-icon.spinning{
  animation: spin 0.8s linear infinite;
}
@keyframes spin{
  from{ transform: rotate(0deg); }
  to{ transform: rotate(360deg); }
}

/* 책 가로 스크롤 */
.book-scroller{
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding-bottom: 20px;
  scroll-behavior: smooth;
}
.book-scroller::-webkit-scrollbar{ height: 6px; }
.book-scroller::-webkit-scrollbar-thumb{
  background: #ddd;
  border-radius: 10px;
}

.book-card{
  min-width: 160px;
  cursor: pointer;
  transition: 0.18s;
}
.book-card:hover{ transform: translateY(-5px); }

.cover{
  width: 100%;
  height: 230px;
  background: #eee;
  border-radius: 12px;
  margin-bottom: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.10);
}
.cover.img{
  object-fit: cover;
  display: block;
}

.b-title{
  font-weight: 600; /* 700 지양 */
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.b-author{
  font-size: 0.9rem;
  color: #888;
  font-weight: 500;
}

.empty{
  padding: 14px 2px;
  color: #777;
  font-weight: 500;
}

/* 오류 */
.error{
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(255,64,64,0.08);
  border: 1px solid rgba(255,64,64,0.18);
  color: #c53030;
  font-weight: 600;
}

/* 스켈레톤 */
.skeleton{ cursor: default; }
.skeleton:hover{ transform: none; }
.sk{
  background: linear-gradient(90deg, #eee, #f5f5f5, #eee);
  background-size: 200% 100%;
  animation: shimmer 1.1s ease-in-out infinite;
}
.skline{
  height: 14px;
  border-radius: 8px;
  margin: 6px 0;
}
.skline.sm{ width: 70%; height: 12px; }
@keyframes shimmer{
  0%{ background-position: 200% 0; }
  100%{ background-position: -200% 0; }
}
</style>
