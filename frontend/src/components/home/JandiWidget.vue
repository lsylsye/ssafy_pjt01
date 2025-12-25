<template>
  <div class="glass-panel jandi-widget">
    <div class="widget-header">
      <div class="user-stat">
        <h3>잔디를 심어보세요  🌱</h3>
        <p>{{ nickname }} 님의 잔디북은 어떤 색일까요?</p>
      </div>
      <button class="more" @click="$emit('more')">보러 가기 &gt;</button>
    </div>

    <div class="jandi-grid" aria-label="jandi">
      <div v-for="(lv, idx) in levels" :key="idx" class="cell" :class="`lv-${lv}`"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  count: { type: Number, default: 12 },
  nickname: { type: String, default: "작가" },
  levels: {
    type: Array,
    default: () => Array.from({ length: 80 }, () => Math.floor(Math.random() * 5)),
  },
});
defineEmits(["more"]);
</script>

<style scoped>
.jandi-widget{
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
  overflow: hidden;
  transition: 0.2s;
}
.jandi-widget:hover{
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}

.widget-header{
  display:flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 24px;
}
.user-stat h3{ font-size: 1.5rem; font-weight: 900; margin-bottom: 4px; }
.user-stat p{ color: var(--text-sub); font-size: 0.95rem; font-weight: 400; }
.more{ color: var(--primary); font-weight: 900; }

.jandi-grid{
  display:grid;
  grid-template-columns: repeat(20, 1fr);
  gap: 6px;
}
.cell{
  width: 100%;
  aspect-ratio: 1;
  background: rgba(0,0,0,0.05);
  border-radius: 6px;
  transition: 0.2s;
}
.cell:hover{ transform: scale(1.15); }

.lv-0{ background: rgba(0,0,0,0.05); }
.lv-1{ background: #d1f7c4; }
.lv-2{ background: #66e095; }
.lv-3{ background: #00d15b; box-shadow: 0 0 8px rgba(0,209,91,0.4); }
.lv-4{ background: #008f3e; box-shadow: 0 0 10px rgba(0,143,62,0.5); }

@media (max-width: 700px){
  .jandi-widget{ padding: 22px; }
  .jandi-grid{ grid-template-columns: repeat(14, 1fr); }
}
</style>
