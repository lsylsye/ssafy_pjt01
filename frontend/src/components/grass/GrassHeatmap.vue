<template>
  <section>
    <calendar-heatmap
      v-if="values.length"
      :values="values"
      :end-date="endDate"
      :round="2"
    />
    <p v-else>잔디 데이터가 없어요.</p>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getMyGrass } from "@/api/grass";

const values = ref([]);
const endDate = ref("");

onMounted(async () => {
  const { data } = await getMyGrass(); // /api/grass/me/
  endDate.value = data.end_date;       // "2025-12-22"
  values.value = data.values;          // [{date,count}, ...]
});
</script>
