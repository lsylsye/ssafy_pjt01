<template>
  <section class="main">
    <h2 class="title">베스트셀러 TOP 10</h2>

    <ul class="bestseller-list">
      <li
        v-for="book in top10"
        :key="book.id"
        class="bestseller-item"
      >
        <router-link
          :to="`/books/${book.isbn13}`"
          class="bestseller-link"
        >
          <span class="rank">{{ book.best_rank }}</span>

          <img
            :src="book.cover"
            alt="표지"
            class="cover"
          />

          <span class="book-title">
            {{ book.title }}
          </span>
        </router-link>
      </li>
    </ul>
  </section>
</template>


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

const top10 = computed(() => bestsellers.value.slice(0, 10))

onMounted(() => {
  fetchBestsellers()
})
</script>


<style scoped>
.main {
  padding: 24px;
}

.title {
  margin-bottom: 16px;
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
