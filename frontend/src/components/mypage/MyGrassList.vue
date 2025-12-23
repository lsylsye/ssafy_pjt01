<template>
  <section class="grass">
    <div class="heatmap">
      <CalendarHeatmap
        v-if="values.length"
        :values="values"
        :end-date="endDate"
        :range-color="rangeColor"
        :max="maxCount"
        :round="2"
      />
      <p v-else class="msg">잔디 데이터가 없습니다.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { CalendarHeatmap } from "vue3-calendar-heatmap";
import { getMyGrass } from "@/api/grass";

const values = ref([]);
const endDate = ref("");
const maxCount = ref(10);

const rangeColor = [
  "#f3f4f6",
  "#ebedf0",
  "#c9efdc",
  "#95ddb6",
  "#58c98f",
];

onMounted(async () => {
  const { data } = await getMyGrass({ year: new Date().getFullYear() }); // 인자 안 받으면 getMyGrass()로
  values.value = data.values || [];
  endDate.value = data.end_date || "";
  maxCount.value = data.cap ?? 10;
});
</script>

<style scoped>
.grass { padding: 12px 0; }
.heatmap { overflow-x: auto; padding: 8px 0; }
.msg { padding: 12px; color: #555; }
.vch__container { width: 80%; }
</style>
