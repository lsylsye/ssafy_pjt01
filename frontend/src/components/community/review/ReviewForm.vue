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
.error { color:#d33; margin:8px 0; }
.form { border:1px solid #eee; border-radius:12px; padding:12px 14px; max-width:860px; }
.row { display:flex; flex-direction:column; gap:6px; margin-bottom:10px; }
.label { font-size:13px; color:#444; }
.input, .textarea { padding:8px 10px; border:1px solid #ddd; border-radius:8px; }
.textarea { min-height:160px; resize:vertical; }
.extra { border:1px solid #eee; border-radius:12px; padding:10px; background:#fafafa; color:#555; font-size:13px; margin-top:10px; }
.actions { display:flex; gap:10px; margin-top:12px; }
.btn { border:1px solid #ddd; background:white; border-radius:8px; padding:8px 12px; cursor:pointer; }
.btn:hover { border-color:#1a73e8; color:#1a73e8; }
.btn:disabled { opacity:.6; cursor:not-allowed; }
</style>
