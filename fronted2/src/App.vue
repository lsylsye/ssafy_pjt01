<template>
  <AppLayout>
    <router-view />
  </AppLayout>

  <AppAlertHost />
</template>

<script setup>
import { onMounted } from "vue";
import AppLayout from "@/layouts/AppLayout.vue";
import AppAlertHost from "@/components/ui/AppAlertHost.vue";
import { useAuthStore } from "@/stores/auth.store";

const authStore = useAuthStore();

onMounted(() => {
  if (authStore.access) {
    authStore.fetchMe();
  }
});
</script>
