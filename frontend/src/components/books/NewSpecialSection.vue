<template>
  <section class="section">
    <!-- ✅ 베스트셀러 TOP10 타이틀과 동일 스타일 -->
    <h2 class="section-title">{{ label }}</h2>

    <p v-if="store.newSpecialLoading" class="msg">불러오는 중...</p>
    <p v-else-if="store.newSpecialError" class="msg error">{{ store.newSpecialError }}</p>

    <div v-else class="row">
      <BookCard v-for="b in store.newSpecial" :key="b.id" :book="b" />
    </div>
  </section>
</template>

<script setup>
import { onMounted } from "vue";
import { useBooksStore } from "@/stores/books";
import BookCard from "@/components/books/BookCard.vue";

defineProps({
  label: { type: String, default: "주목할 만한 신간" },
});

const store = useBooksStore();

onMounted(() => {
  if (!store.newSpecial || store.newSpecial.length === 0) {
    store.fetchNewSpecial();
  }
});
</script>

<style scoped>
.section {
  margin-top: 48px;
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow-sm);
}

.section-title {
  margin: 0 0 24px;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
  line-height: 1.2;
  color: var(--text-primary);
  position: relative;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--primary-color);
  display: inline-block;
}

.msg {
  margin: 20px 0;
  color: var(--text-secondary);
  text-align: center;
  font-weight: 500;
}

.msg.error {
  color: #ef4444;
}

.row {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 4px 0 12px;
  -webkit-overflow-scrolling: touch;
  scroll-behavior: smooth;
}

.row::-webkit-scrollbar {
  height: 6px;
}

.row::-webkit-scrollbar-track {
  background: var(--bg-secondary);
  border-radius: 3px;
}

.row::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 999px;
}

.row::-webkit-scrollbar-thumb:hover {
  background: var(--primary-dark);
}
</style>
