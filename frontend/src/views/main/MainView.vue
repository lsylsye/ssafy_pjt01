<!-- src/views/main/MainView.vue -->
<template>
  <section class="main">
    <h2 class="section-title">베스트셀러 TOP 10</h2>

    <ul class="bestseller-list">
      <li v-for="book in top10" :key="book.id" class="bestseller-item">
        <router-link :to="`/books/${book.isbn13}`" class="bestseller-link">
          <span class="rank">{{ book.best_rank }}</span>
          <img :src="book.cover" alt="표지" class="cover" />
          <span class="book-title">{{ book.title }}</span>
        </router-link>
      </li>
    </ul>

    <!-- ✅ 주목할 만한 신간 5권(가로 스크롤) -->
    <NewSpecialSection />

    <!-- ✅ 추천 시스템1(작가버전): 신간 아래에 추가 -->
    <RecommendBookmarkSection />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import api from "@/api/axios";
import NewSpecialSection from "@/components/books/NewSpecialSection.vue";
import RecommendBookmarkSection from "@/components/home/RecommendBookmarkSection.vue";

const bestsellers = ref([]);

const fetchBestsellers = () => {
  api
    .get("/api/books/bestsellers/", { auth: false })
    .then((res) => {
      bestsellers.value = Array.isArray(res.data) ? res.data : [];
    })
    .catch((err) => {
      console.error(err);
    });
};

const top10 = computed(() => bestsellers.value.slice(0, 10));

onMounted(() => {
  fetchBestsellers();
});
</script>

<style scoped>
.main {
  padding: 24px;
}

.section-title {
  margin: 0 0 18px;
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -0.5px;
  line-height: 1.1;
  color: #111;
}

.bestseller-list {
  list-style: none;
  padding: 0;
  margin: 0;

  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px 24px;
}

.bestseller-item {
  border: 1px solid #eee;
  border-radius: 6px;
}

.bestseller-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;

  text-decoration: none;
  color: inherit;
}

.rank {
  font-weight: bold;
  color: #e53935;
  width: 20px;
}

.cover {
  width: 50px;
  height: auto;
}

.book-title {
  font-size: 15px;
}

.bestseller-link:hover {
  background-color: #f5f7fa;
}
</style>
