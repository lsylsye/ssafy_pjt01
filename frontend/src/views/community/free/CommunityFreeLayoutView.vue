<template>
  <section>
    <div class="top">
      <router-link :to="`/community/${country}/free`" exact-active-class="active">
        목록
      </router-link>

      <router-link :to="`/community/${country}/free/write`" exact-active-class="active">
        글쓰기
      </router-link>
    </div>

    <router-view />
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const country = computed(() => String(route.params.country || 'kr'))
</script>

<style scoped>
.top {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}
.top a {
  text-decoration: none;
  color: #444;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.top a.active {
  border-color: #1a73e8;
  color: #1a73e8;
  font-weight: bold;
}
</style>
