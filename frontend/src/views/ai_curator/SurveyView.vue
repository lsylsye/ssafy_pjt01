<template>
  <div class="survey-container">

    <!-- 로딩 화면 -->
    <transition name="fade" v-if="loading">
      <div class="loading-view">
        <div class="spinner"></div>
        <h2>분석 중입니다...</h2>
      </div>
    </transition>

    <!-- 테스트 화면 -->
    <div v-else class="survey-box">
      <!-- 진행 바 -->
      <div class="progress-bar-bg">
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
                @click="handleSelect(option.value)"
              >
                <span class="option-label">{{ option.label }}</span>
                <span class="option-desc">{{ option.desc }}</span>
              </button>
            </div>
          </div>
        </transition>
      </div>

      <div class="footer-indicator">{{ currentStep + 1 }} / {{ totalSteps }}</div>
    </div>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, computed } from "vue";
import api from "@/api/axios";
import { questions } from "@/data/questions";

const router = useRouter();
const currentStep = ref(0);
const answers = ref([]);
const loading = ref(false);
const totalSteps = questions.length;

const currentQuestion = computed(() => questions[currentStep.value]);
const progressPercentage = computed(() => ((currentStep.value + 1) / totalSteps) * 100);

const handleSelect = async (value) => {
  answers.value.push(value);

  if (currentStep.value < totalSteps - 1) {
    currentStep.value++;
    return;
  }
  await submitResult();
};

const submitResult = async () => {
  loading.value = true;
  try {
    const response = await api.post('/api/ai_curator/recommend/', {
      answers: answers.value
    });

    router.push({
      name: 'survey-result', 
      state: { resultData: response.data } 
    });

  } catch (error) {
    console.error('분석 실패:', error);
    alert("오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
  } finally {
    loading.value = false;
  }
};

</script>

<style scoped>
.survey-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #F2F4F6;
  font-family: -apple-system, BlinkMacSystemFont, "Pretendard", sans-serif;
  padding: 20px;
}

.survey-box {
  width: 100%;
  max-width: 500px;
  background: white;
  padding: 40px 32px;
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
  min-height: 620px;
  display: flex;
  flex-direction: column;
}

/* 진행 바 */
.progress-bar-bg {
  width: 100%;
  height: 6px;
  background-color: #E5E8EB;
  border-radius: 10px;
  margin-bottom: 40px;
}

.progress-bar-fill {
  height: 100%;
  background-color: #3182F6;
  transition: width 0.4s cubic-bezier(0.25, 1, 0.5, 1);
}

/* 헤더 */
.header {
  margin-bottom: 40px;
}
.q-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 20px;
  font-weight: 700;
  color: #3182F6;
  background: #EEF4FF;
  padding: 6px 10px;
  border-radius: 999px;
  margin-bottom: 14px;
}
.scenario {
  font-size: 24px;
  font-weight: 700;
  color: #191F28;
  line-height: 1.35;
  margin-bottom: 12px;
  letter-spacing: -0.5px;
  word-break: keep-all;
}

.question-text {
  font-size: 17px;
  font-weight: 500;
  color: #6B7684;
  line-height: 1.5;
}

/* 옵션 */
.options-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex-grow: 1;
}

.option-card {
  width: 100%;
  padding: 22px 24px;
  border: 1px solid #E5E8EB;
  background-color: #fff;
  border-radius: 18px;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.option-card:hover {
  border-color: #3182F6;
  background-color: #F8F9FA;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(49, 130, 246, 0.08);
}

.option-card:active {
  transform: scale(0.98);
}

.option-label {
  font-size: 17px;
  font-weight: 700;
  color: #333;
}

.option-desc {
  font-size: 14px;
  color: #8B95A1;
  line-height: 1.4;
  font-weight: 400;
}

/* 하단 번호 */
.footer-indicator {
  margin-top: 30px;
  text-align: center;
  color: #8B95A1;
  font-size: 14px;
}

/* 로딩 & 애니메이션 */
.loading-view {
  text-align: center;
  margin-top: 100px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #E5E8EB;
  border-top-color: #3182F6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.35s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
