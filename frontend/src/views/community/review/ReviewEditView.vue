<template>
  <div class="wrap">
    <h3>리뷰 수정</h3>

    <div v-if="!auth.isLoggedIn" class="need-login">
      로그인 후 수정할 수 있어요.
      <button @click="goLogin">로그인</button>
    </div>

    <div v-else>
      <div v-if="loading">불러오는 중...</div>

      <form v-else class="form" @submit.prevent="submit">
        <div class="fixed">
          <div class="line">책 제목: {{ book_title || "-" }}</div>
          <div class="line">저자: {{ book_author || "-" }}</div>
        </div>

        <div class="row">
          <label>평점</label>
          <input
            v-model.number="rating"
            type="number"
            min="1"
            max="5"
            placeholder="1~5 (선택)"
          />
        </div>

        <div class="row">
          <label>리뷰 내용</label>
          <textarea v-model="content" placeholder="필수"></textarea>
        </div>

        <div v-if="errorMsg" class="error">{{ errorMsg }}</div>

        <div class="buttons">
          <button type="submit" :disabled="saving">저장</button>
          <button type="button" @click="goBack" :disabled="saving">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getReviewDetail, patchReview } from "@/api/review";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const country = computed(() => String(route.params.country || "kr"));
const reviewId = computed(() => String(route.params.reviewId || ""));

const loading = ref(false);
const saving = ref(false);
const errorMsg = ref("");

const book_title = ref("");
const book_author = ref("");
const rating = ref(null);
const content = ref("");

const fetchDetail = () => {
  errorMsg.value = "";
  loading.value = true;

  getReviewDetail(country.value, reviewId.value)
    .then((res) => {
      const r = res.data || {};
      book_title.value = r.book_title || "";
      book_author.value = r.book_author || "";
      rating.value = r.rating ?? null;
      content.value = r.content || "";
    })
    .catch(() => {
      errorMsg.value = "수정할 리뷰를 불러오지 못했어.";
    })
    .finally(() => {
      loading.value = false;
    });
};

const submit = () => {
  errorMsg.value = "";

  const payload = {
    content: (content.value || "").trim(),
  };

  if (!payload.content) {
    errorMsg.value = "리뷰 내용을 입력해줘.";
    return;
  }

  if (rating.value !== null && rating.value !== "" && !Number.isNaN(Number(rating.value))) {
    payload.rating = Number(rating.value);
  }

  saving.value = true;

  patchReview(country.value, reviewId.value, payload)
    .then(() => {
      router.replace(`/community/${country.value}/review/${reviewId.value}`);
    })
    .catch(() => {
      errorMsg.value = "수정에 실패했어. (권한/필드명/서버 확인)";
    })
    .finally(() => {
      saving.value = false;
    });
};

const goBack = () => router.back();

const goLogin = () => {
  router.push({ path: "/login", query: { redirect: route.fullPath } });
};

watch(
  [country, reviewId, () => auth.isLoggedIn],
  () => {
    if (auth.isLoggedIn) fetchDetail();
  },
  { immediate: true }
);
</script>

<style scoped>
.wrap { padding: 16px; max-width: 720px; }
.need-login { display: flex; gap: 8px; align-items: center; margin-top: 12px; }
.form { display: flex; flex-direction: column; gap: 12px; margin-top: 12px; }
.fixed { padding: 10px; border: 1px solid #eee; border-radius: 10px; background: #fafafa; }
.line { font-size: 13px; color: #444; }
.row { display: flex; flex-direction: column; gap: 6px; }
textarea { min-height: 160px; resize: vertical; }
.buttons { display: flex; gap: 8px; margin-top: 8px; }
.error { color: #c00; font-size: 13px; }
</style>
