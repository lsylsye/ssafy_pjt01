<!-- src/components/ui/SearchCapsule.vue -->
<template>
  <div class="wrap" ref="wrapRef">
    <div class="search-capsule" :class="{ open: open }">
      <input
        v-model="q"
        class="search-input"
        placeholder="검색"
        @focus="onFocus"
        @keydown.escape.prevent="close"
        @keydown.enter.prevent="goSearch"
      />
      <button class="search-btn" type="button" @click="goSearch" aria-label="search">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </button>
    </div>

    <div v-if="showDropdown" class="dropdown" role="listbox">
      <div v-if="books.searchLoading" class="state">검색 중…</div>
      <div v-else-if="books.searchError" class="state error">{{ books.searchError }}</div>

      <template v-else-if="books.searchResults.length">
        <button
          v-for="b in books.searchResults.slice(0, 8)"
          :key="b.isbn13 || b.title"
          class="item"
          type="button"
          :disabled="!b.isbn13"
          :class="{ disabled: !b.isbn13 }"
          @click="pick(b)"
        >
          <div class="thumb">
            <img v-if="b.cover" :src="b.cover" alt="" />
            <div v-else class="ph">Cover</div>
          </div>

          <div class="meta">
            <div class="t" :title="b.title">{{ b.title }}</div>
            <div class="s" :title="b.author">{{ b.author || "-" }}</div>
            <div class="x">
              <span class="p">{{ b.publisher || "-" }}</span>
              <span class="dot">·</span>
              <span class="d">{{ b.pub_date || "-" }}</span>
              <span v-if="!b.isbn13" class="badge">ISBN 없음</span>
            </div>
          </div>

          <div class="chev">›</div>
        </button>

        <!-- ✅ 전체 결과 보기 -->
        <button class="more" type="button" @click="goSearch">
          전체 결과 보기
          <span class="arrow">→</span>
        </button>
      </template>

      <div v-else class="state">검색 결과가 없어요.</div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useBooksStore } from "@/stores/books.store";

const router = useRouter();
const books = useBooksStore();

const q = ref("");
const open = ref(false);
const wrapRef = ref(null);

const trimmed = computed(() => (q.value || "").trim());

// ✅ 드롭다운: open 상태에서 로딩/에러/결과 있을 때 보여줌
const showDropdown = computed(() => {
  if (!open.value) return false;
  if (books.searchLoading) return true;
  if (books.searchError) return true;
  return !!(books.searchResults && books.searchResults.length);
});

let timer = null;

function onFocus() {
  open.value = true;

  // 포커스 시에도 (2글자 이상이면) 최신 결과 보이게
  const t = trimmed.value;
  if (t.length >= 2) books.search(t);
}

function close() {
  open.value = false;
}

/**
 * ✅ 전체 결과 보기 이동 로직 (수정된 부분)
 * - 이동 전에 store에 한번 검색 호출(선택)
 * - /search?q=검색어 로 라우팅
 * - 드롭다운 닫기
 */
function goSearch() {
  const t = trimmed.value;
  if (!t) return;

  // ✅ SearchView 들어가자마자 결과가 보이도록 선검색(필요 없으면 이 줄 삭제해도 됨)
  if (t.length >= 2) books.search(t);

  close();
  router.push({ path: "/search", query: { q: t } });
}

// 드롭다운에서 책 클릭 시 동작
function pick(b) {
  if (!b || !b.isbn13) return;

  close();
  q.value = "";

  // ✅ 책 상세 페이지로 이동
  router.push(`/books/${encodeURIComponent(b.isbn13)}`);
}

function onDocClick(e) {
  const el = wrapRef.value;
  if (!el) return;
  if (!el.contains(e.target)) close();
}

watch(
  trimmed,
  (v) => {
    if (timer) clearTimeout(timer);

    // 0~1글자는 검색 안 함
    if (v.length < 2) {
      // books.clearSearch?.();
      return;
    }

    timer = setTimeout(() => {
      books.search(v);
      open.value = true;
    }, 250);
  },
  { immediate: false }
);

