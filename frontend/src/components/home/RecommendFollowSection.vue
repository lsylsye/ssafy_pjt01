<template>
  <!-- ✅ picked_user_id가 null이면 섹션 자체 숨김 -->
  <section v-if="shouldRender" class="rec">
    <div class="head">
      <div>
        <h2 class="section-title">팔로잉 북마크 추천</h2>
        <p class="sub">팔로우한 유저가 최근 북마크한 책 5권</p>
      </div>

      <button class="refresh" :disabled="loading" @click="refresh">
        {{ loading ? "불러오는 중..." : "새로고침" }}
      </button>
    </div>

    <ul class="list">
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
import { recommendFollowBased } from "@/api/books";

const router = useRouter();

const pickedUserId = ref(null);
const items = ref([]);
const loading = ref(false);

// ✅ picked_user_id가 null이면 숨김 (명세)
const shouldRender = computed(() => pickedUserId.value !== null);

const goBook = (isbn13) => {
  if (!isbn13) return;
  router.push(`/books/${isbn13}`);
};

const load = () => {
  if (loading.value) return;

  loading.value = true;

  return recommendFollowBased()
    .then((res) => {
      const data = res.data || {};
      pickedUserId.value =
        data.picked_user_id === null || data.picked_user_id === undefined
          ? null
          : data.picked_user_id;

      items.value = Array.isArray(data.items) ? data.items : [];
    })
    .catch(() => {
      // 실패하면 그냥 숨김 처리
      pickedUserId.value = null;
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
</style>
