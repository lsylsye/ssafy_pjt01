<!-- src/layouts/AppLayout.vue -->
<template>
  <div class="layout">
    <AppNavbar>
      <template #search>
        <SearchCapsule />
      </template>
    </AppNavbar>

    <main class="main">
      <slot />
    </main>
  </div>
</template>

<script setup>
import AppNavbar from "@/components/common/AppNavbar.vue";
import SearchCapsule from "@/components/ui/SearchCapsule.vue";
</script>

<style scoped>
.main {
  min-height: calc(100vh - 70px);
}
</style>
