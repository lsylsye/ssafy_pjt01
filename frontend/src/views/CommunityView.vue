<template>
  <div class="page">
    <div class="container">
      <!-- 헤더: 타이틀 + 글쓰기 -->
      <div class="header-row">
        <h1 class="title">커뮤니티 🌲</h1>
        <button class="write-btn" @click="goWrite">
          <PenLine :size="16" />
          글쓰기
        </button>
      </div>

      <!-- 카테고리 필터 (슬림한 칩) -->
      <div class="filter-row">
        <button
          class="chip"
          :class="{ active: selectedPrefix === '' }"
          @click="selectPrefix('')"
        >
          전체
        </button>
        <button
          v-for="p in FREE_PREFIXES"
          :key="p.value"
          class="chip"
          :class="{ active: selectedPrefix === p.value }"
          @click="selectPrefix(p.value)"
        >
          {{ p.value }}
        </button>
      </div>

      <!-- 검색 영역 (높이 축소) -->
      <div class="search-section">
        <div class="search-bar">
          <input
            v-model="q"
            type="text"
            placeholder="검색어를 입력하세요"
            @keydown.enter="fetchList"
          />
          <button class="search-btn" @click="fetchList">검색</button>
          <button class="reset-btn" @click="resetFilters">초기화</button>
        </div>
      </div>

      <div v-if="loading" class="state-view">불러오는 중...</div>
      <div v-else-if="error" class="state-view error">{{ error }}</div>
      <div v-else-if="posts.length === 0" class="state-view">글이 아직 없습니다. 🌱</div>

      <!-- 압축된 게시글 리스트 -->
      <div v-else class="post-list">
        <div
          v-for="post in posts"
          :key="post.id"
          class="post-card"
          @click="goDetail(post.id)"
        >
          <div class="card-left">
            <div class="card-main-row">
              <span class="prefix-tag" :class="getPrefixClass(post.prefix_name)">
                {{ post.prefix_name || '자유' }}
              </span>
              <h3 class="post-title">{{ post.title }}</h3>
            </div>
            <div class="card-sub-row">
              <p class="post-summary">{{ post.content }}</p>
              <span class="post-meta-mini">{{ post.user_nickname }} · {{ fromNow(post.created_at) }}</span>
            </div>
          </div>

          <div class="card-right">
            <div class="meta-item" :class="{ liked: post.liked }">
              <Heart :size="13" :fill="post.liked ? 'currentColor' : 'none'" />
              <span>{{ post.like_count }}</span>
            </div>
            <div class="meta-item">
              <MessageCircle :size="13" />
              <span>{{ post.comment_count }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 페이지네이션 -->
      <div v-if="totalPages > 1" class="pagination">
        <button 
          class="pg-btn" 
          :disabled="!prev"
          @click="changePage(currentPage - 1)"
        >
          이전
        </button>
        <span class="pg-info">{{ currentPage }} / {{ totalPages }}</span>
        <button 
          class="pg-btn" 
          :disabled="!next"
          @click="changePage(currentPage + 1)"
        >
          다음
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { getFreePosts } from "@/api/community";
import { FREE_PREFIXES } from "@/constants/freePrefixes";
import { Heart, MessageCircle, PenLine } from 'lucide-vue-next';

const router = useRouter();
const loading = ref(false);
const error = ref("");
const posts = ref([]);
const selectedPrefix = ref("");
const q = ref("");

// Pagination State
const currentPage = ref(1);
const totalPages = ref(1);
const next = ref(null);
const prev = ref(null);

const getPrefixClass = (name) => {
  if (!name) return 'free';
  if (name.includes('후기')) return 'review';
  if (name.includes('질문')) return 'question';
  return 'free';
};

const fromNow = (iso) => {
  try {
    const d = new Date(iso);
    const diff = Date.now() - d.getTime();
    const sec = Math.floor(diff / 1000);
    if (sec < 60) return "방금 전";
    const min = Math.floor(sec / 60);
    if (min < 60) return `${min}분 전`;
    const hr = Math.floor(min / 60);
    if (hr < 24) return `${hr}시간 전`;
    const day = Math.floor(hr / 24);
    return `${day}일 전`;
  } catch { return ""; }
};

async function fetchList(resetPage = false) {
  if (resetPage) currentPage.value = 1;
  
  loading.value = true;
  error.value = "";
  try {
    const res = await getFreePosts({
      q: q.value.trim(),
      prefix: selectedPrefix.value,
      page: currentPage.value,
    });
    
    // DRF Pagination response: { count, next, previous, results }
    const data = res.data;
    if (data.results) {
      posts.value = data.results;
      next.value = data.next;
      prev.value = data.previous;
      totalPages.value = Math.ceil(data.count / 7);
    } else {
      posts.value = Array.isArray(data) ? data : [];
      totalPages.value = 1;
    }
  } catch (e) {
    console.error("[Community List Fail]", e);
    error.value = "게시글을 불러오지 못했습니다.";
  } finally {
    loading.value = false;
  }
}

const changePage = (newPage) => {
  currentPage.value = newPage;
  fetchList();
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const selectPrefix = (prefix) => {
  selectedPrefix.value = prefix;
  fetchList(true);
};

const resetFilters = () => {
  q.value = "";
  selectedPrefix.value = "";
  fetchList(true);
};

const goDetail = (id) => router.push(`/community/free/${id}`);
const goWrite = () => router.push("/community/free/write");

onMounted(fetchList);
</script>

<style scoped>
.page {
  min-height: calc(100vh - 70px);
  padding-bottom: 40px;
}

.container {
  max-width: 840px;
  margin: 0 auto;
  padding: 30px 20px;
}

/* Header */
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #191f28;
}
.write-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #00D15B;
  color: white;
  padding: 8px 16px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.9rem;
  transition: 0.2s;
}
.write-btn:hover {
  background: #00b54f;
  transform: translateY(-1px);
}

