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
.row { display:flex; gap:8px; margin:10px 0 14px; }
.input { flex:1; border:1px solid #ddd; border-radius:10px; padding:8px 10px; }
.btn { border:1px solid #ddd; background:white; border-radius:10px; padding:8px 12px; cursor:pointer; }
.btn:hover { border-color:#1a73e8; color:#1a73e8; }
.btn:disabled { opacity:.6; cursor:not-allowed; }
</style>
