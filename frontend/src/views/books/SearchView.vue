<template>
  <section>
    <h1>도서 검색</h1>

    <!-- 검색창 -->
    <div class="search-box">
      <input
        v-model="query"
        placeholder="책 제목을 입력하세요"
        @keyup.enter="searchBooks"
      />
      <button @click="searchBooks">검색</button>
    </div>

    <!-- 검색 결과 -->
    <ul v-if="results.length" class="result-list">
      <li
        v-for="book in results"
        :key="book.isbn13"
        class="result-item"
      >
        <router-link
          :to="`/books/${book.isbn13}`"
          class="result-link"
        >
          <img :src="book.cover" alt="표지" />
          <div>
            <p class="title">{{ book.title }}</p>
            <p class="author">{{ book.author }}</p>
            <p class="publisher">{{ book.publisher }}</p>
          </div>
        </router-link>
      </li>
    </ul>

    <!-- 검색 결과 없음 -->
    <p v-else-if="isSearched">검색 결과가 없습니다.</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/axios'

const query = ref('')
const results = ref([])
const isSearched = ref(false)

const searchBooks = () => {
  if (!query.value.trim()) return

  api.get(`/api/books/search/?q=${query.value}`)
    .then((res) => {
      results.value = res.data.items
      isSearched.value = true
    })
    .catch((err) => {
      console.error(err)
    })
}
</script>

<style scoped>
.search-box {
  margin-bottom: 16px;
}

.search-box input {
  padding: 6px;
  width: 220px;
}

.result-list {
  list-style: none;
  padding: 0;
}

.result-item {
  border-bottom: 1px solid #eee;
}

.result-link {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  text-decoration: none;
  color: inherit;
}

.result-link img {
  width: 60px;
}

.title {
  font-weight: bold;
}

.author,
.publisher {
  font-size: 14px;
  color: #555;
}
</style>
