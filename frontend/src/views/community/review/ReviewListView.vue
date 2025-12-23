<template>
  <section>
    <div class="filters">
      <input v-model="q" class="input" placeholder="검색(책제목/저자/리뷰내용)" />
      <button class="btn" :disabled="loading" @click="search">검색</button>
    </div>

    <p v-if="loading">불러오는 중...</p>
    <p v-else-if="errorMsg" class="error">{{ errorMsg }}</p>

    <div v-else>
      <p v-if="reviews.length === 0">게시글이 없습니다.</p>

      <ul v-else class="list">
        <ReviewCard
          v-for="r in reviews"
          :key="r.id"
          :review="r"
          :to="`/community/${country}/review/${r.id}`"
        />
      </ul>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { storeToRefs } from "pinia";
import useCountry from "@/composables/useCountry";
import { useReviewStore } from "@/stores/community/review";
import ReviewCard from "@/components/community/review/ReviewCard.vue";

const { country } = useCountry();
const store = useReviewStore();
const { loading, errorMsg, reviews } = storeToRefs(store);

const q = ref("");

const fetch = () => {
  store.fetchList(country.value, {
    q: q.value.trim() || undefined,
  });
};
const search = () => fetch();

onMounted(fetch);

watch(
  () => country.value,
  () => {
    q.value = "";
    fetch();
  }
);
</script>

<style scoped>
.page {
  padding: 32px;
  background: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 28px;
  align-items: center;
  flex-wrap: wrap;
}

.input {
  flex: 1;
  min-width: 200px;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: var(--text-primary);
  background: #ffffff;
  transition: var(--transition);
}

.input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.btn {
  border: 1px solid var(--border-color);
  background: #ffffff;
  border-radius: 8px;
  padding: 12px 20px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  transition: var(--transition);
  box-shadow: none;
}

.btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background: #ffffff;
}

.error {
  color: #dc2626;
  font-size: 14px;
  font-weight: 600;
  padding: 12px;
  background: #fee2e2;
  border-radius: 8px;
  margin-bottom: 16px;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (max-width: 640px) {
  .page {
    padding: 20px 16px;
  }

  .filters {
    flex-direction: column;
  }

  .input {
    min-width: auto;
  }
}
</style>
