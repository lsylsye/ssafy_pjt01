<template>
  <section>
    <div class="filters">
      <input v-model="q" class="input" placeholder="검색(책제목/저자/리뷰내용)" />
      <button class="btn" @click="fetchList" :disabled="loading">검색</button>
    </div>

    <p v-if="loading">불러오는 중...</p>
    <p v-else-if="errorMsg" class="error">{{ errorMsg }}</p>

    <div v-else>
      <p v-if="reviews.length === 0">게시글이 없습니다.</p>

      <ul v-else class="list">
        <li v-for="r in reviews" :key="r.id" class="item">
          <router-link :to="`/community/${country}/review/${r.id}`" class="link">
            <div class="row">
              <span class="title">{{ r.book_title }}</span>
              <span class="author">({{ r.book_author }})</span>
            </div>

            <div class="meta">
              <span>{{ r.user_nickname }}</span>
              <span>· {{ formatDate(r.created_at) }}</span>
              <span>· 평점 {{ r.rating ?? '-' }}</span>
              <span>· 좋아요 {{ r.like_count }}</span>
              <span>· 댓글 {{ r.comment_count }}</span>
            </div>

            <p class="content">{{ r.content }}</p>
          </router-link>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import api from "@/api/axios";

const route = useRoute();
const country = computed(() => String(route.params.country || "kr"));
const apiCountry = (c) => String(c || "kr").toLowerCase();

const loading = ref(false);
const errorMsg = ref("");
const reviews = ref([]);

const q = ref("");

const formatDate = (iso) => (typeof iso === "string" ? iso.slice(0, 10) : "");

const fetchList = () => {
  loading.value = true;
  errorMsg.value = "";
  reviews.value = [];

  const c = apiCountry(country.value);

  api
    .get(`/api/community/${c}/review/`, {
      params: {
        q: q.value.trim() || undefined,
      },
      auth: false, // 비로그인도 가능
    })
    .then((res) => {
      reviews.value = Array.isArray(res.data) ? res.data : [];
    })
    .catch((err) => {
      console.error("[리뷰 목록 실패]", err.response?.status, err.response?.data || err.message);
      errorMsg.value = "리뷰를 불러오지 못했습니다.";
    })
    .finally(() => {
      loading.value = false;
    });
    
};

onMounted(() => {
  fetchList();
});

watch(
  () => country.value,
  () => {
    q.value = "";
    fetchList();
  }
);
</script>

<style scoped>
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
  align-items: center;
}
.input {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.btn {
  border: 1px solid #ddd;
  background: white;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}
.btn:hover { border-color: #1a73e8; color: #1a73e8; }

.error { color: #d33; }

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 12px 14px;
}

.link { text-decoration: none; color: inherit; display: block; }

.row { display: flex; gap: 8px; align-items: center; margin-bottom: 6px; }
.title { font-weight: 800; }
.author { color: #666; font-weight: 600; }

.meta {
  color: #666;
  font-size: 14px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.content {
  margin: 0;
  color: #333;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>
