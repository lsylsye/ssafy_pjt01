<template>
  <section class="search-container">
    <div class="search-header">
      <h1 class="search-title">도서 검색</h1>
      <p class="search-subtitle">책 제목이나 저자를 입력하세요</p>
    </div>

    <div class="search-box">
      <input
        v-model="query"
        placeholder="책 제목 또는 저자 검색..."
        @keyup.enter="searchBooks"
        class="search-input"
      />
      <button @click="searchBooks" class="search-button">검색</button>
    </div>

    <div v-if="results.length" class="results-container">
      <p class="results-count">{{ results.length }}개의 검색 결과</p>
      <ul class="result-list">
        <li
          v-for="book in results"
          :key="book.isbn13"
          class="result-item"
        >
          <router-link
            :to="`/books/${book.isbn13}`"
            class="result-link"
          >
            <div class="result-cover">
              <img :src="book.cover" alt="표지" />
            </div>
            <div class="result-content">
              <p class="result-title">{{ book.title }}</p>
              <p class="result-author">{{ book.author }}</p>
              <p class="result-publisher">{{ book.publisher }}</p>
            </div>
          </router-link>
        </li>
      </ul>
    </div>

    <div v-else-if="isSearched" class="empty-state">
      <p class="empty-message">검색 결과가 없습니다</p>
      <p class="empty-hint">다른 키워드로 검색해보세요</p>
    </div>

    <div v-else class="initial-state">
      <p class="initial-message">검색어를 입력하면 결과가 표시됩니다</p>
    </div>
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
.search-container {
  min-height: calc(100vh - 80px);
  background: var(--bg-secondary);
  padding: 40px 32px;
}

.search-header {
  text-align: center;
  margin-bottom: 40px;
}

.search-title {
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px;
  letter-spacing: -0.5px;
}

.search-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
}

.search-box {
  display: flex;
  gap: 12px;
  max-width: 600px;
  margin: 0 auto 48px;
}

.search-input {
  flex: 1;
  padding: 14px 18px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  font-size: 15px;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: var(--text-primary);
  background: var(--bg-primary);
  transition: var(--transition);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.search-button {
  padding: 14px 32px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
}

.search-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.results-container {
  max-width: 900px;
  margin: 0 auto;
}

.results-count {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 20px;
}

.result-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.result-item {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
}

.result-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.result-link {
  display: flex;
  gap: 20px;
  padding: 16px;
  text-decoration: none;
  color: inherit;
}

.result-cover {
  flex-shrink: 0;
  width: 80px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
}

.result-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.result-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.result-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px;
  line-height: 1.4;
  word-break: keep-all;
}

.result-author {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 4px;
  font-weight: 500;
}

.result-publisher {
  font-size: 13px;
  color: var(--text-light);
  margin: 0;
}

.empty-state,
.initial-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
}

.empty-message,
.initial-message {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0;
}

.empty-hint {
  font-size: 14px;
  color: var(--text-light);
  margin: 8px 0 0;
}
</style>
