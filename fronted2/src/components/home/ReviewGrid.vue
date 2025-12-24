<template>
  <section class="review-section">
    <div class="container">
      <div class="section-header">
        <h2>{{ title }}</h2>
        <button class="link-more" @click="$emit('more')">전체 리뷰</button>
      </div>

      <div class="review-grid">
        <div class="glass-panel review-item" v-for="r in reviews" :key="r.id">
          <div class="reviewer">
            <div class="profile-pic"></div>
            <div>
              <div class="name">{{ r.user }}</div>
              <div class="time">{{ r.time }}</div>
            </div>
          </div>
          <div class="review-body">
            <h4>{{ r.bookTitle }}</h4>
            <p>{{ r.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: { type: String, default: "최근 심어진 이야기 💬" },
  reviews: { type: Array, default: () => [] },
});
defineEmits(["more"]);
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
.section-header h2{ font-size: 1.8rem; font-weight: 900; }
.link-more{ font-size: 0.9rem; font-weight: 900; color: var(--text-sub); }
.link-more:hover{ color: var(--primary); }

.review-grid{
  display:grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  padding-bottom: 100px;
}

.review-item{
  padding: 24px;
  background: rgba(255,255,255,0.8);
  transition: 0.2s;
}
.review-item:hover{
  background: white;
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}

.reviewer{
  display:flex;
  align-items:center;
  gap: 12px;
  margin-bottom: 16px;
}

.profile-pic{
  width: 40px; height: 40px;
  border-radius: 50%;
  background-image: linear-gradient(135deg, #e0e0e0, #f5f5f5);
}

.name{ font-weight: 900; font-size: 0.95rem; }
.time{ font-size: 0.8rem; color: var(--text-sub); font-weight: 400; }

.review-body h4{ font-size: 1.1rem; margin-bottom: 8px; font-weight: 900; }
.review-body p{ color: #505967; font-size: 0.95rem; line-height: 1.6; font-weight: 400; }

@media (max-width: 520px){
  .review-grid{ grid-template-columns: 1fr; }
}
</style>
