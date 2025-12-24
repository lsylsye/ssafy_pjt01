<template>
  <section class="review-section">
    <div class="container">
      <div class="section-header">
        <h2>{{ title }}</h2>
        <button class="link-more" @click="$emit('more')">전체 리뷰</button>
      </div>

      <div v-if="loading" class="review-grid">
        <div v-for="i in 3" :key="i" class="skeleton-card"></div>
      </div>

      <div v-else class="review-grid">
        <div class="glass-panel review-item" v-for="r in reviews" :key="r.id">
          <div class="reviewer">
            <div class="profile-pic">
              <img v-if="r.user_profile_image" :src="getProfileImage(r.user_profile_image)" alt="" />
              <User v-else :size="20" color="#8b95a1" />
            </div>
            <div class="reviewer-meta">
              <div class="name">{{ r.user }}</div>
              <div class="time">{{ fromNow(r.time) }}</div>
            </div>
            <div class="stars">
              <Star 
                v-for="i in 5" 
                :key="i" 
                :size="12" 
                :fill="i <= r.rating ? '#FFD700' : 'none'" 
                :color="i <= r.rating ? '#FFD700' : '#e5e8eb'"
              />
            </div>
          </div>
          <div class="review-body">
            <h4>{{ r.bookTitle }}</h4>
            <p>{{ r.content }}</p>
          </div>
        </div>
      </div>

      <div v-if="!loading && reviews.length === 0" class="empty-state">
        아직 심어진 이야기가 없어요. 🌱
      </div>
    </div>
  </section>
</template>

<script setup>
import { User, Star } from 'lucide-vue-next';

defineProps({
  title: { type: String, default: "최근 심어진 이야기 💬" },
  reviews: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
});
defineEmits(["more"]);

const getProfileImage = (url) => {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  const path = String(url).startsWith("/") ? url : `/${url}`;
  return `http://127.0.0.1:8000${path}`;
};

const fromNow = (iso) => {
  if (!iso) return "";
  try {
    const d = new Date(iso);
    const diff = Date.now() - d.getTime();
    const sec = Math.floor(diff / 1000);
    if (sec < 60) return "방금 전";
    const min = Math.floor(sec / 60);
    if (min < 60) return `${min}분 전`;
    const hr = Math.floor(min / 60);
    if (hr < 24) return `${hr}시간 전`;
    const day = Math.floor(hr / 24);
    return `${day}일 전`;
  } catch {
    return "";
  }
};
</script>

<style scoped>
.review-section{ width: 100%; }
.container{ max-width: 1100px; margin: 0 auto; padding: 0 24px; width: 100%; }

.section-header{
  display:flex;
  justify-content: space-between;
  align-items: flex-end;
  margin: 60px 0 24px;
}
.section-header h2{ font-size: 1.8rem; font-weight: 900; letter-spacing: -0.5px; }
.link-more{ font-size: 0.9rem; font-weight: 900; color: var(--text-sub); }
.link-more:hover{ color: var(--primary); }

.review-grid{
  display:grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
  padding-bottom: 80px;
}

.review-item{
  padding: 24px;
  background: white;
  border-radius: 24px;
  border: 1px solid rgba(0,0,0,0.03);
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
  transition: 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.review-item:hover{
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.06);
  border-color: var(--primary);
}

.reviewer{
  display:flex;
  align-items:center;
  gap: 12px;
  margin-bottom: 16px;
}

.profile-pic{
  width: 42px; height: 42px;
  border-radius: 50%;
  background: #f2f4f6;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.profile-pic img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.reviewer-meta { flex: 1; }
.name{ font-weight: 800; font-size: 0.95rem; color: #191f28; }
.time{ font-size: 0.8rem; color: #b0b8c1; font-weight: 500; margin-top: 2px; }

.stars { display: flex; gap: 1px; }

.review-body h4{ 
  font-size: 1.05rem; 
  margin-bottom: 8px; 
  font-weight: 800; 
  color: #191f28;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.review-body p{ 
  color: #4e5968; 
  font-size: 0.95rem; 
  line-height: 1.6; 
  font-weight: 500;
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.skeleton-card {
  height: 180px;
  background: linear-gradient(90deg, #f2f4f6 25%, #f9fafb 50%, #f2f4f6 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 24px;
}

.empty-state {
  text-align: center;
  padding: 60px 0 100px;
  color: #8b95a1;
  font-weight: 600;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (max-width: 520px){
  .review-grid{ grid-template-columns: 1fr; }
}
</style>
