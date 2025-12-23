<template>
  <section class="rec">
    <div class="head">
      <div>
        <h2 class="section-title">{{ title }}</h2>
        <p class="sub">내 북마크 기반 추천</p>
      </div>

      <button class="refresh" :disabled="loading" @click="refresh">
        {{ loading ? "불러오는 중..." : "새로고침" }}
      </button>
    </div>

    <!-- ✅ item이 0개면 안내 문구 -->
    <p v-if="isEmpty" class="empty-msg">
      해당 작가의 다른 저서가 없습니다. 새로고침하여 주세요.
    </p>

    <!-- ✅ item이 1개 이상이면(1~5 포함) 그대로 보여줌 -->
    <ul v-else class="list">
      <li v-for="b in items" :key="b.isbn13" class="row" @click="goBook(b.isbn13)">
        <img :src="b.cover" class="cover" alt="cover" />
        <div class="meta">
          <p class="t">{{ b.title }}</p>
          <p class="a">{{ b.author }}</p>
          <p class="p">{{ b.publisher }}</p>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { recommendBookmarkAuthor } from "@/api/books";

const router = useRouter();

const pickedAuthor = ref("");
const items = ref([]);
const loading = ref(false);

const isEmpty = computed(() => !Array.isArray(items.value) || items.value.length === 0);

const title = computed(() => {
  if (!pickedAuthor.value) return "추천 도서";
  return `${pickedAuthor.value} 작가의 다른 책 추천`;
});

const goBook = (isbn13) => {
  if (!isbn13) return;
  router.push(`/books/${isbn13}`);
};

const load = () => {
  if (loading.value) return;

  loading.value = true;

  return recommendBookmarkAuthor()
    .then((res) => {
      const data = res.data || {};
      pickedAuthor.value = data.picked_author || "";
      items.value = Array.isArray(data.items) ? data.items : [];
    })
    .catch(() => {
      pickedAuthor.value = "";
      items.value = [];
    })
    .finally(() => {
      loading.value = false;
    });
};

const refresh = () => load();

onMounted(() => {
  load();
});
</script>

<style scoped>
.rec {
  margin-top: 48px;
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow-sm);
}

.head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
}

.section-title {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
  line-height: 1.2;
  color: var(--text-primary);
}

.sub {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 500;
}

.refresh {
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  border-radius: 10px;
  padding: 10px 16px;
  cursor: pointer;
  font-weight: 600;
  font-size: 13px;
  color: var(--text-primary);
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
}

.refresh:hover:not(:disabled) {
  background: var(--primary-lighter);
  border-color: var(--primary-color);
  color: var(--primary-dark);
}

.refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.row {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 14px;
  cursor: pointer;
  transition: var(--transition);
  background: var(--bg-secondary);
  flex: 1;
  min-width: 140px;
  max-width: 180px;
}

.row:hover {
  transform: translateY(-2px);
  border-color: var(--primary-light);
  box-shadow: var(--shadow-md);
  background: var(--bg-primary);
}

.cover {
  width: 80px;
  height: 110px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: var(--bg-tertiary);
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.meta {
  min-width: 0;
  flex: 1;
  text-align: center;
  width: 100%;
}

.t {
  margin: 0 0 6px;
  font-weight: 700;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.4;
}

.a,
.p {
  margin: 0;
  font-size: 12px;
  color: var(--text-light);
  font-weight: 500;
}

.empty-msg {
  margin: 0;
  padding: 20px;
  border: 1px dashed var(--border-color);
  border-radius: 12px;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  line-height: 1.6;
  font-size: 14px;
  text-align: center;
}
</style>
