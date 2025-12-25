<!-- src/views/TasteTestView.vue -->
<template>
  <div class="page">
    <div class="container">
      <!-- 상단 배너(설문 UI 톤 맞추기용) -->
      <!-- <section class="test-banner">
        <div class="banner-deco"></div>

        <div class="banner-text">
          <h1 class="banner-title">내 독서 취향은 무슨 색일까요?</h1>
          <p class="banner-sub">
            간단한 테스트로 나만의 독서 DNA를 찾아보세요.
          </p>
        </div>

        <div class="banner-cta">
          <div class="step-chip">
            진행률 {{ Math.min(currentStep + 1, totalSteps) }} / {{ totalSteps }}
          </div>
        </div>
      </section> -->

      <!-- 설문 카드 영역 -->
      <transition name="fade" mode="out-in">
        <!-- 로딩 화면 -->
        <div v-if="loading" class="loading-card">
          <div class="spinner"></div>
          <h2 class="loading-title">분석 중입니다...</h2>
          <p class="loading-sub">잠시만요. 당신의 취향을 정리하는 중이에요.</p>
        </div>

        <!-- 테스트 화면 -->
        <div v-else class="survey-card">
          <!-- 진행 바 -->
          <div class="progress-bar-bg" aria-label="progress">
            <div class="progress-bar-fill" :style="{ width: progressPercentage + '%' }"></div>
          </div>

          <!-- 질문 카드 -->
          <div class="question-content">
            <transition name="slide-fade" mode="out-in">
              <div :key="currentStep" class="step-wrapper">
                <div class="header">
                  <div class="q-badge">📖 Q{{ currentQuestion.id }}</div>
                  <h2 class="scenario">{{ currentQuestion.scenario }}</h2>
                  <h3 class="question-text">{{ currentQuestion.question }}</h3>
                </div>

                <div class="options-group">
                  <button
                    v-for="(option, index) in currentQuestion.options"
                    :key="index"
                    class="option-card"
                    type="button"
                    @click="handleSelect(option.value)"
                    :disabled="submitting"
                  >
                    <span class="option-label">{{ option.label }}</span>
                    <span class="option-desc">{{ option.desc }}</span>
                  </button>
                </div>
              </div>
            </transition>
          </div>

          <div class="footer-indicator">
            {{ currentStep + 1 }} / {{ totalSteps }}
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import { questions } from "@/data/questions";

const router = useRouter();

const currentStep = ref(0);
const answers = ref([]);
const loading = ref(false);
const submitting = ref(false);

const totalSteps = questions.length;

const currentQuestion = computed(() => questions[currentStep.value]);
const progressPercentage = computed(() => ((currentStep.value + 1) / totalSteps) * 100);

const handleSelect = async (value) => {
  if (submitting.value) return;

  answers.value.push(value);

  if (currentStep.value < totalSteps - 1) {
    currentStep.value++;
    return;
  }
  await submitResult();
};

const submitResult = async () => {
  loading.value = true;
  submitting.value = true;

  try {
    const res = await api.post("ai_curator/recommend/", { answers: answers.value });

    sessionStorage.setItem("taste_result", JSON.stringify(res.data || {}));
    router.push("/taste/result");
  } catch (error) {
    console.error(error);
    alert("추천 생성에 실패했습니다. 잠시 후 다시 시도해주세요.");
  } finally {
    loading.value = false;
    submitting.value = false;
  }
};
</script>

<style scoped>
/* ===== page tokens (HTML 시안 톤) ===== */
:root{
  --primary: #00d15b;
  --bg: #fafafa;
  --text: #191f28;
}

.page{
  min-height: calc(100vh - 70px);
  /* background Removed to show bg-blobs from layout */
  color: var(--text);
  padding: 32px 0 60px;
  font-family: -apple-system, BlinkMacSystemFont, "Pretendard", sans-serif;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}


