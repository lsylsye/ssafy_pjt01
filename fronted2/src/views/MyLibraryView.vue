<template>
  <div class="page">
    <div class="container">
      <!-- 1. 대시보드 상단 그리드 -->
      <div class="dashboard-grid">
        <!-- 프로필 & 레벨 서브 그리드 -->
        <div class="dash-left">
          <section class="profile-card glass-panel">
            <div class="profile-inner">
              <img v-if="me?.profile_image" :src="getAbsoluteUrl(me.profile_image)" class="p-img" />
              <div v-else class="p-img ph"><User :size="24" /></div>
              <div class="p-info">
                <h1 class="p-nick">{{ me?.nickname || '정원사' }}님</h1>
                <p class="p-desc">오늘도 정원을 가꿔볼까요? 🌱</p>
              </div>
            </div>
            <div class="p-stats">
              <div class="stat-item">
                <span class="stat-val">{{ reviews.length }}</span>
                <span class="stat-label">심은 나무</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <span class="stat-val">{{ grassValues.length }}</span>
                <span class="stat-label">활동 일수</span>
              </div>
            </div>
          </section>

          <section class="level-mini-card glass-panel highlight">
            <div class="level-top">
              <div class="icon-floating-wrap">
                <img v-if="stats?.level_icon" :src="getAbsoluteUrl(stats.level_icon)" class="lv-icon" />
                <div v-else class="lv-icon ph">🌱</div>
                <div class="lv-shadow"></div>
              </div>
              <div class="lv-info">
                <span class="lv-badge">Level {{ stats?.level || 1 }}</span>
                <h2 class="lv-title">{{ stats?.level_title || '성장하는 씨앗' }}</h2>
              </div>
            </div>
            <div class="lv-progress">
              <div class="prog-label">성장도 <strong>{{ Math.round((stats?.level_progress || 0) * 100) }}%</strong></div>
              <div class="prog-track">
                <div class="prog-fill" :style="{ width: `${(stats?.level_progress || 0) * 100}%` }">
                  <div class="prog-glow"></div>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- 잔디밭 섹션 -->
        <section class="grass-card glass-panel">
          <div class="card-head">
            <h3 class="card-title">활동 잔디밭</h3>
            <span class="card-sub">최근 1년의 기록</span>
          </div>
          <div class="grass-wrap">
            <CalendarHeatmap
              v-if="grassValues.length"
              :values="grassValues"
              :end-date="grassEndDate"
              :range-color="grassColors"
              :max="grassMax"
              :round="2"
              class="custom-heatmap"
            />
            <div v-else-if="loading" class="grass-placeholder animate-pulse">데이터 로딩 중...</div>
            <div v-else class="grass-placeholder">아직 심은 잔디가 없어요. 첫 나무를 심어보세요!</div>
          </div>
        </section>
      </div>

      <!-- 2. 탭 컨트롤 -->
      <div class="tab-control">
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'review' }"
          @click="activeTab = 'review'"
        >
          📝 리뷰 목록
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'garden' }"
          @click="activeTab = 'garden'"
        >
          📅 월별 캘린더
        </button>
      </div>

      <!-- 3. 하단 컨텐츠 -->
      <div v-if="activeTab === 'review'" class="section-content animate-in">
        <!-- 리뷰 목록 (기존과 동일하되 콤팩트하게) -->
        <div v-if="loading" class="loading-state">기록을 불러오는 중...</div>
        <div v-else-if="reviews.length === 0" class="empty-state">아직 작성한 리뷰가 없습니다.</div>
        <div v-else class="review-grid">
          <div v-for="rev in sortedReviews" :key="rev.id" class="rev-item" @click="goBookDetail(rev.isbn13)">
            <div class="rev-cover-box">
              <img :src="rev.cover" alt="" />
              <div class="rev-spine"></div>
            </div>
            <div class="rev-main">
              <div class="rev-top">
                <span class="rev-title">{{ rev.book_title }}</span>
                <span class="rev-star">★ {{ rev.rating }}</span>
              </div>
              <p class="rev-txt">{{ rev.content }}</p>
              <span class="rev-date">{{ formatDate(rev.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'garden'" class="section-content animate-in">
        <div class="calendar-card glass-panel">
          <div class="calendar-header">
            <button class="nav-btn" @click="prevMonth">◀</button>
            <span class="month-title">{{ currentYear }}년 {{ currentMonth + 1 }}월</span>
            <button class="nav-btn" @click="nextMonth">▶</button>
          </div>
          <div class="calendar-grid">
            <div class="day-label sun">일</div> <div class="day-label">월</div> <div class="day-label">화</div>
            <div class="day-label">수</div> <div class="day-label">목</div> <div class="day-label">금</div>
            <div class="day-label sat">토</div>
            <div 
              v-for="(day, idx) in calendarDays" :key="idx" class="day-cell"
              :class="{ 'not-current': !day.isCurrentMonth, 'filled': day.featuredReview }"
              :style="day.featuredReview ? { backgroundImage: `url(${day.featuredReview.cover})` } : {}"
              @click="onDayClick(day)"
            >
              <span v-if="!day.featuredReview">{{ day.date }}</span>
              <div v-if="day.featuredReview" class="star-badge">★{{ day.featuredReview.rating }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 날짜별 리뷰 선택 팝업 (모달) -->
    <div v-if="showDayModal" class="modal-overlay" @click.self="showDayModal = false">
      <div class="modal-content glass-panel">
        <header class="modal-header">
          <h3>{{ selectedDay?.fullDate }} 기록들</h3>
          <button class="close-btn" @click="showDayModal = false">✕</button>
        </header>
        <div class="modal-body">
          <p class="modal-desc">대표로 보여줄 책을 선택하세요.</p>
          <div class="day-review-list">
            <div 
              v-for="rev in selectedDayReviews" 
              :key="rev.id"
              class="day-review-item"
              :class="{ selected: selectedDay?.featuredReview?.id === rev.id }"
              @click="setFeaturedReview(rev)"
            >
              <img :src="rev.cover" class="day-mini-cover" />
              <div class="day-rev-info">
                 <div class="day-rev-title">{{ rev.book_title }}</div>
                 <div class="day-rev-rating">★ {{ rev.rating }}</div>
              </div>
              <div class="check-icon" v-if="selectedDay?.featuredReview?.id === rev.id">
                <Check :size="16" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.store';
import { getMyPageStats } from '@/api/mypage';
import { getMyReviews } from '@/api/review';
import { getMyGrass, getMyLevel } from '@/api/grass';
import { CalendarHeatmap } from "vue3-calendar-heatmap";
import "vue3-calendar-heatmap/dist/style.css";
import { User, Check } from 'lucide-vue-next';

const router = useRouter();
const authStore = useAuthStore();

const me = computed(() => authStore.me);
const activeTab = ref('review');
const loading = ref(true);
const stats = ref(null);
const reviews = ref([]);

// 잔디 데이터
const grassValues = ref([]);
const grassEndDate = ref("");
const grassMax = ref(10);
const grassColors = ["#f3f4f6", "#d1fae5", "#6ee7b7", "#10b981", "#047857"];

// 캘린더 관련
const now = new Date();
const currentYear = ref(now.getFullYear());
const currentMonth = ref(now.getMonth());

// 팝업
const showDayModal = ref(false);
const selectedDay = ref(null);
const forcedFeatured = ref({});

const sortedReviews = computed(() => {
  return [...reviews.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
});

onMounted(async () => {
  if (!authStore.access) {
     router.push('/login');
     return;
  }
  
  try {
    loading.value = true;
    const [levelRes, userRes, grassRes, reviewsRes] = await Promise.all([
      getMyLevel(),
      authStore.fetchMe(),
      getMyGrass({ year: new Date().getFullYear() }),
      getMyReviews()
    ]);
    
    stats.value = levelRes.data;
    const maxVal = grassRes.data?.cap ?? 10;
    grassMax.value = maxVal;
    
    // 데이터 보정: 0은 회색, 10 이상은 가장 진한 색 유지
    grassValues.value = (grassRes.data?.values || []).map(v => ({
      date: v.date,
      count: v.count > 0 ? Math.min(v.count, maxVal) : 0
    }));
    
    grassEndDate.value = grassRes.data?.end_date || "";
    reviews.value = reviewsRes.data || [];
    
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
});

const getAbsoluteUrl = (url) => {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  return `http://127.0.0.1:8000${url.startsWith('/') ? '' : '/'}${url}`;
};

const getProfileImage = (url) => getAbsoluteUrl(url);

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`;
};

const goBookDetail = (isbn) => {
  if (isbn) router.push(`/books/${isbn}`);
};

/** Calendar Logic **/
const calendarDays = computed(() => {
  const days = [];
  const firstDay = new Date(currentYear.value, currentMonth.value, 1);
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0);
  
  // Previous month padding
  const startDayOfWeek = firstDay.getDay(); 
  const prevMonthLastDay = new Date(currentYear.value, currentMonth.value, 0).getDate();
  for (let i = startDayOfWeek - 1; i >= 0; i--) {
     days.push({
       date: prevMonthLastDay - i,
       isCurrentMonth: false,
       month: currentMonth.value - 1,
       year: currentYear.value
     });
  }
  
  // Current month
  for (let i = 1; i <= lastDay.getDate(); i++) {
     const dateStr = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
     const dayReviews = reviews.value.filter(r => r.created_at.startsWith(dateStr));
     
     let featured = null;
     if (dayReviews.length > 0) {
        const forcedId = forcedFeatured.value[dateStr];
        if (forcedId) {
           featured = dayReviews.find(r => r.id === forcedId) || dayReviews[dayReviews.length - 1];
        } else {
           featured = dayReviews[dayReviews.length - 1]; // Last review of the day
        }
     }

     days.push({
       date: i,
       isCurrentMonth: true,
       fullDate: dateStr,
       featuredReview: featured,
       reviews: dayReviews
     });
  }
  
  // Next month padding
  const totalCells = 42;
  const remainingCells = totalCells - days.length;
  for (let i = 1; i <= remainingCells; i++) {
     days.push({
       date: i,
       isCurrentMonth: false,
       month: currentMonth.value + 1,
       year: currentYear.value
     });
  }
  
  return days;
});

const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11;
    currentYear.value--;
  } else {
    currentMonth.value--;
  }
};

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0;
    currentYear.value++;
  } else {
    currentMonth.value++;
  }
};

const onDayClick = (day) => {
  if (day.featuredReview) {
    selectedDay.value = day;
    showDayModal.value = true;
  }
};

const selectedDayReviews = computed(() => {
  return selectedDay.value?.reviews || [];
});

const setFeaturedReview = (rev) => {
  if (!selectedDay.value) return;
  forcedFeatured.value[selectedDay.value.fullDate] = rev.id;
  showDayModal.value = false;
};
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f8fafb;
  padding: 40px 0 100px;
}
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 공통 패널 */
.glass-panel { background: white; border-radius: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.02); border: 1px solid white; }

/* 1. 대시보드 그리드 */
.dashboard-grid {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

/* 왼쪽 열: 프로필 + 레벨 */
.dash-left {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 프로필 카드 */
.profile-card {
  padding: 24px;
}
.profile-inner {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}
.p-img {
  width: 56px; height: 56px; border-radius: 50%; object-fit: cover;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.p-img.ph {
  background: #f0fdf4; display: flex; align-items: center; justify-content: center; color: #00d15b;
}
.p-nick { font-size: 1.25rem; font-weight: 850; margin: 0; color: #191f28; }
.p-desc { font-size: 0.85rem; color: #8b95a1; margin: 4px 0 0; }

.p-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 16px;
  border-top: 1px solid #f2f4f6;
}
.stat-item { text-align: center; display: flex; flex-direction: column; }
.stat-val { font-size: 1.15rem; font-weight: 800; color: #191f28; }
.stat-label { font-size: 0.75rem; color: #8b95a1; margin-top: 4px; }
.stat-divider { width: 1px; background: #f2f4f6; }

/* 레벨 카드 */
.level-mini-card.highlight {
  padding: 24px;
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
  border: 1px solid rgba(0,209,91,0.15);
}
.level-top {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}
.icon-floating-wrap { position: relative; width: 64px; }
.lv-icon { 
  width: 60px; height: 60px; object-fit: contain; 
  animation: float 3s ease-in-out infinite;
}
.lv-shadow {
  width: 30px; height: 4px; background: rgba(0,0,0,0.05); border-radius: 50%;
  position: absolute; bottom: -8px; left: 15px;
  animation: shadow-pulse 3s ease-in-out infinite;
}
.lv-badge { 
  font-size: 0.75rem; font-weight: 800; color: #00d15b; 
  background: rgba(0,209,91,0.1); padding: 2px 8px; border-radius: 99px;
}
.lv-title { font-size: 1.1rem; font-weight: 850; margin: 6px 0 0; color: #191f28; }

.lv-progress { width: 100%; }
.prog-label { font-size: 0.85rem; color: #4e5968; margin-bottom: 8px; }
.prog-label strong { color: #00d15b; }
.prog-track { height: 8px; background: #e5e8eb; border-radius: 99px; overflow: hidden; }
.prog-fill { 
  height: 100%; background: linear-gradient(90deg, #00d15b, #00ff6f); 
  border-radius: 99px; position: relative; transition: width 1s ease-out;
}
.prog-glow {
  position: absolute; top: 0; height: 100%; width: 20px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: shimmer 1.5s infinite;
}

/* 잔디 카드 */
.grass-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
}
.card-head { margin-bottom: 20px; }
.card-title { font-size: 1.2rem; font-weight: 850; color: #191f28; margin: 0; }
.card-sub { font-size: 0.85rem; color: #8b95a1; }
.grass-wrap { 
  flex: 1; display: flex; align-items: center; justify-content: center; 
  overflow-x: auto; 
}
.custom-heatmap { width: 100%; max-width: 700px; padding: 10px 0; }
.grass-placeholder { color: #b0b8c1; font-weight: 600; font-size: 0.95rem; }

/* 2. 탭 컨트롤 */
.tab-control {
  display: flex; gap: 12px; margin-bottom: 24px; 
  padding: 6px; background: #eee; border-radius: 16px; width: fit-content;
}
.tab-btn {
  padding: 10px 24px; border: none; border-radius: 12px; font-weight: 800; color: #8b95a1;
  background: transparent; cursor: pointer; transition: 0.2s; font-size: 0.95rem;
}
.tab-btn.active { background: white; color: #191f28; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

/* 3. 리스트 영역 */
.animate-in {
  animation: fadeIn 0.4s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #8b95a1;
  font-weight: 600;
}

.review-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px;
}
.rev-item {
  background: white; padding: 16px; border-radius: 20px; display: flex; gap: 16px;
  border: 1px solid rgba(0,0,0,0.03); cursor: pointer; transition: 0.2s;
}
.rev-item:hover { transform: translateY(-4px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }

.rev-cover-box { 
  position: relative; width: 60px; height: 90px; flex-shrink: 0; border-radius: 2px 6px 6px 2px;
  overflow: hidden; box-shadow: 3px 5px 12px rgba(0,0,0,0.1);
}
.rev-cover-box img { width: 100%; height: 100%; object-fit: cover; }
.rev-spine {
  position: absolute; top: 0; left: 0; bottom: 0; width: 4px;
  background: linear-gradient(to right, rgba(0,0,0,0.2), transparent);
}

.rev-main { flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
.rev-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.rev-title { font-weight: 850; font-size: 0.95rem; color: #191f28; line-clamp: 1; -webkit-line-clamp: 1; overflow: hidden; display: -webkit-box; -webkit-box-orient: vertical; }
.rev-star { color: #FFD700; font-size: 0.85rem; font-weight: 800; }
.rev-txt { font-size: 0.85rem; color: #4e5968; line-height: 1.5; margin-bottom: 8px; line-clamp: 2; -webkit-line-clamp: 2; overflow: hidden; display: -webkit-box; -webkit-box-orient: vertical; }
.rev-date { font-size: 0.75rem; color: #adb5bd; }

/* 애니메이션 */
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes shadow-pulse { 0%, 100% { transform: scale(1); opacity: 0.2; } 50% { transform: scale(1.3); opacity: 0.1; } }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(300%); } }

@media (max-width: 1024px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .grass-wrap { justify-content: flex-start; }
}

/* 기존 나머지 디자인 유지 */
.calendar-card {
  max-width: 600px;
  margin: 0 auto;
  padding: 30px;
}
.calendar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding: 0 10px; }
.nav-btn { background: none; border: none; cursor: pointer; color: #8b95a1; font-size: 1.1rem; width: 36px; height: 36px; border-radius: 50%; }
.nav-btn:hover { background: #f2f4f6; color: #191f28; }
.month-title { font-size: 1.2rem; font-weight: 850; }
.calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }
.day-label { text-align: center; color: #8b95a1; font-weight: 700; font-size: 0.8rem; padding-bottom: 15px; }
.day-label.sun { color: #ff6b6b; }
.day-label.sat { color: #4d96ff; }
.day-cell { aspect-ratio: 1/1.4; border-radius: 8px; background: #f2f4f6; display: flex; align-items: center; justify-content: center; color: #adb5bd; font-weight: 700; position: relative; cursor: pointer; font-size: 0.85rem; }
.day-cell.not-current { opacity: 0.3; pointer-events: none; }
.day-cell.filled { background-size: cover; background-position: center; color: transparent; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
.star-badge { position: absolute; top: 4px; right: 4px; background: rgba(0,0,0,0.6); color: #ffd700; font-size: 0.65rem; padding: 2px 5px; border-radius: 6px; backdrop-filter: blur(2px); font-weight: 800; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { width: 90%; max-width: 400px; padding: 24px; background: white; border-radius: 24px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.modal-header h3 { margin: 0; font-weight: 850; }
.close-btn { background: none; border: none; cursor: pointer; font-size: 1.2rem; color: #8b95a1; }
.modal-desc { font-size: 0.9rem; color: #6b7684; margin-bottom: 20px; }
.day-review-list { display: flex; flex-direction: column; gap: 10px; }
.day-review-item { display: flex; align-items: center; gap: 12px; padding: 10px; border-radius: 14px; background: #f9fafb; cursor: pointer; border: 2px solid transparent; }
.day-review-item.selected { border-color: #00d15b; background: white; }
.day-mini-cover { width: 40px; height: 60px; border-radius: 4px; object-fit: cover; }
.day-rev-info { flex: 1; }
.day-rev-title { font-weight: 800; font-size: 0.9rem; }
.day-rev-rating { color: #FFD700; font-size: 0.8rem; font-weight: 800; }
.check-icon { color: #00d15b; }
</style>
