<template>
  <div class="result-container">
    <div class="result-card">
      <div class="analysis-section">
        <h3 class="section-title">당신의 독서 DNA</h3>

        <div class="keywords">
          <span v-for="(keyword, index) in keywords" :key="index" class="keyword-tag">
            #{{ keyword }}
          </span>
        </div>

        <p class="analysis-desc">
          당신의 취향을 분석하여<br />
          꼭 맞는 책 {{ books.length }}권을 선정했습니다.
        </p>
      </div>

      <div class="divider"></div>

      <div class="books-wrapper">
        <div
          v-for="(book, index) in books"
          :key="index"
          class="book-card"
          @click="goToDetail(book.isbn13)"
          role="button"
          tabindex="0"
          @keydown.enter="goToDetail(book.isbn13)"
        >
          <div class="badge" :class="index === 0 ? 'badge-primary' : 'badge-secondary'">
            {{ book.type || (index === 0 ? "운명의 책" : "새로운 시도") }}
          </div>

          <div class="cover-area">
            <img v-if="book.cover" :src="book.cover" :alt="book.title" class="book-cover" />
            <div v-else class="book-cover-placeholder">NO IMAGE</div>
          </div>

          <div class="info-area">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author }}</p>

            <div class="ai-reason-box">
              <span class="ai-icon">🤖</span>
              <p class="ai-text">{{ book.reason }}</p>
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
.result-container{
  --primary:#00D15B;
  --primary-dark:#00B84F;
  --bg:#0b1220;
  --glass: rgba(255,255,255,0.10);
  --glass-2: rgba(255,255,255,0.14);
  --border: rgba(255,255,255,0.16);
  --border-2: rgba(255,255,255,0.22);
  --text:#EAF1F7;
  --text-sub: rgba(234,241,247,0.78);
  --text-dim: rgba(234,241,247,0.62);
  --shadow: 0 22px 60px rgba(0,0,0,0.35);
  --shadow-soft: 0 14px 40px rgba(0,0,0,0.22);
  --transition: 0.18s ease;

  min-height: calc(100vh - 80px);
  padding: 56px 20px;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  font-family:"Pretendard",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;

  /* 메인페이지 느낌: 어두운 그라데이션 + 은은한 그린 오로라 */
  background:
    radial-gradient(900px 480px at 20% 12%, rgba(0,209,91,0.22), transparent 62%),
    radial-gradient(860px 520px at 80% 18%, rgba(56,189,248,0.16), transparent 60%),
    radial-gradient(760px 520px at 55% 88%, rgba(168,85,247,0.12), transparent 62%),
    linear-gradient(180deg, #07101f 0%, #090f1b 55%, #070b14 100%);
}

/* 메인 카드(유리판) */
.result-card{
  width:100%;
  max-width: 720px;
  border-radius: 22px;
  padding: 46px 40px;
  position: relative;

  background: linear-gradient(180deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.08) 100%);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  overflow: hidden;
}

/* 유리 하이라이트 */
.result-card::before{
  content:"";
  position:absolute;
  inset: 0;
  background:
    radial-gradient(900px 220px at 20% 0%, rgba(255,255,255,0.18), transparent 55%),
    radial-gradient(700px 240px at 90% 10%, rgba(255,255,255,0.10), transparent 60%);
  pointer-events:none;
}

.section-title{
  position: relative;
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  text-align: center;
  color: var(--text-dim);
  margin: 0 0 18px 0;
}

.keywords{
  position: relative;
  display:flex;
  flex-wrap:wrap;
  justify-content:center;
  gap: 10px;
  margin-bottom: 18px;
}

.keyword-tag{
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 800;

  color: var(--text);
  background: rgba(255,255,255,0.10);
  border: 1px solid rgba(255,255,255,0.16);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);

  box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}

.keyword-tag:hover{
  border-color: rgba(0,209,91,0.30);
  box-shadow: 0 14px 30px rgba(0,0,0,0.22);
}

.analysis-desc{
  position: relative;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-sub);
  line-height: 1.7;
  text-align:center;
  margin: 0;
}

