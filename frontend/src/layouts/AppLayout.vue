<template>
  <div class="bg-blobs">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
  </div>

  <AppNavbar v-if="!route.meta.hideHeader" />

  <main :class="['page', { 'bg-gray': route.name === 'community' }]">
    <slot />
  </main>
</template>

<script setup>
import { useRoute } from "vue-router";
import AppNavbar from "@/components/common/AppNavbar.vue";

const route = useRoute();
</script>

<style scoped>
.bg-blobs{
  position:fixed; inset:0;
  z-index:-1; overflow:hidden;
  background:#f9fafb;
}
.blob{
  position:absolute;
  border-radius:50%;
  filter:blur(80px);
  opacity:0.6;
}
.blob-1{
  width:500px;height:500px;
  background:#d4f4dd;
  top:-100px;left:-100px;
  animation:move 20s infinite alternate;
}
.blob-2{
  width:400px;height:400px;
  background:#e0f2fe;
  bottom:-50px;right:-50px;
  animation:move 15s infinite alternate-reverse;
}
@keyframes move{from{transform:translate(0,0);}to{transform:translate(50px,50px);}}

.page{ 
  min-height: 100vh;
  padding-bottom: 80px; 
}
.bg-gray {
  background-color: #f2f4f6;
}
</style>
