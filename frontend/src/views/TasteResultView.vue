<template>
  <div class="result-container">
    <div class="result-card">
      <!-- 1. Hero: My Tree -->
      <div class="tree-hero" :style="gradientStyle">
        <div class="tree-badge" :style="{ backgroundColor: pointColor }">당신과 닮아있는 나무는...</div>
        <h1 class="tree-name">{{ tree.name }}</h1>
        <p class="tree-tagline" :style="{ color: pointColor }">“{{ tree.tagline }}”</p>
        <div class="tree-desc-box">
          <p>{{ tree.description }}</p>
        </div>
      </div>

      <!-- 2. DNA Keywords -->
      <div class="dna-section">
        <h3 class="section-title"># {{ userNickname }}님의 독서 DNA</h3>
        <div class="tags-container">
          <span v-for="(keyword, index) in keywords" :key="index" class="hashtag">
            #{{ keyword }}
          </span>
        </div>
      </div>

      <div class="divider"></div>

      <!-- 3. Recommendation List -->
      <div class="recommend-section">
        <h3 class="section-title">당신을 위한 5권의 책</h3>
        <p class="section-sub">당신의 결에 맞춘 특별한 북 큐레이션입니다.</p>

        <div class="recommendation-list">
          <div
            v-for="(book, index) in books"
            :key="index"
            class="book-row-card"
            :class="{ 'fate-card': index === 0 }"
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
import { useAuthStore } from "@/stores/auth.store";

const router = useRouter();
const authStore = useAuthStore();

const userNickname = computed(() => authStore.me?.nickname || "정원사");

function safeParse(jsonStr) {
  try {
    return JSON.parse(jsonStr);
  } catch {
    return null;
  }
}

const raw = safeParse(sessionStorage.getItem("taste_result")) || {};

const tree = computed(() => {
  return raw.tree || {
    name: "탐구하는 올리브나무",
    tagline: "지혜의 열매를 맺는 차분한 관찰자",
    description: "당신은 지적인 호기심이 강하고 매사를 깊이 있게 들여다보는 성향을 가지고 계시네요. 화려하지는 않지만 묵묵히 자신의 자리를 지키며 깊은 지혜를 나누는 올리브나무와 닮아 있습니다."
  };
});

const analysisText = computed(() => {
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

const pointColor = computed(() => {
  const aiPointColor = tree.value.point_color;
  const name = tree.value.name || "";

  // 1. Priority: AI pointed vibrant color
  if (aiPointColor) return aiPointColor;

  // 2. Fallback: Keyword-based vibrant colors
  if (name.includes("벚꽃")) return "#d63384"; // Deep Pink
  if (name.includes("단풍")) return "#c0392b"; // Deep Red
  if (name.includes("올리브")) return "#198754"; // Deep Green
  if (name.includes("은행")) return "#d97706"; // Deep Yellow
  if (name.includes("자작")) return "#0d6efd"; // Deep Blue
  if (name.includes("등나무") || name.includes("보라")) return "#6f42c1"; // Deep Purple
  if (name.includes("소나무") || name.includes("전나무")) return "#064e3b"; // Forest Green
  if (name.includes("야자") || name.includes("바다")) return "#0891b2"; // Teal
  if (name.includes("바오밥")) return "#d35400"; // Deep Orange

  return "#00d15b"; // Default primary
});

const gradientStyle = computed(() => {
  const aiBgColors = tree.value.bg_colors;
  const name = tree.value.name || "";
  
  // Default Mint/Navy subtle
  let baseColors = ["#f0fff4", "#e6fffa"]; 

  // 1. Priority: AI determined subtle colors
  if (Array.isArray(aiBgColors) && aiBgColors.length >= 2) {
    baseColors = [aiBgColors[0], aiBgColors[1]];
  } 
  // 2. Fallback: Keyword-based subtle colors
  else {
    if (name.includes("벚꽃")) baseColors = ["#fff0f6", "#ffdeeb"];
    else if (name.includes("단풍")) baseColors = ["#fff5f5", "#ffe3e3"];
    else if (name.includes("올리브")) baseColors = ["#f0fff4", "#dcfce7"];
    else if (name.includes("은행")) baseColors = ["#fffbeb", "#fef3c7"];
    else if (name.includes("자작")) baseColors = ["#f0f9ff", "#e0f2fe"];
    else if (name.includes("등나무") || name.includes("보라")) baseColors = ["#f5f3ff", "#ede9fe"];
    else if (name.includes("소나무") || name.includes("전나무")) baseColors = ["#f0fdf4", "#dcfce7"];
    else if (name.includes("야자") || name.includes("바다")) baseColors = ["#f0f9ff", "#e0f2fe"];
    else if (name.includes("바오밥")) baseColors = ["#fffaf0", "#ffedd5"];
  }

  // Wrap with white for the subtle "blooming" effect
  const finalColors = ["#ffffff", ...baseColors, "#ffffff"];

  return {
    background: `linear-gradient(135deg, ${finalColors.join(",")})`,
    backgroundSize: "200% 200%",
    animation: "resultGradient 10s ease-in-out infinite"
  };
});

if (!sessionStorage.getItem("taste_result")) {
  router.replace("/taste/test");
}
</script>

<style scoped>
.result-container {
  --primary: #00d15b;
  --bg: #f8fafb;
  --card-bg: rgba(255, 255, 255, 0.95);
  --text-main: #191f28;
  --text-grey: #4e5968;
  --text-light: #8b95a1;

  min-height: calc(100vh - 70px);
  padding: 60px 20px;
  display: flex;
  justify-content: center;
  /* background is handled by :style */
  font-family: "Pretendard", -apple-system, sans-serif;
  overflow-x: hidden;
}

@keyframes resultGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}


.result-card {
  width: 100%;
  max-width: 800px;
  background: var(--card-bg);
  border-radius: 40px;
  padding: 50px;
  box-shadow: 0 30px 100px rgba(0,0,0,0.05);
  border: 1px solid #fff;
}

/* Tree Hero Section */
.tree-hero {
  text-align: center;
  margin-bottom: 50px;
  padding: 40px;
  /* background is dynamic */
  border-radius: 32px;
  border: 1px solid rgba(0, 0, 0, 0.03);
}


.tree-badge {
  display: inline-block;
  background: var(--primary);
  color: white;
  padding: 6px 16px;
  border-radius: 30px;
  font-size: 0.85rem;
  font-weight: 800;
  margin-bottom: 20px;
}
.tree-name {
  font-size: 2.8rem;
  font-weight: 900;
  color: var(--text-main);
  margin-bottom: 12px;
  letter-spacing: -1px;
}
.tree-tagline {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 24px;
}
.tree-desc-box {
  background: white;
  padding: 24px;
  border-radius: 20px;
  color: var(--text-grey);
  line-height: 1.7;
  font-size: 1.05rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

/* DNA Section */
.dna-section {
  margin-bottom: 40px;
}
.section-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 20px;
}
.section-sub {
  color: var(--text-light);
  margin-bottom: 30px;
  font-weight: 500;
}
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.hashtag {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-grey);
  background: #f2f4f6;
  padding: 8px 18px;
  border-radius: 12px;
  transition: 0.2s;
}
.hashtag:hover {
  background: var(--primary);
  color: white;
}