onMounted(() => document.addEventListener("click", onDocClick));
onBeforeUnmount(() => {
  document.removeEventListener("click", onDocClick);
  if (timer) clearTimeout(timer);
});
</script>

<style scoped>
.wrap{ position:relative; }

.search-capsule{
  position:relative;
  width:180px;
  height:40px;
  background:#f2f4f6;
  border-radius:999px;
  display:flex;
  align-items:center;
  transition:0.35s cubic-bezier(0.25,0.8,0.25,1);
  border:1px solid transparent;
}
.search-capsule:focus-within,
.search-capsule.open{
  width:240px;
  background:#fff;
  border-color:var(--primary);
  box-shadow:0 4px 12px rgba(0,209,91,0.10);
}

.search-input{
  width:100%;
  height:100%;
  border:none;
  background:transparent;
  padding:0 10px 0 18px;
  font-size:0.9rem;
  outline:none;
  color:#333;
}
.search-input::placeholder{ color:#adb5bd; }

.search-btn{
  padding:0 12px 0 0;
  color:#8b95a1;
  display:flex;
  align-items:center;
}
.search-capsule:focus-within .search-btn,
.search-capsule.open .search-btn{
  color:var(--primary);
}

.dropdown{
  position:absolute;
  top:48px;
  right:0;
  width:min(420px, 92vw);
  background: rgba(255,255,255,0.92);
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 16px;
  box-shadow: 0 18px 50px rgba(0,0,0,0.12);
  backdrop-filter: blur(18px);
  padding: 8px;
  z-index: 200;
}

.item{
  width:100%;
  display:flex;
  gap:12px;
  padding:10px 10px;
  border-radius: 14px;
  text-align:left;
  transition:0.16s;
  align-items:center;
}
.item:hover{ background:#f2f4f6; }
.item.disabled{ opacity:0.55; cursor:not-allowed; }
.item.disabled:hover{ background: transparent; }

.thumb{
  width:40px;
  height:54px;
  border-radius:12px;
  overflow:hidden;
  border:1px solid rgba(0,0,0,0.06);
  background:#fff;
  flex: 0 0 auto;
  display:flex;
  align-items:center;
  justify-content:center;
  box-shadow: 0 8px 18px rgba(0,0,0,0.08);
}
.thumb img{ width:100%; height:100%; object-fit:cover; }
.ph{ font-weight: 950; color:#94a3b8; font-size:0.78rem; }

.meta{ min-width:0; flex:1; }
.t{
  font-weight: 950;
  font-size: 0.94rem;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  letter-spacing:-0.2px;
}
.s{
  font-size:0.82rem;
  color:var(--text-sub);
  margin-top:3px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  font-weight: 800;
}
.x{
  margin-top:4px;
  display:flex;
  align-items:center;
  gap:6px;
  color:#94a3b8;
  font-size:0.78rem;
  font-weight: 800;
  min-width:0;
}
.p,.d{ white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width: 45%; }
.dot{ opacity:0.6; }

.badge{
  margin-left:6px;
  padding:2px 8px;
  border-radius:999px;
  background: rgba(255,64,64,0.12);
  color:#ff4040;
  font-weight: 950;
  font-size:0.74rem;
}

.chev{
  color:#94a3b8;
  font-weight: 950;
  font-size: 1.2rem;
  padding: 0 6px;
}

.more{
  width:100%;
  margin-top:6px;
  height:40px;
  border-radius: 12px;
  font-weight: 950;
  background: rgba(0,209,91,0.10);
  color: #0b7a34;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:8px;
}
.more:hover{ background: rgba(0,209,91,0.14); }
.arrow{ font-weight: 950; }

.state{
  padding:12px 10px;
  color:var(--text-sub);
  font-weight: 800;
}
.state.error{ color:#ff4040; }
</style>
