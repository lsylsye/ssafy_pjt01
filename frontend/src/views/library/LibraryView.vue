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
/* 전체 페이지 레이아웃 */
.page-container {
  max-width: 600px; /* 너무 퍼지지 않게 중앙 정렬 */
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  min-height: 100vh;
}

/* 헤더 & 뒤로가기 */
.header {
  margin-bottom: 20px;
}
.back-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: #3182f6; /* 토스 블루 */
  cursor: pointer;
  padding: 0;
  font-weight: 600;
}

/* 타이틀 영역 */
.title-area {
  margin-bottom: 24px;
}
.page-title {
  font-size: 28px;
  font-weight: 800;
  color: #191f28; /* 진한 검정 */
  margin: 0 0 8px 0;
}
.sub-title {
  font-size: 15px;
  color: #8b95a1; /* 회색 */
  margin: 0;
}

/* 지도 카드 디자인 (둥글고 그림자 있게) */
.map-card {
  width: 100%;
  height: 500px;
  background-color: #f2f4f6;
  border-radius: 24px; /* 애플/토스 스타일의 둥근 모서리 */
  overflow: hidden;    /* 내용이 둥근 모서리 밖으로 나가지 않게 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); /* 부드러운 그림자 */
  position: relative;
}

.map-frame {
  width: 100%;
  height: 100%;
  border: none;
}

/* 로딩 & 에러 상태 디자인 */
.status-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #6b7684;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #e5e8eb;
  border-top-color: #3182f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.retry-btn {
  margin-top: 12px;
  padding: 8px 16px;
  background-color: #3182f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
</style>