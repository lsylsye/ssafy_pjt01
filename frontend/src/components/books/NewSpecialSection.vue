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
  margin-top: 28px;
}

/* ✅ MainView의 베스트셀러 타이틀과 동일 */
.section-title {
  margin: 0 0 18px;
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -0.5px;
  line-height: 1.1;
  color: #111;
}

.msg { margin: 8px 0; color: #666; }
.msg.error { color: #d33; }

/* ✅ 가로 카드 */
.row {
  display: flex;
  gap: 22px;
  overflow-x: auto;
  padding: 6px 2px 10px;
  -webkit-overflow-scrolling: touch;
}

.row::-webkit-scrollbar { height: 8px; }
.row::-webkit-scrollbar-thumb { background: #e6e6e6; border-radius: 999px; }
</style>
