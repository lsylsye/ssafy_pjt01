<template>
  <div class="page">
    <div class="container">
      <header class="list-header">
        <h1 class="title">최근 심어진 이야기들 🌿</h1>
        <p class="desc">정원사들이 정성껏 심은 소중한 독서 기록을 둘러보세요.</p>
      </header>

      <div v-if="loading" class="review-grid">
        <div v-for="i in 6" :key="i" class="review-card-sk"></div>
      </div>

      <div v-else class="review-grid">
        <div 
          v-for="rev in reviews" 
          :key="rev.id" 
          class="review-card"
          @click="goBookDetail(rev.isbn13)"
        >
          <div class="card-left">
            <div class="book-mini-canvas">
              <img :src="rev.book_cover" class="mini-cover" alt="" />
              <div class="spine"></div>
            </div>
          </div>
          <div class="card-right">
            <div class="user-info">
              <img v-if="rev.user_profile_image" :src="getProfileImage(rev.user_profile_image)" class="avatar" />
              <div v-else class="avatar ph"><User :size="14" /></div>
              <span class="nick">{{ rev.user_nickname }}</span>
              <span class="date">{{ fromNow(rev.created_at) }}</span>
            </div>
            <h3 class="book-name">《{{ rev.book_title }}》</h3>
            <p class="content">{{ rev.content }}</p>
            <div class="stars">
              <Star 
                v-for="i in 5" :key="i" :size="12" 
                :fill="i <= rev.rating ? '#FFD700' : 'none'" 
                :color="i <= rev.rating ? '#FFD700' : '#e5e8eb'" 
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { getReviews } from '@/api/review';
import { User, Star } from 'lucide-vue-next';

const router = useRouter();
const reviews = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await getReviews();
    reviews.value = (res.data || []).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
});

function goBookDetail(isbn) {
  if (isbn) router.push(`/books/${isbn}`);
}

const getProfileImage = (url) => {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  return `http://127.0.0.1:8000${url.startsWith('/') ? '' : '/'}${url}`;
};

const fromNow = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diff = now - date;
  
  const min = 60 * 1000;
  const hour = min * 60;
  const day = hour * 24;

  if (diff < min) return '방금 전';
  if (diff < hour) return Math.floor(diff / min) + '분 전';
  if (diff < day) return Math.floor(diff / hour) + '시간 전';
  if (diff < day * 7) return Math.floor(diff / day) + '일 전';
  return date.toLocaleDateString();
};
</script>

<style scoped>
.page {
  min-height: 100vh;
  padding-bottom: 80px;
}
.container {
  max-width: 1000px;
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

.review-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
  gap: 24px;
}

.review-card {
  background: white;
  padding: 24px;
  border-radius: 20px;
  display: flex;
  gap: 20px;
  cursor: pointer;
  border: 1px solid rgba(0,0,0,0.03);
  box-shadow: 0 4px 16px rgba(0,0,0,0.02);
  transition: all 0.3s ease;
}
.review-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.06);
}

.book-mini-canvas {
  position: relative;
  width: 80px;
  aspect-ratio: 2/3;
  border-radius: 2px 6px 6px 2px;
  overflow: hidden;
  box-shadow: 3px 5px 12px rgba(0,0,0,0.15);
}
.mini-cover { width: 100%; height: 100%; object-fit: cover; }
.spine {
  position: absolute;
  top: 0; left: 0; bottom: 0; width: 6px;
  background: linear-gradient(to right, rgba(0,0,0,0.2), transparent);
}

.card-right {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}
.avatar { width: 20px; height: 20px; border-radius: 50%; object-fit: cover; }
.avatar.ph { background: #f2f4f6; display: flex; align-items: center; justify-content: center; color: #adb5bd; }
.nick { font-size: 0.85rem; font-weight: 700; color: #191f28; }
.date { font-size: 0.8rem; color: #b0b8c1; margin-left: auto; }

.book-name {
  font-size: 0.95rem;
  font-weight: 800;
  color: #00d15b;
  margin-bottom: 8px;
}

.content {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #4e5968;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.stars { display: flex; gap: 1px; }

/* Skeletons */
.review-card-sk {
  height: 180px;
  background: #f2f4f6;
  border-radius: 20px;
  animation: pulse 1.5s infinite;
}

@media (max-width: 600px) {
  .review-grid {
    grid-template-columns: 1fr;
  }
}
</style>
