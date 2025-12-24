<template>
  <div class="result-container">
    <div class="result-card">
      <div class="analysis-header">
        <div class="title-row">
          <span class="dna-label">당신의 독서 DNA</span>
          <h2 class="main-title">취향 분석 결과</h2>
        </div>

        <div class="tags-container">
          <span v-for="(keyword, index) in keywords" :key="index" class="hashtag">
            #{{ keyword }}
          </span>
        </div>

        <p class="summary-text">
           {{ books.length }}권의 특별한 책을 선정했습니다.
        </p>
      </div>

      <div class="divider"></div>

      <div class="recommendation-list">
        <div
          v-for="(book, index) in books"
          :key="index"
          class="book-row-card"
          @click="goToDetail(book.isbn13)"
        >
          <div class="book-cover-wrap">
            <img v-if="book.cover" :src="book.cover" class="book-thumb" />
            <div v-else class="book-thumb-ph">Cover</div>
            <div class="rank-badge">{{ index + 1 }}</div>
          </div>

            <div class="book-details">
            <div class="detail-header">
              <span class="type-tag" :class="index === 0 ? 'destiny' : 'challenge'">
                {{ book.type || (index === 0 ? "운명의 책" : "새로운 시도") }}
              </span>
              <h3 class="display-title">{{ book.title }}</h3>
              <p class="author-label">{{ book.author }}</p>
            </div>

            <div class="ai-insight">
              <div class="insight-label">AI Insights</div>
              <p class="insight-content">{{ book.reason }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="actions">
        <button class="retry-btn" type="button" @click="retry">다시 테스트하기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

function safeParse(jsonStr) {
  try {
    return JSON.parse(jsonStr);
  } catch {
    return null;
  }
}

const raw = safeParse(sessionStorage.getItem("taste_result")) || {};

const analysisText = computed(() => {
  // 백엔드가 어떤 키로 주든 대응
  return raw.analysis || raw.analysis_text || raw.keywords || raw.summary || "";
});

const keywords = computed(() => {
  const t = analysisText.value;
  if (!t) return ["취향", "분석", "완료"];
  return String(t)
    .split(/[,\n]/)
    .map((s) => s.trim())
    .filter(Boolean)
    .slice(0, 8);
});

const books = computed(() => {
  // books/items/recommendations 등 어떤 형태든 대응
  const arr = raw.books || raw.items || raw.recommendations || [];
  if (!Array.isArray(arr)) return [];

  return arr.map((b) => ({
    type: b.type,
    isbn13: b.isbn13 || b.isbn || b.item_id,
    title: b.title || "제목 없음",
    author: b.author || "-",
    cover: b.cover || "",
    reason: b.reason || b.recommend_reason || "추천 사유가 없습니다.",
  }));
});

const goToDetail = (isbn13) => {
  if (!isbn13) {
    alert("ISBN 정보가 없어 상세 페이지로 이동할 수 없습니다.");
    return;
  }
  router.push(`/books/${isbn13}`);
};

const retry = () => {
  sessionStorage.removeItem("taste_result");
  router.push("/taste/test");
};

// 새로고침 등으로 결과 데이터가 없으면 테스트로 보내기
if (!sessionStorage.getItem("taste_result")) {
  router.replace("/taste/test");
}
</script>

<style scoped>
/* src/views/TasteResultView.vue (style scoped 교체본) */
.result-container {
  --primary: #00d15b;
  --bg: #f8fafb;
  --card-bg: rgba(255, 255, 255, 0.8);
  --text-main: #191f28;
  --text-grey: #4e5968;
  --text-light: #8b95a1;

  min-height: calc(100vh - 70px);
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  background: var(--bg);
  font-family: "Pretendard", -apple-system, sans-serif;
}

.result-card {
  width: 100%;
  max-width: 760px;
  background: var(--card-bg);
  backdrop-filter: blur(20px);
  border-radius: 32px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.03);
  border: 1px solid #fff;
}

/* 헤더 구조 */
.analysis-header {
  text-align: center;
  margin-bottom: 40px;
}
.dna-label {
  display: block;
  font-size: 0.92rem;
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 8px;
  letter-spacing: 1px;
}
.main-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 20px;
}
.tags-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
}
.hashtag {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-grey);
  background: #fff;
  padding: 6px 14px;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.08);
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  transition: all 0.2s ease;
}
.hashtag:hover {
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
}
.summary-text {
  font-size: 1.1rem;
  color: var(--text-grey);
  font-weight: 500;
}

.divider {
  height: 1px;
  background: rgba(0,0,0,0.05);
  margin: 32px 0;
}

/* 다단 가로 카드 구조 */
.recommendation-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 40px;
}

.book-row-card {
  display: flex;
  gap: 28px;
  background: #fff;
  padding: 24px;
  border-radius: 24px;
  cursor: pointer;
  transition: 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
  border: 1px solid transparent;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

.book-row-card:hover {
  transform: translateX(8px);
  border-color: var(--primary);
  box-shadow: 0 12px 32px rgba(0, 209, 91, 0.08);
}

.book-cover-wrap {
  position: relative;
  flex-shrink: 0;
}
.book-thumb {
  width: 120px;
  height: 170px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 4px 8px 16px rgba(0,0,0,0.1);
}
.book-thumb-ph {
  width: 120px;
  height: 170px;
  background: #f2f4f6;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-light);
}
.rank-badge {
  position: absolute;
  top: -8px;
  left: -8px;
  width: 32px;
  height: 32px;
  background: var(--primary);
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1rem;
  box-shadow: 0 4px 8px rgba(0, 209, 91, 0.3);
}

.book-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.type-tag {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 6px;
  margin-bottom: 8px;
}
.type-tag.destiny {
  color: var(--primary);
  background: rgba(0, 209, 91, 0.1);
}
.type-tag.challenge {
  color: #a855f7; /* 보라색 계열로 구분 */
  background: rgba(168, 85, 247, 0.1);
}

.display-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 4px;
  line-height: 1.3;
}
.author-label {
  font-size: 1rem;
  color: var(--text-light);
  font-weight: 500;
  margin-bottom: 16px;
}

/* AI 인사이트 블록 */
.ai-insight {
  background: #f9fafb;
  padding: 16px;
  border-radius: 16px;
  border-left: 4px solid var(--primary);
}
.insight-label {
  font-size: 0.75rem;
  font-weight: 800;
  color: var(--primary);
  text-transform: uppercase;
  margin-bottom: 6px;
}
.insight-content {
  font-size: 0.9rem;
  color: var(--text-grey);
  line-height: 1.6;
  margin: 0;
  font-weight: 500;
}

.actions {
  display: flex;
  justify-content: center;
}

.retry-btn {
  padding: 16px 48px;
  border-radius: 16px;
  border: none;
  background: #f2f4f6;
  color: var(--text-grey);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: 0.2s;
}

.retry-btn:hover {
  background: #e5e8eb;
  color: var(--text-main);
}

@media (max-width: 600px) {
  .book-row-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .display-title {
    font-size: 1.2rem;
  }
  .ai-insight {
    text-align: left;
  }
}

</style>
