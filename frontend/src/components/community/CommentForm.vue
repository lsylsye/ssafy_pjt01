<template>
  <div class="row">
    <input v-model="text" class="input" :placeholder="placeholder" @keyup.enter="submit" />
    <button class="btn" :disabled="disabled" @click="submit">등록</button>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  placeholder: { type: String, default: "댓글을 입력하세요" },
  disabled: { type: Boolean, default: false },
});
const emit = defineEmits(["submit"]);

const text = ref("");

const submit = () => {
  const v = text.value.trim();
  if (!v) return;
  emit("submit", v);
  text.value = "";
};
</script>

<style scoped>
.row {
  display: flex;
  gap: 8px;
  margin: 14px 0 16px;
  align-items: stretch;
}

.input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 10px 12px;
  font-size: 13px;
  transition: var(--transition);
  background: #ffffff;
  color: var(--text-primary);
  font-family: inherit;
}

.input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.1);
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