.divider {
  height: 1px;
  background: #f2f4f6;
  margin: 40px 0;
}

/* Recommendation List */
.recommendation-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 50px;
}
.book-row-card {
  display: flex;
  gap: 30px;
  background: #fff;
  padding: 30px;
  border-radius: 28px;
  cursor: pointer;
  transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid #f2f4f6;
}
.book-row-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 209, 91, 0.1);
  border-color: var(--primary);
}
.fate-card {
  border: 2px solid rgba(0, 209, 91, 0.2);
  background: linear-gradient(to right, #ffffff, #f9fffb);
}

.book-cover-wrap {
  position: relative;
  flex-shrink: 0;
}
.book-thumb {
  width: 140px;
  height: 200px;
  border-radius: 16px;
  object-fit: cover;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
.rank-badge {
  position: absolute;
  top: -10px;
  left: -10px;
  width: 36px;
  height: 36px;
  background: var(--text-main);
  color: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
.fate-card .rank-badge { background: var(--primary); }

.book-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.type-tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 800;
  margin-bottom: 12px;
}
.type-tag.destiny { background: #00d15b; color: white; }
.type-tag.challenge { background: #f2f4f6; color: var(--text-grey); }

.display-title {
  font-size: 1.6rem;
  font-weight: 900;
  color: var(--text-main);
  margin-bottom: 6px;
}
.author-label {
  font-size: 1.05rem;
  color: var(--text-light);
  margin-bottom: 20px;
}

.ai-insight {
  margin-top: auto;
  background: #f8fafb;
  padding: 20px;
  border-radius: 18px;
  position: relative;
}
.insight-label {
  font-size: 0.8rem;
  font-weight: 900;
  color: var(--primary);
  margin-bottom: 8px;
  letter-spacing: 0.5px;
}
.insight-content {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--text-main);
  margin: 0;
}

.actions {
  display: flex;
  justify-content: center;
}
.retry-btn {
  padding: 18px 60px;
  border-radius: 20px;
  border: none;
  background: #191f28;
  color: white;
  font-size: 1.1rem;
  font-weight: 800;
  cursor: pointer;
  transition: 0.3s;
}
.retry-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

@media (max-width: 700px) {
  .result-card { padding: 30px; }
  .tree-name { font-size: 2rem; }
  .book-row-card { flex-direction: column; align-items: center; text-align: center; }
  .book-thumb { width: 160px; height: 230px; }
}
</style>
