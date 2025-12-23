<!-- src/views/main/MainView.vue -->
<template>
  <section class="main">
    <!-- ✅ 배너 슬라이더 -->
    <div class="banner-carousel">
      <div class="carousel-wrapper">
        <img :src="bannerImages[currentBannerIndex]" :alt="`배너 ${currentBannerIndex + 1}`" class="banner-image" />
      </div>
      <div class="carousel-controls">
        <button class="control-btn prev" @click="prevBanner">❮</button>
        <div class="dots">
          <button v-for="(_, index) in bannerImages" :key="index" 
            :class="['dot', { active: index === currentBannerIndex }]"
            @click="currentBannerIndex = index"></button>
        </div>
        <button class="control-btn next" @click="nextBanner">❯</button>
      </div>
    </div>

    <h2 class="section-title">베스트셀러 TOP 10</h2>

    <ul class="bestseller-list">
      <li v-for="book in top10" :key="book.id" class="bestseller-item">
        <router-link :to="`/books/${book.isbn13}`" class="bestseller-link">
          <span class="rank">{{ book.best_rank }}</span>
          <img :src="book.cover" alt="표지" class="cover" />
          <span class="book-title">{{ book.title }}</span>
          <span class="book-author">{{ book.author }}</span>
        </router-link>
      </li>
    </ul>

    <!-- ✅ 주목할 만한 신간 5권(가로 스크롤) -->
    <NewSpecialSection />

    <!-- ✅ 추천 시스템1(작가버전): 신간 아래 -->
    <RecommendBookmarkSection />

    <!-- ✅ 추천 시스템2(팔로잉버전): 작가추천 아래 -->
    <RecommendFollowSection />
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import api from "@/api/axios";
import NewSpecialSection from "@/components/books/NewSpecialSection.vue";
import RecommendBookmarkSection from "@/components/home/RecommendBookmarkSection.vue";
import RecommendFollowSection from "@/components/home/RecommendFollowSection.vue";

const bestsellers = ref([]);
const currentBannerIndex = ref(0);

// 배너 이미지 (assets/image001.png 사용)
const bannerImages = [
  new URL('@/assets/image001.png', import.meta.url).href,
  new URL('@/assets/image001.png', import.meta.url).href,
  new URL('@/assets/image001.png', import.meta.url).href,
];

let carouselInterval = null;

const fetchBestsellers = () => {
  api
    .get("/api/books/bestsellers/", { auth: false })
    .then((res) => {
      bestsellers.value = Array.isArray(res.data) ? res.data : [];
    })
    .catch((err) => {
      console.error(err);
    });
};

const top10 = computed(() => bestsellers.value.slice(0, 10));

const nextBanner = () => {
  currentBannerIndex.value = (currentBannerIndex.value + 1) % bannerImages.length;
};

const prevBanner = () => {
  currentBannerIndex.value = (currentBannerIndex.value - 1 + bannerImages.length) % bannerImages.length;
};

const startCarousel = () => {
  carouselInterval = setInterval(() => {
    nextBanner();
  }, 3000);
};

const stopCarousel = () => {
  if (carouselInterval) {
    clearInterval(carouselInterval);
    carouselInterval = null;
  }
};

onMounted(() => {
  fetchBestsellers();
  startCarousel();
});

onUnmounted(() => {
  stopCarousel();
});
</script>

<style scoped>
.main {
  padding: 40px 32px;
  background: var(--bg-secondary);
  min-height: calc(100vh - 80px);
  max-width: 1320px;
  margin: 0 auto;
}

/* ✅ 배너 슬라이더 */
.banner-carousel {
  margin-bottom: 48px;
  border-radius: 12px;
  overflow: hidden;
}

.carousel-wrapper {
  position: relative;
  width: 100%;
  height: 300px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 12px;
  background: var(--bg-primary);
  border-top: 1px solid var(--border-color);
}

.control-btn {
  border: none;
  background: none;
  font-size: 20px;
  cursor: pointer;
  color: var(--text-secondary);
  transition: var(--transition);
  padding: 4px 8px;
}

.control-btn:hover {
  color: var(--primary-color);
}

.dots {
  display: flex;
  gap: 8px;
}

.dot {
  border: none;
  background: #ddd;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  cursor: pointer;
  transition: var(--transition);
}

.dot.active {
  background: var(--primary-color);
}

.dot:hover {
  background: var(--primary-color);
}

.section-title {
  margin: 0 0 24px;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
  line-height: 1.2;
  ook-author {
  font-size: 12px;
  color: var(--text-secondary);
  text-align: center;
  line-height: 1.3;
}

.bcolor: var(--text-primary);
  position: relative;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--primary-color);
  display: inline-block;
}

.bestseller-list {
  list-style: none;
  padding: 0;
  margin: 0 0 48px;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.bestseller-item {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: var(--bg-primary);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: var(--transition);
}

.bestseller-item:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
}

.bestseller-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 20px;
  text-decoration: none;
  color: inherit;
  height: 100%;
}

.rank {
  font-weight: 700;
  color: white;
  background: var(--primary-color);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.cover {
  width: 100%;
  max-width: 160px;
  height: auto;
  border-radius: 8px;
  box-shadow: var(--shadow-md);
}

.book-title {
  font-size: 14px;
  font-weight: 600;
  text-align: center;
  color: var(--text-primary);
  line-height: 1.4;
}

.bestseller-link:hover .book-title {
  color: var(--primary-color);
}
</style>
