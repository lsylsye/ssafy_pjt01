<template>
  <div class="top">
    <router-link :to="`/community/${country}/${board}`" exact-active-class="active" class="list-btn">
      목록
    </router-link>

    <router-link :to="`/community/${country}/${board}/write`" exact-active-class="active" class="write-btn">
      글쓰기
    </router-link>
  </div>
</template>

<script setup>
defineProps({
  country: { type: String, required: true },
  board: { type: String, required: true }, // "free" | "review"
});
</script>

<style scoped>
.top {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  justify-content: center;
  align-items: center;
  border: none;
  padding: 0;
}

.top a {
  text-decoration: none;
  color: var(--text-primary);
  padding: 10px 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-weight: 600;
  font-size: 13px;
  transition: var(--transition);
  cursor: pointer;
  background: #ffffff;
  display: inline-block;
}

.list-btn {
  background: #ffffff !important;
  color: var(--text-primary) !important;
}

.write-btn {
  background: var(--primary-color) !important;
  color: #ffffff !important;
  border-color: var(--primary-color) !important;
}

.write-btn.active {
  background: var(--primary-color) !important;
  color: #ffffff !important;
  border-color: var(--primary-color) !important;
}
</style>