.container{
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

/* ===== banner ===== */
.test-banner{
  background: linear-gradient(120deg, #191f28 0%, #2b3340 100%);
  border-radius: 24px;
  padding: 40px 40px;
  color: #fff;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.banner-deco{
  position: absolute;
  width: 320px;
  height: 320px;
  background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
  top: -60%;
  right: -12%;
  opacity: 0.28;
  filter: blur(55px);
}

.banner-text{
  position: relative;
  z-index: 1;
}

.banner-title{
  margin: 0 0 10px 0;
  font-size: 1.9rem;
  font-weight: 800;
  letter-spacing: -0.6px;
  line-height: 1.15;
}

.banner-sub{
  margin: 0;
  opacity: 0.85;
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.45;
}

.banner-cta{
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.step-chip{
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.18);
  padding: 10px 14px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.95rem;
  backdrop-filter: blur(10px);
}

/* ===== survey card ===== */
.survey-card{
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 34px 32px;
  box-shadow: 0 18px 45px rgba(0,0,0,0.2);
  border: 1px solid rgba(255,255,255,0.2);
  min-height: 620px;
  display: flex;
  flex-direction: column;
}

.progress-bar-bg{
  width: 100%;
  height: 8px;
  background: #eceff2;
  border-radius: 999px;
  margin-bottom: 28px;
  overflow: hidden;
}

.progress-bar-fill{
  height: 100%;
  background: var(--primary);
  transition: width 0.35s cubic-bezier(0.25, 1, 0.5, 1);
  border-radius: 999px;
}

.header{
  margin-bottom: 26px;
}

.q-badge{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  font-weight: 800;
  color: var(--text);
  background: rgba(0, 209, 91, 0.10);
  border: 1px solid rgba(0, 209, 91, 0.22);
  padding: 7px 12px;
  border-radius: 999px;
  margin-bottom: 12px;
}

.scenario{
  font-size: 22px;
  font-weight: 800;
  color: var(--text);
  line-height: 1.35;
  margin: 0 0 10px 0;
  letter-spacing: -0.5px;
  word-break: keep-all;
}

.question-text{
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #6b7684;
  line-height: 1.55;
}

/* options */
.options-group{
  display: flex;
  flex-direction: column;
  gap: 14px;
  flex-grow: 1;
}

.option-card{
  width: 100%;
  padding: 20px 22px;
  border: 1px solid #e5e8eb;
  background: #fff;
  border-radius: 18px;
  cursor: pointer;
  text-align: left;
  transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease, background 0.16s ease;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.option-card:hover{
  border-color: rgba(0, 209, 91, 0.55);
  background: #fbfffd;
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0,0,0,0.07);
}

.option-card:active{
  transform: scale(0.985);
}

.option-card:disabled{
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.option-label{
  font-size: 16px;
  font-weight: 800;
  color: #191f28;
}

.option-desc{
  font-size: 14px;
  color: #8b95a1;
  line-height: 1.45;
  font-weight: 400;
}

.footer-indicator{
  margin-top: 18px;
  text-align: center;
  color: #8b95a1;
  font-size: 14px;
  font-weight: 600;
}

/* loading */
.loading-card{
  background: #fff;
  border-radius: 24px;
  padding: 70px 32px;
  box-shadow: 0 18px 45px rgba(0,0,0,0.07);
  border: 1px solid rgba(0,0,0,0.05);
  text-align: center;
}

.loading-title{
  margin: 8px 0 6px 0;
  font-size: 20px;
  font-weight: 800;
  color: #191f28;
}

.loading-sub{
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: #8b95a1;
}

.spinner{
  width: 44px;
  height: 44px;
  border: 4px solid #e5e8eb;
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* transitions */
.slide-fade-enter-active,
.slide-fade-leave-active{
  transition: all 0.32s ease;
}
.slide-fade-enter-from{
  opacity: 0;
  transform: translateX(10px);
}
.slide-fade-leave-to{
  opacity: 0;
  transform: translateX(-10px);
}

.fade-enter-active,
.fade-leave-active{
  transition: opacity 0.35s;
}
.fade-enter-from,
.fade-leave-to{
  opacity: 0;
}

/* responsive */
@media (max-width: 720px){
  .test-banner{
    padding: 28px 22px;
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }
  .banner-title{
    font-size: 1.55rem;
  }
}
</style>
