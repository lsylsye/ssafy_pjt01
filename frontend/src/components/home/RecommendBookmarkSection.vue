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
.rec { margin-top: 18px; }
.head { display:flex; align-items:flex-end; justify-content:space-between; gap:12px; }

.section-title {
  margin: 0 0 18px;
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -0.5px;
  line-height: 1.1;
  color: #111;
}

.sub { margin: 6px 0 0; font-size: 12px; color:#666; }

.refresh{
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 10px;
  padding: 8px 12px;
  cursor: pointer;
  font-weight: 600;
}
.refresh:disabled{
  opacity: .6;
  cursor: not-allowed;
}

.list { list-style: none; padding: 0; margin: 12px 0 0; display:flex; flex-direction:column; gap:10px; }
.row {
  display:flex; gap:12px; align-items:flex-start;
  border: 1px solid #eee; border-radius: 12px; padding: 10px;
  cursor: pointer;
}
.row:hover { border-color:#cfd8ff; }
.cover { width: 54px; height: 72px; object-fit: cover; border-radius: 8px; border:1px solid #eee; background:#fafafa; }
.meta { min-width:0; }
.t { margin:0 0 4px; font-weight:700; color:#111; }
.a, .p { margin:0; font-size: 12px; color:#555; }

.empty-msg{
  margin: 14px 0 0;
  padding: 14px;
  border: 1px dashed #ddd;
  border-radius: 12px;
  color: #444;
  background: #fafafa;
  line-height: 1.5;
  font-size: 14px;
}
</style>