/* Chips (More Compact) */
.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 20px;
}
.chip {
  padding: 6px 14px;
  border-radius: 999px;
  background: #f2f4f6;
  color: #8b95a1;
  font-weight: 700;
  font-size: 0.85rem;
}
.chip.active {
  background: #191f28;
  color: white;
}

/* Search Bar (Tighter) */
.search-section {
  margin-bottom: 24px;
}
.search-bar {
  display: flex;
  gap: 8px;
}
.search-bar input {
  flex: 1;
  padding: 10px 16px;
  border-radius: 10px;
  border: 1px solid #e5e8eb;
  background: white;
  font-size: 0.9rem;
  outline: none;
}
.search-btn {
  background: #191f28;
  color: white;
  padding: 0 16px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.9rem;
}
.reset-btn {
  padding: 0 12px;
  border-radius: 10px;
  border: 1px solid #e5e8eb;
  background: white;
  color: #4e5968;
  font-weight: 600;
  font-size: 0.85rem;
}

/* Post List & Ultra Compact Cards */
.post-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.post-card {
  background: white;
  padding: 14px 20px;
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.04);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: 0.2s;
}
.post-card:hover {
  border-color: #00D15B;
  background: #f9fffb;
}

.card-left {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.card-main-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-sub-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.prefix-tag {
  font-size: 0.65rem;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 4px;
  flex-shrink: 0;
}
.prefix-tag.free { background: #e3f2fd; color: #1e88e5; }
.prefix-tag.review { background: #e8f5e9; color: #2e7d32; }
.prefix-tag.question { background: #fff3e0; color: #ef6c00; }

.post-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #191f28;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.post-summary {
  font-size: 0.85rem;
  color: #6b7684;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}
.post-meta-mini {
  font-size: 0.75rem;
  color: #adb5bd;
  font-weight: 500;
  flex-shrink: 0;
}

.card-right {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 20px;
  flex-shrink: 0;
}
.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.85rem;
  color: #b0b8c1;
  font-weight: 600;
}
.meta-item.liked {
  color: #ff4d6d;
}

.state-view {
  text-align: center;
  padding: 40px 0;
  color: #8b95a1;
}

/* Pagination */
.pagination {
  margin-top: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}
.pg-btn {
  padding: 8px 16px;
  border-radius: 8px;
  background: white;
  border: 1px solid #e5e8eb;
  color: #4e5968;
  font-weight: 700;
  font-size: 0.9rem;
  transition: 0.2s;
}
.pg-btn:hover:not(:disabled) {
  background: #f2f4f6;
  border-color: #b0b8c1;
}
.pg-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.pg-info {
  font-size: 0.95rem;
  font-weight: 700;
  color: #191f28;
}
</style>
