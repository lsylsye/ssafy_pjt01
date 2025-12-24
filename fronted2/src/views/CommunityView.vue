<template>
  <div class="page">
    <div class="container" style="margin-top: 20px">
      <div class="top">
        <h1 class="title">커뮤니티 🌲</h1>
        <button class="btn-write" type="button" @click="goWrite">✏️ 글쓰기</button>
      </div>

      <!-- 말머리(탭) -->
      <div class="tab-menu" role="tablist" aria-label="prefix tabs">
        <button
          class="tab-btn"
          :class="selectedPrefix === '' ? 'active' : 'inactive'"
          type="button"
          @click="selectPrefix('')"
        >
          전체
        </button>

        <button
          v-for="p in FREE_PREFIXES"
          :key="p.value"
          class="tab-btn"
          :class="selectedPrefix === p.value ? 'active' : 'inactive'"
          type="button"
          @click="selectPrefix(p.value)"
        >
          {{ p.icon }} {{ p.value }}
        </button>
      </div>

      <!-- 검색 -->
      <div class="search-row">
        <input
          v-model="q"
          class="search-input"
          type="text"
          placeholder="제목/내용 검색"
          @keydown.enter="fetchList"
        />
        <button class="search-btn" type="button" @click="fetchList">검색</button>
        <button class="ghost-btn" type="button" @click="resetFilters">초기화</button>
      </div>

      <!-- 상태 -->
      <div v-if="loading" class="state">불러오는 중...</div>
      <div v-else-if="error" class="state error">{{ error }}</div>
      <div v-else-if="posts.length === 0" class="state">게시글이 없습니다.</div>

      <!-- 리스트 -->
      <div v-else class="list">
        <div
          v-for="post in posts"
          :key="post.id"
          class="glass-panel"
          role="button"
          tabindex="0"
          @click="goDetail(post.id)"
          @keydown.enter="goDetail(post.id)"
        >
          <div class="row1">
            <span class="badge free">
              {{ iconOf(post.prefix_name) }} {{ normalizedPrefix(post.prefix_name) }}
            </span>
            <span class="time">{{ fromNow(post.created_at) }}</span>
          </div>

          <h3 class="post-title">{{ post.title }}</h3>

          <p class="post-content">
            {{ post.content }}
          </p>

          <div class="meta">
            <span>❤️ {{ post.like_count }}</span>
            <span>💬 {{ post.comment_count }}</span>
            <span>by {{ post.user_nickname }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { getFreePosts } from "@/api/community";
import { FREE_PREFIXES } from "@/constants/freePrefixes";

const router = useRouter();

const loading = ref(false);
const error = ref("");
const posts = ref([]);

const selectedPrefix = ref(""); // "" = 전체
const q = ref("");

function normalizedPrefix(name) {
  // 서버에 옛 데이터(잡담/경제)가 있을 수 있어서 안전하게 표시
  if (!name) return "자유게시판";
  return String(name);
}

function iconOf(prefixName) {
  const hit = FREE_PREFIXES.find((p) => p.value === prefixName);
  return hit?.icon || "💬";
}

function fromNow(iso) {
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
  } catch {
    return "";
  }
}

async function fetchList() {
  loading.value = true;
  error.value = "";
  try {
    const res = await getFreePosts({
      q: q.value.trim(),
      prefix: selectedPrefix.value,
    });
    posts.value = Array.isArray(res.data) ? res.data : [];
  } catch (e) {
    console.error("[free list fail]", e?.response?.status, e?.response?.data || e?.message);
    error.value = "게시글을 불러오지 못했습니다.";
    posts.value = [];
  } finally {
    loading.value = false;
  }
}

function selectPrefix(prefix) {
  selectedPrefix.value = prefix;
  fetchList(); // ✅ 비동기 필터링(새로고침 없음)
}

function resetFilters() {
  q.value = "";
  selectedPrefix.value = "";
  fetchList();
}

function goDetail(id) {
  // 네 라우트 구조에 맞게 바꿔도 됨
  router.push(`/community/free/${id}`);
}

function goWrite() {
  router.push("/community/free/write");
}

onMounted(fetchList);
</script>

<style scoped>
:root{
  --primary:#00D15B;
  --bg:#F2F4F6;
  --text:#191F28;
  --glass: rgba(255,255,255,0.72);
}

.page{
  min-height: calc(100vh - 70px);
  background: var(--bg);
  color: var(--text);
  font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.container{
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.top{
  display:flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 18px;
}

.title{
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.4px;
}

.btn-write{
  background: var(--primary);
  color: white;
  border: none;
  padding: 12px 22px;
  border-radius: 12px;
  font-weight: 800;
  cursor: pointer;
  transition: 0.15s;
}
.btn-write:hover{
  transform: translateY(-1px);
  box-shadow: 0 10px 18px rgba(0,0,0,0.08);
}

.tab-menu{
  display:flex;
  gap:10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.tab-btn{
  padding: 9px 14px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  font-size: 0.98rem;
  font-weight: 600;
  transition: 0.15s;
}
.tab-btn.active{
  background: #191F28;
  color: white;
}
.tab-btn.inactive{
  background: rgba(0,0,0,0.05);
  color: #8B95A1;
}
.tab-btn:hover{ transform: translateY(-1px); }

.search-row{
  display:flex;
  gap:10px;
  align-items:center;
  margin-bottom: 18px;
}

.search-input{
  flex: 1;
  height: 40px;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.08);
  padding: 0 12px;
  background: rgba(255,255,255,0.8);
  outline: none;
}
.search-input:focus{
  border-color: rgba(0,209,91,0.45);
  box-shadow: 0 0 0 3px rgba(0,209,91,0.12);
}

.search-btn{
  height: 40px;
  padding: 0 14px;
  border-radius: 12px;
  border: none;
  background: #191F28;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.ghost-btn{
  height: 40px;
  padding: 0 14px;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.10);
  background: rgba(255,255,255,0.8);
  color: #4E5968;
  font-weight: 600;
  cursor: pointer;
}

.state{
  padding: 20px 4px;
  color: #6B7684;
  font-weight: 600;
}
.state.error{ color: #EF4444; }

.glass-panel{
  background: var(--glass);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 14px;
  border: 1px solid rgba(255,255,255,0.9);
  transition: 0.18s;
  cursor: pointer;
}
.glass-panel:hover{
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.06);
  background: white;
}

.row1{
  display:flex;
  align-items:center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.badge{
  padding: 5px 10px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
}
.badge.free{
  background: rgba(0, 209, 91, 0.12);
  color: #067A35;
  border: 1px solid rgba(0, 209, 91, 0.25);
}

.time{
  color: #8B95A1;
  font-size: 0.9rem;
  font-weight: 600;
}

.post-title{
  font-size: 1.2rem;
  margin-bottom: 8px;
  font-weight: 800;
  letter-spacing: -0.2px;
}

.post-content{
  color: #555;
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta{
  display:flex;
  gap: 12px;
  color: #8B95A1;
  font-size: 0.9rem;
  margin-top: 12px;
  font-weight: 600;
}
</style>
