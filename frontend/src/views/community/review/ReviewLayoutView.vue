<template>
  <section>
    <TopTabs :country="country" board="review" />
    <router-view />
  </section>
</template>

<script setup>
import useCountry from "@/composables/useCountry";
import TopTabs from "@/components/community/TopTabs.vue";

const { country } = useCountry();
</script>
