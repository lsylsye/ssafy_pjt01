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
  min-height: calc(100vh - 80px);
  background: linear-gradient(135deg, var(--primary-lighter) 0%, var(--bg-secondary) 100%);
  padding: 48px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.result-card {
  width: 100%;
  max-width: 640px;
  background: var(--bg-primary);
  border-radius: 20px;
  padding: 48px 40px;
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(34, 197, 94, 0.1);
  backdrop-filter: var(--blur-sm);
}

.section-title {
  font-size: 14px;
  color: var(--text-light);
  font-weight: 700;
  margin-bottom: 24px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.keywords {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-bottom: 24px;
}

.keyword-tag {
  background: var(--primary-lighter);
  color: var(--primary-dark);
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
  border: 1px solid var(--primary-color);
}

.analysis-desc {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.7;
  font-weight: 500;
  text-align: center;
}

.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-color), transparent);
  margin: 32px 0;
}

.books-wrapper {
  display: flex;
  flex-direction: column;
  gap: 28px;
  margin-bottom: 40px;
}

@media (min-width: 680px) {
  .books-wrapper {
    flex-direction: row;
    align-items: stretch;
  }
}

.book-card {
  flex: 1;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 28px 24px;
  position: relative;
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
  background: var(--bg-primary);
}

.badge {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 800;
  color: white;
  z-index: 1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-primary {
  background: var(--primary-color);
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
}

.badge-secondary {
  background: #ef4444;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.cover-area {
  margin-top: 24px;
  margin-bottom: 24px;
}

.book-cover {
  width: 130px;
  height: 180px;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: var(--shadow-lg);
}

.book-cover-placeholder {
  width: 130px;
  height: 180px;
  background: linear-gradient(135deg, var(--primary-lighter) 0%, var(--bg-tertiary) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: var(--text-light);
  border: 2px dashed var(--border-color);
}

.info-area {
  width: 100%;
}

.book-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.3;
  word-break: keep-all;
}

.book-author {
  font-size: 13px;
  color: var(--text-light);
  margin-bottom: 16px;
  font-weight: 500;
}

.ai-reason-box {
  background: var(--primary-lighter);
  border-radius: 12px;
  padding: 14px;
  text-align: left;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  display: flex;
  gap: 10px;
  align-items: flex-start;
  border: 1px solid var(--primary-color);
}

.ai-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.retry-btn {
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.retry-btn:active {
  transform: translateY(0);
}
</style>