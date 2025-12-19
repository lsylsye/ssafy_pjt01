<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api/axios'

const bestsellers = ref([])

const fetchBestsellers = () => {
  api.get('/api/books/bestsellers/')
    .then((res) => {
      bestsellers.value = res.data
    })
    .catch((err) => {
      console.error(err)
    })
}

// TOP 10만 사용
const top10 = computed(() => bestsellers.value.slice(0, 10))

onMounted(() => {
  fetchBestsellers()
})
</script>

<template>
  <section>
    <h2>베스트셀러 TOP 10</h2>

    <ul class="bestseller-list">
      <li
        v-for="book in top10"
        :key="book.id"
        class="bestseller-item"
      >
        <!-- 순위 -->
        <span class="rank">{{ book.best_rank }}</span>

        <!-- 표지 -->
        <img
          :src="book.cover"
          alt="표지"
          class="cover"
        />

        <!-- 제목 -->
        <span class="title">{{ book.title }}</span>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.bestseller-list {
  list-style: none;
  padding: 0;
  margin: 0;

  display: grid;
  grid-template-columns: repeat(2, 1fr); /* ⭐ 한 줄에 2개 */
  gap: 16px 24px; /* 세로 / 가로 간격 */
}

.bestseller-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid #eee;
  border-radius: 6px;
}

.rank {
  font-weight: bold;
  color: #e53935;
}

.cover {
  width: 40px;
  height: auto;
}

.title {
  font-size: 15px;
}

</style>
