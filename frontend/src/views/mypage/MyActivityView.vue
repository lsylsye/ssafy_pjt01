<template>
  <section class="activity">
    <MyGrassList />
    <MyActivityList />
  </section>
</template>

<script setup>
import MyGrassList from "@/components/mypage/MyGrassList.vue";
import MyActivityList from "@/components/mypage/MyActivityList.vue";
</script>

<style scoped>
.activity { padding: 12px 0; }
</style>
