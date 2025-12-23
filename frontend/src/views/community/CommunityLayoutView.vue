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
section {
  padding: 24px;
  min-height: calc(100vh - 80px);
  background: #ffffff;
}

.boardTabs {
  display: flex;
  gap: 0;
  margin: 0 0 28px;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0;
}

.boardTabs a {
  text-decoration: none;
  color: #999;
  padding: 14px 20px;
  border: none;
  border-bottom: 3px solid transparent;
  border-radius: 0;
  font-weight: 600;
  font-size: 14px;
  transition: var(--transition);
  cursor: pointer;
  position: relative;
}

.boardTabs a:hover {
  color: var(--text-primary);
}

.boardTabs a.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
  font-weight: 700;
}
</style>
