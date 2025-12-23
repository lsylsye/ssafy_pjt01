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
  min-height: calc(100vh - 80px);
  background: linear-gradient(135deg, var(--primary-lighter) 0%, var(--bg-secondary) 100%);
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  padding: 40px 20px;
}

.survey-box {
  width: 100%;
  max-width: 520px;
  background: var(--bg-primary);
  padding: 48px 40px;
  border-radius: 20px;
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
  min-height: 660px;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(34, 197, 94, 0.1);
  backdrop-filter: var(--blur-sm);
}

.progress-bar-bg {
  width: 100%;
  height: 6px;
  background-color: var(--border-color);
  border-radius: 10px;
  margin-bottom: 40px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-dark));
  transition: width 0.4s cubic-bezier(0.25, 1, 0.5, 1);
  box-shadow: 0 0 12px rgba(34, 197, 94, 0.3);
}

.header {
  margin-bottom: 40px;
}

.q-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: var(--primary-dark);
  background: var(--primary-lighter);
  padding: 8px 12px;
  border-radius: 999px;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.scenario {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  margin-bottom: 12px;
  letter-spacing: -0.5px;
  word-break: keep-all;
}

.question-text {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-secondary);
  line-height: 1.6;
}

.options-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex-grow: 1;
  margin: 28px 0;
}

.option-card {
  width: 100%;
  padding: 20px 24px;
  border: 2px solid var(--border-color);
  background: var(--bg-secondary);
  border-radius: 14px;
  cursor: pointer;
  text-align: left;
  transition: var(--transition);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.option-card:hover {
  border-color: var(--primary-color);
  background: var(--primary-lighter);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.option-card:active {
  transform: scale(0.98);
}

.option-label {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.option-desc {
  font-size: 13px;
  color: var(--text-light);
  line-height: 1.4;
  font-weight: 400;
}

.footer-indicator {
  margin-top: 20px;
  text-align: center;
  color: var(--text-light);
  font-size: 13px;
  font-weight: 500;
}

.loading-view {
  text-align: center;
  margin-top: 80px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 20px;
  box-shadow: 0 0 12px rgba(34, 197, 94, 0.2);
}

@keyframes spin {
  to { transform: rotate(360deg); }
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
