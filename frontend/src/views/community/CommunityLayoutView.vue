<template>
  <section>
    <div class="boardTabs">
      <router-link :to="`/community/${country}/free`" exact-active-class="active">자유</router-link>
      <router-link :to="`/community/${country}/review`" exact-active-class="active">리뷰</router-link>
    </div>

    <router-view />
  </section>
</template>

<script setup>
import useCountry from "@/composables/useCountry";
const { country } = useCountry();
</script>

<style scoped>
.boardTabs { display:flex; gap:10px; margin: 0 0 14px; }
.boardTabs a { text-decoration:none; color:#444; padding:6px 10px; border:1px solid #ddd; border-radius:8px; }
.boardTabs a.active { border-color:#1a73e8; color:#1a73e8; font-weight:700; }
</style>
