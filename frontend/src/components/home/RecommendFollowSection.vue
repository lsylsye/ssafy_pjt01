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
</style>
