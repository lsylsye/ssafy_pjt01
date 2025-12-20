<template>
  <section>
    <p v-if="isLoading">불러오는 중...</p>
    <p v-else-if="errorMsg">{{ errorMsg }}</p>

    <div v-else-if="book">
      <h1>{{ book.title }}</h1>

      <div class="detail">
        <img :src="book.cover" alt="표지" />

        <div class="info">
          <p>저자: {{ book.author }}</p>
          <p>출판사: {{ book.publisher }}</p>
          <p v-if="book.category_name">카테고리: {{ book.category_name }}</p>
        </div>
      </div>

      <p v-if="book.description" class="description">
        {{ book.description }}
      </p>
    </div>

    <p v-else>도서 데이터가 없습니다.</p>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()

const book = ref(null)
const isLoading = ref(false)
const errorMsg = ref('')

const fetchBookDetail = (isbn13) => {
  if (!isbn13) return

  isLoading.value = true
  errorMsg.value = ''
  book.value = null

  // ✅ Django 스타일: 끝에 / 붙이는 게 안전함
  api.get(`/api/books/${isbn13}/`)
    .then((res) => {
      book.value = res.data
    })
    .catch((err) => {
      console.error(err)
      errorMsg.value = '도서 정보를 불러오지 못했습니다.'
    })
    .finally(() => {
      isLoading.value = false
    })
}

onMounted(() => {
  fetchBookDetail(route.params.isbn13)
})

// ✅ 같은 컴포넌트에서 isbn만 바뀌어도 다시 호출되게
watch(
  () => route.params.isbn13,
  (newIsbn) => {
    fetchBookDetail(newIsbn)
  }
)
</script>

<style scoped>
.detail {
  display: flex;
  gap: 24px;
  margin-top: 16px;
}

.detail img {
  width: 180px;
  height: auto;
}

.description {
  margin-top: 24px;
  line-height: 1.6;
}
</style>
