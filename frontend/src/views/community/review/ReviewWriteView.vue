<template>
  <section class="wrap">
    <BookSearch v-if="showSearch" @select="selectBook" />

    <div v-else class="selectedBar">
      <div class="selectedText">
        선택된 도서: {{ form.book_title || "-" }} / {{ form.book_author || "-" }}
      </div>
      <button class="btn" @click="openSearch">다른 도서 선택</button>
    </div>

    <h3 class="h3">리뷰 작성</h3>

    <ReviewForm
      :initial="form"
      :disabled="saving"
      submit-text="등록"
      :error-msg="errorMsg"
      @submit="submit"
      :show-extra="true"
    />
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

import useCountry from "@/composables/useCountry";
import { useAuthStore } from "@/stores/auth";
import { useReviewStore } from "@/stores/community/review";

import BookSearch from "@/components/community/review/BookSearch.vue";
import ReviewForm from "@/components/community/review/ReviewForm.vue";

const route = useRoute();
const router = useRouter();
const { country } = useCountry();

const auth = useAuthStore();
const store = useReviewStore();

const showSearch = ref(true);
const saving = ref(false);
const errorMsg = ref("");

const form = ref({
  book_title: "",
  book_author: "",
  rating: null,
  content: "",
  isbn13: "",
  publisher: "",
  pub_date: "",
  cover: "",
});

const selectBook = (b) => {
  form.value.book_title = b.title || "";
  form.value.book_author = b.author || "";
  form.value.isbn13 = b.isbn13 || "";
  form.value.publisher = b.publisher || "";
  form.value.pub_date = b.pub_date || "";
  form.value.cover = b.cover || "";
  showSearch.value = false;
};

const openSearch = () => {
  showSearch.value = true;
};

const applyQueryPrefill = () => {
  const q = route.query || {};
  const qt = String(q.book_title || "");
  const qa = String(q.book_author || "");
  if (qt || qa) {
    form.value.book_title = qt;
    form.value.book_author = qa;
    form.value.isbn13 = String(q.isbn13 || "");
    form.value.publisher = String(q.publisher || "");
    form.value.pub_date = String(q.pub_date || "");
    form.value.cover = String(q.cover || "");
    showSearch.value = false;
  }
};

const submit = (payload) => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }

  saving.value = true;
  errorMsg.value = "";

  store
    .createReview(country.value, payload) // ✅ api에서 country 소문자 처리 + write/ 유지
    .then((data) => {
      const id = data?.id;
      router.replace(id ? `/community/${country.value}/review/${id}` : `/community/${country.value}/review`);
    })
    .catch(() => {
      errorMsg.value = "등록에 실패했어.";
    })
    .finally(() => {
      saving.value = false;
    });
};

onMounted(applyQueryPrefill);
</script>

<style scoped>
section {
  padding: 24px;
  min-height: auto;
  max-width: 900px;
  margin: 0 auto;
  background: #ffffff;
}

.wrap {
  max-width: 900px;
}

h3 {
  margin: 0 0 14px;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.selectedBar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin: 0 0 16px;
  padding: 12px 14px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  background: #f9f9f9;
  flex-wrap: wrap;
}

.selectedText {
  color: var(--text-primary);
  font-size: 13px;
  flex: 1;
  min-width: 200px;
}

.btn {
  border: 1px solid #ddd;
  background: #ffffff;
  border-radius: 6px;
  padding: 8px 12px;
  cursor: pointer;
  color: var(--text-primary);
  font-weight: 500;
  transition: var(--transition);
  font-size: 12px;
}

.btn:hover {
  border-color: var(--primary-color);
  background: #f5f5f5;
  color: var(--primary-color);
}
</style>
