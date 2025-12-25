<template>
  <div class="page">
    <div class="container">
      <header class="list-header">
        <h1 class="title">많은 사람들이 찾는 책 🔥</h1>
        <p class="desc">지금 가장 핫한 베스트셀러 20권을 만나보세요.</p>
      </header>

      <div v-if="loading" class="shelf-grid">
        <div v-for="i in 10" :key="i" class="book-card-sk"></div>
      </div>

      <div v-else class="shelf-grid">
        <div 
          v-for="book in bestsellers" 
          :key="book.isbn13" 
          class="book-card"
          @click="goDetail(book)"
        >
          <div class="cover-canvas">
            <img :src="book.cover" :alt="book.title" class="book-cover" />
            <div class="spine-overlay"></div>
          </div>
          <div class="book-info">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { getBestsellers } from '@/api/books.api';

const router = useRouter();
const bestsellers = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await getBestsellers();
    // Assuming getBestsellers might return more than 20, slice to be safe
    bestsellers.value = (res.data?.items || res.data || []).slice(0, 20);
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
});

function goDetail(book) {
  const isbn = book.isbn13 || book.id;
  if (isbn) router.push(`/books/${isbn}`);
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  padding-bottom: 80px;
}
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 60px 20px;
}
.list-header {
  margin-bottom: 50px;
  text-align: center;
}
.title {
  font-size: 2.4rem;
  font-weight: 900;
  margin-bottom: 12px;
  color: #191f28;
}
.desc {
  font-size: 1.1rem;
  color: #8b95a1;
}

.shelf-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 40px 30px;
  /* Bookshelf shelf visual */
}

.book-card {
  cursor: pointer;
  transition: transform 0.3s ease;
}
.book-card:hover {
  transform: translateY(-10px);
}

.cover-canvas {
  position: relative;
  width: 100%;
  aspect-ratio: 2/3;
  border-radius: 4px 12px 12px 4px;
  overflow: hidden;
  box-shadow: 
    5px 15px 30px rgba(0,0,0,0.2),
    0 4px 8px rgba(0,0,0,0.1);
  margin-bottom: 16px;
  background: #f2f4f6;
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.spine-overlay {
  position: absolute;
  top: 0; left: 0; bottom: 0;
  width: 12px;
  background: linear-gradient(to right, 
    rgba(0,0,0,0.15) 0%, 
    rgba(255,255,255,0.1) 50%, 
    rgba(0,0,0,0.1) 100%);
  border-right: 1px solid rgba(0,0,0,0.05);
}

.book-info {
  text-align: center;
}
.book-title {
  font-size: 1rem;
  font-weight: 800;
  color: #191f28;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}
.book-author {
  font-size: 0.85rem;
  color: #6b7684;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Skeletons */
.book-card-sk {
  width: 100%;
  aspect-ratio: 2/3;
  background: #f2f4f6;
  border-radius: 12px;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

@media (max-width: 600px) {
  .shelf-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
