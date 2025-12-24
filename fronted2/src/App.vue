<template>
  <AppLayout>
    <router-view />
  </AppLayout>

  <AppAlertHost />
</template>

<script setup>
import AppLayout from "@/layouts/AppLayout.vue";
import AppAlertHost from "@/components/ui/AppAlertHost.vue";
</script>
