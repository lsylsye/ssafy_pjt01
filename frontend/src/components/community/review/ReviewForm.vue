<template>
  <div class="form">
    <div class="row">
      <label class="label">책 제목(필수)</label>
      <input v-model="bookTitle" class="input" :disabled="lockBook" />
    </div>

    <div class="row">
      <label class="label">저자(필수)</label>
      <input v-model="bookAuthor" class="input" :disabled="lockBook" />
    </div>

    <div class="row">
      <label class="label">평점(선택)</label>
      <input v-model.number="rating" class="input" type="number" min="1" max="5" placeholder="1~5" />
    </div>

    <div class="row">
      <label class="label">리뷰 내용(필수)</label>
      <textarea v-model="content" class="textarea" placeholder="리뷰 내용을 입력하세요"></textarea>
    </div>

    <div class="extra" v-if="showExtra">
      <div>isbn13: {{ isbn13 || "-" }}</div>
      <div>출판사: {{ publisher || "-" }}</div>
      <div>출간일: {{ pubDate || "-" }}</div>
    </div>

    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

    <div class="actions">
      <button class="btn" :disabled="disabled" @click="submit">{{ submitText }}</button>
      <button v-if="showCancel" class="btn" :disabled="disabled" @click="$emit('cancel')">취소</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect } from "vue";

const props = defineProps({
  initial: { type: Object, default: () => ({}) }, // book_title, book_author, rating, content, isbn13, publisher, pub_date, cover
  lockBook: { type: Boolean, default: false }, // edit 시 true
  showExtra: { type: Boolean, default: true },
  submitText: { type: String, default: "등록" },
  showCancel: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  errorMsg: { type: String, default: "" },
});
const emit = defineEmits(["submit", "cancel"]);

const bookTitle = ref("");
const bookAuthor = ref("");
const rating = ref(null);
const content = ref("");

const isbn13 = ref("");
const publisher = ref("");
const pubDate = ref("");
const cover = ref("");

watchEffect(() => {
  const i = props.initial || {};
  bookTitle.value = i.book_title || i.bookTitle || "";
  bookAuthor.value = i.book_author || i.bookAuthor || "";
  rating.value = i.rating ?? null;
  content.value = i.content || "";

  isbn13.value = i.isbn13 || "";
  publisher.value = i.publisher || "";
  pubDate.value = i.pub_date || "";
  cover.value = i.cover || "";
});

const submit = () => {
  const payload = {
    book_title: bookTitle.value.trim(),
    book_author: bookAuthor.value.trim(),
    content: content.value.trim(),
  };

  if (!payload.book_title || !payload.book_author || !payload.content) return;

  if (rating.value !== null && rating.value !== "" && !Number.isNaN(Number(rating.value))) {
    payload.rating = Number(rating.value);
  }
  if (isbn13.value) payload.isbn13 = isbn13.value;
  if (publisher.value) payload.publisher = publisher.value;
  if (pubDate.value) payload.pub_date = pubDate.value;
  if (cover.value) payload.cover = cover.value;

  emit("submit", payload);
};
</script>

<style scoped>
.error {
  color: #dc2626;
  background: #fee2e2;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 12px 0;
}

.form {
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 18px;
  max-width: 900px;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}

.label {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 600;
}

.input,
.textarea {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
  font-family: inherit;
  transition: var(--transition);
  background: #ffffff;
  color: var(--text-primary);
}

.input:focus,
.textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.1);
}

.textarea {
  min-height: 160px;
  resize: vertical;
  line-height: 1.5;
}

.extra {
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  padding: 10px 12px;
  background: #f9f9f9;
  color: #666;
  font-size: 12px;
  margin-top: 12px;
  line-height: 1.5;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 14px;
}

.btn {
  border: 1px solid #ddd;
  background: #ffffff;
  border-radius: 6px;
  padding: 10px 16px;
  cursor: pointer;
  color: var(--text-primary);
  font-weight: 500;
  transition: var(--transition);
  font-size: 13px;
}

.btn:hover {
  border-color: var(--primary-color);
  background: #f5f5f5;
  color: var(--primary-color);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
