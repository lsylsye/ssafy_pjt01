<template>
  <div class="result-container">
    <div class="result-card">
      
      <!-- 1. 사용자 분석 결과 -->
      <div class="analysis-section">
        <h3 class="section-title">당신의 독서 DNA</h3>
        <div class="keywords">
          <span v-for="(keyword, index) in keywords" :key="index" class="keyword-tag">
            #{{ keyword.trim() }}
          </span>
        </div>
        <p class="analysis-desc">
          당신의 취향을 분석하여<br>
          꼭 맞는 책 2권을 선정했습니다.
        </p>
      </div>

      <div class="divider"></div>

      <!-- 2. 추천 도서 리스트 (2권) -->
      <div class="books-wrapper">
        <div 
          v-for="(book, index) in result.books" 
          :key="index" 
          class="book-card"
          @click="goToDetail(book.isbn)"
        >
          <!-- 뱃지 (운명의 책 / 새로운 시도) -->
          <div class="badge" :class="index === 0 ? 'badge-primary' : 'badge-secondary'">
            {{ book.type }}
          </div>

          <!-- 책 표지 -->
          <div class="cover-area">
            <img v-if="book.cover" :src="book.cover" :alt="book.title" class="book-cover" />
            <div v-else class="book-cover-placeholder">NO IMAGE</div>
          </div>

          <!-- 책 정보 -->
          <div class="info-area">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author }}</p>
            
            <!-- AI 추천사 -->
            <div class="ai-reason-box">
              <span class="ai-icon">🤖</span>
              <p class="ai-text">{{ book.reason }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 하단 버튼 -->
      <div class="actions">
        <button class="retry-btn" @click="router.push('/recommend')">다시 테스트하기</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// history.state로 넘겨받은 데이터
const result = computed(() => history.state.resultData || { books: [], analysis: "" });

// 키워드 파싱
const keywords = computed(() => {
  if (result.value.analysis) {
    return result.value.analysis.split(',');
  }
  return ['취향 분석 중...'];
});

// 상세 페이지 이동 함수
const goToDetail = (isbn) => {
  if (isbn) {
    router.push(`/books/${isbn}`);
  } else {
    alert("ISBN 정보가 없어 상세 페이지로 이동할 수 없습니다.");
  }
};

// 데이터가 없으면 홈으로 튕기기 (새로고침 시 방지)
if (!history.state.resultData) {
  router.replace('/recommend');
}
</script>

<style scoped>
.result-container {
  min-height: 100vh;
  background-color: #F2F4F6;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 내용이 길어질 수 있으므로 상단 정렬 */
  font-family: "Pretendard", sans-serif;
}

.result-card {
  width: 100%;
  max-width: 600px; /* 2권이라 폭을 좀 더 넓게 */
  background: white;
  border-radius: 24px;
  padding: 40px 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.06);
  text-align: center;
}

/* 분석 섹션 */
.section-title {
  font-size: 16px;
  color: #8B95A1;
  font-weight: 600;
  margin-bottom: 32px;
}

.keywords {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
}

.keyword-tag {
  background-color: #E8F3FF;
  color: #3182F6;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
}

.analysis-desc {
  font-size: 16px;
  color: #333;
  line-height: 1.5;
  font-weight: 500;
}

.divider {
  height: 1px;
  background-color: #E5E8EB;
  margin: 30px 0;
}

/* 책 카드 영역 */
.books-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 40px;
}

/* 데스크탑(태블릿)에서는 가로 배치 */
@media (min-width: 600px) {
  .books-wrapper {
    flex-direction: row;
    align-items: stretch;
  }
}

.book-card {
  flex: 1;
  background-color: #F9FAFB;
  border: 1px solid #E5E8EB;
  border-radius: 20px;
  padding: 24px 20px;
  position: relative;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  border-color: #3182F6;
}

/* 뱃지 스타일 */
.badge {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 800;
  color: white;
  z-index: 1;
}

.badge-primary { background-color: #3182F6; } /* 파란색 */
.badge-secondary { background-color: #FF6B6B; } /* 붉은색 포인트 */

/* 책 표지 */
.cover-area {
  margin-top: 20px;
  margin-bottom: 20px;
}

.book-cover {
  width: 120px;
  height: 180px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 4px 4px 12px rgba(0,0,0,0.15);
}

.book-cover-placeholder {
  width: 120px;
  height: 180px;
  background-color: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  color: #aaa;
}

/* 책 정보 */
.info-area {
  width: 100%;
}

.book-title {
  font-size: 18px;
  font-weight: 700;
  color: #191F28;
  margin-bottom: 6px;
  line-height: 1.3;
  word-break: keep-all;
}

.book-author {
  font-size: 14px;
  color: #8B95A1;
  margin-bottom: 16px;
}

/* AI 코멘트 */
.ai-reason-box {
  background-color: white;
  border-radius: 12px;
  padding: 12px;
  text-align: left;
  font-size: 13px;
  color: #4E5968;
  line-height: 1.5;
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.ai-icon { font-size: 16px; }

/* 버튼 */
.retry-btn {
  width: 100%;
  padding: 18px;
  background-color: #3182F6;
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-btn:hover { background-color: #1B64DA; }
</style>