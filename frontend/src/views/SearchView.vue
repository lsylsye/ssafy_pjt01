<template>
  <section>
    <h1>도서 검색</h1>

    <!-- 검색창 -->
    <div>
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
        <img :src="book.cover" alt="표지" width="60" />
        <div>
          <p><strong>{{ book.title }}</strong></p>
          <p>{{ book.author }}</p>
          <p>{{ book.publisher }}</p>
        </div>
      </li>
    </ul>

    <!-- 검색 결과 없음 -->
    <p v-else-if="isSearched">
      검색 결과가 없습니다.
    </p>
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
.result-list {
  list-style: none;
  padding: 0;
}

.result-item {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}
</style>