.divider{
  position: relative;
  height: 1px;
  margin: 30px 0 34px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
}

/* 책 카드 레이아웃 */
.books-wrapper{
  position: relative;
  display:flex;
  flex-direction:column;
  gap: 18px;
  margin-bottom: 34px;
}

@media (min-width: 720px){
  .books-wrapper{
    flex-direction: row;
    gap: 18px;
  }
}

/* 개별 책 카드(유리 카드) */
.book-card{
  flex:1;
  border-radius: 18px;
  padding: 26px 22px 22px;
  position: relative;
  cursor: pointer;
  display:flex;
  flex-direction:column;
  align-items:center;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition), background var(--transition);

  background: linear-gradient(180deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.06) 100%);
  border: 1px solid rgba(255,255,255,0.14);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  overflow: hidden;
}

.book-card::before{
  content:"";
  position:absolute;
  inset:-1px;
  background:
    radial-gradient(520px 180px at 15% 0%, rgba(0,209,91,0.16), transparent 55%),
    radial-gradient(520px 180px at 85% 0%, rgba(255,255,255,0.10), transparent 55%);
  opacity: 0.7;
  pointer-events:none;
}

.book-card:hover{
  transform: translateY(-4px);
  border-color: rgba(0,209,91,0.28);
  box-shadow: 0 22px 55px rgba(0,0,0,0.34);
}

/* 배지 */
.badge{
  position:absolute;
  top: 14px;
  left: 14px;
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #fff;
  border: 1px solid rgba(255,255,255,0.18);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 10px 26px rgba(0,0,0,0.25);
  z-index: 2;
}

.badge-primary{
  background: linear-gradient(135deg, rgba(0,209,91,0.95), rgba(0,184,79,0.95));
}
.badge-secondary{
  background: linear-gradient(135deg, rgba(239,68,68,0.95), rgba(244,63,94,0.95));
}

.cover-area{
  position: relative;
  margin-top: 34px;
  margin-bottom: 20px;
}

.book-cover{
  width: 132px;
  height: 184px;
  object-fit: cover;
  border-radius: 12px;

  border: 1px solid rgba(255,255,255,0.18);
  box-shadow: 0 18px 45px rgba(0,0,0,0.35);
}

.book-cover-placeholder{
  width: 132px;
  height: 184px;
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius: 12px;

  color: rgba(234,241,247,0.75);
  font-weight: 600;
  background: rgba(255,255,255,0.08);
  border: 1px dashed rgba(255,255,255,0.22);
  box-shadow: 0 18px 45px rgba(0,0,0,0.28);
}

.info-area{
  position: relative;
  width:100%;
}

.book-title{
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 800;
  color: var(--text);
  line-height: 1.35;
  word-break: keep-all;
  text-align: center;
}

.book-author{
  margin: 0 0 16px 0;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-dim);
  text-align: center;
}

/* AI 추천사 박스(유리 박스) */
.ai-reason-box{
  display:flex;
  gap: 10px;
  align-items:flex-start;

  padding: 14px;
  border-radius: 14px;

  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.14);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);

  color: var(--text-sub);
  line-height: 1.6;
}

.ai-icon{
  font-size: 18px;
  flex-shrink:0;
  margin-top: 1px;
}

.ai-text{
  margin: 0;
  font-size: 13px;
  font-weight: 500;
}

/* 버튼 */
.actions{
  position: relative;
  display:flex;
  justify-content:center;
}

.retry-btn{
  width: 100%;
  padding: 16px 22px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.16);

  color: #fff;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;

  background: linear-gradient(135deg, rgba(0,209,91,0.95), rgba(0,184,79,0.95));
  box-shadow: 0 18px 40px rgba(0,0,0,0.28);
  transition: transform var(--transition), box-shadow var(--transition), filter var(--transition);
}

.retry-btn:hover{
  transform: translateY(-2px);
  box-shadow: 0 22px 55px rgba(0,0,0,0.35);
  filter: brightness(1.02);
}

.retry-btn:active{
  transform: translateY(0);
  box-shadow: 0 18px 40px rgba(0,0,0,0.28);
}

</style>
