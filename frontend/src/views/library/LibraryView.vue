<template>
  <div class="page-container">
    <!-- 뒤로가기 버튼 (상단 네비게이션) -->
    <header class="header">
      <button class="back-btn" @click="$router.go(-1)">
        ← 뒤로
      </button>
    </header>

    <div class="content-wrapper">
      <!-- 타이틀 -->
      <div class="title-area">
        <h1 class="page-title">내 주변 도서관</h1>
        <p class="sub-title">현재 위치를 기반으로 가까운 도서관을 찾습니다.</p>
      </div>

      <!-- 지도 영역 (카드 형태 디자인) -->
      <div class="map-card">
        <!-- 로딩 중일 때 -->
        <div v-if="isLoading" class="status-box">
          <div class="spinner"></div>
          <p>위치를 불러오고 있어요...</p>
        </div>

        <!-- 에러 났을 때 -->
        <div v-else-if="error" class="status-box error">
          <p>😥 {{ error }}</p>
          <button class="retry-btn" @click="getMyLocation">다시 시도</button>
        </div>

        <!-- 지도 표시 (성공 시) -->
        <iframe
          v-else
          class="map-frame"
          :src="mapUrl"
          allowfullscreen
          loading="lazy"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const lat = ref(0);
const lng = ref(0);
const mapUrl = ref('');
const error = ref('');
const isLoading = ref(true);

const getMyLocation = () => {
  isLoading.value = true;
  error.value = '';

  if (!navigator.geolocation) {
    error.value = '위치 정보를 지원하지 않는 브라우저입니다.';
    isLoading.value = false;
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      lat.value = position.coords.latitude;
      lng.value = position.coords.longitude;
      
      // 구글 지도 임베드 URL (q: 검색어, ll: 중심좌표, z: 줌레벨)
      mapUrl.value = `https://maps.google.com/maps?q=도서관&ll=${lat.value},${lng.value}&z=15&output=embed`;
      isLoading.value = false;
    },
    (err) => {
      console.error(err);
      error.value = '위치 권한을 허용해주세요.';
      isLoading.value = false;
    }
  );
};

onMounted(() => {
  getMyLocation();
});
</script>

<style scoped>
.page-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 32px 20px;
  background: linear-gradient(135deg, var(--primary-lighter) 0%, var(--bg-secondary) 100%);
  min-height: calc(100vh - 80px);
}

.header {
  margin-bottom: 28px;
}

.back-btn {
  background: var(--primary-color);
  border: none;
  font-size: 15px;
  color: white;
  cursor: pointer;
  padding: 10px 16px;
  font-weight: 600;
  border-radius: 10px;
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
}

.back-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.title-area {
  margin-bottom: 32px;
  text-align: center;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px;
  letter-spacing: -0.5px;
}

.sub-title {
  font-size: 15px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
}

.map-card {
  width: 100%;
  height: 520px;
  background: var(--bg-primary);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  position: relative;
  border: 1px solid var(--border-color);
}

.map-frame {
  width: 100%;
  height: 100%;
  border: none;
}

.status-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  gap: 16px;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.status-box p {
  margin: 0;
  font-weight: 500;
  font-size: 16px;
}

.status-box.error {
  color: #ef4444;
}

.retry-btn {
  padding: 12px 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: var(--transition);
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
}

.retry-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

@media (max-width: 600px) {
  .page-container {
    padding: 20px 16px;
  }

  .page-title {
    font-size: 28px;
  }

  .map-card {
    height: 400px;
  }
}
</style>