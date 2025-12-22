<template>
  <section>
    <h2>내 잔디</h2>

    <CalendarHeatmap
      v-if="values.length"
      :values="values"
      :end-date="endDate"
      :range-color="rangeColor"
      :max="maxCount"
      :round="2"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { CalendarHeatmap } from "vue3-calendar-heatmap";
import { getMyGrass } from "@/api/grass";

const values = ref([]);
const endDate = ref("");
const maxCount = ref(10);

const rangeColor = [
  "#f3f4f6", // null: 아주 연한 회색(거의 배경)
  "#ebedf0", // 0: 연한 민트(회색보다 살짝 초록)
  "#c9efdc", // mid
  "#95ddb6", // high
  "#58c98f", // max
];

onMounted(async () => {
  const { data } = await getMyGrass({ year: new Date().getFullYear() });
  values.value = data.values;     // [{date, count}]
  endDate.value = data.end_date;  // "YYYY-MM-DD"
  maxCount.value = data.cap ?? 10;
});
</script>


<style scoped>
.grass { padding: 12px 0; }

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.controls select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.msg { padding: 12px; color: #555; }
.msg.error { color: #c00; }
.vch__container {
  width: 80%;
}
.heatmap {
  overflow-x: auto; /* 화면 좁으면 가로 스크롤 */
  padding: 8px 0;
}
</style>
