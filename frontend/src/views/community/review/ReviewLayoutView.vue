<template>
  <section>
    <router-view />
    <TopTabs :country="country" board="review" />
  </section>
</template>

<script setup>
import useCountry from "@/composables/useCountry";
import TopTabs from "@/components/community/TopTabs.vue";

const { country } = useCountry();
</script>
