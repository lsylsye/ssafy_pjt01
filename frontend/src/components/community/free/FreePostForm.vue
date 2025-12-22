<template>
  <div class="form">
    <input
      v-if="showPrefix"
      v-model="prefixName"
      class="input"
      placeholder="말머리(예: 잡담) - 선택"
      :disabled="prefixDisabled"
    />

    <input v-model="title" class="input" placeholder="제목" />
    <textarea v-model="content" class="textarea" placeholder="내용"></textarea>

    <div class="actions">
      <button class="btn" :disabled="disabled" @click="submit">{{ submitText }}</button>
      <button v-if="showCancel" class="btn" :disabled="disabled" @click="$emit('cancel')">
        취소
      </button>
    </div>

    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  </div>
</template>

<script setup>
import { ref, watchEffect } from "vue";

const props = defineProps({
  initialPrefix: { type: String, default: "" },
  initialTitle: { type: String, default: "" },
  initialContent: { type: String, default: "" },

  showPrefix: { type: Boolean, default: true },
  prefixDisabled: { type: Boolean, default: false },

  submitText: { type: String, default: "등록" },
  showCancel: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  errorMsg: { type: String, default: "" },
});

const emit = defineEmits(["submit", "cancel"]);

const prefixName = ref("");
const title = ref("");
const content = ref("");

watchEffect(() => {
  prefixName.value = props.initialPrefix || "";
  title.value = props.initialTitle || "";
  content.value = props.initialContent || "";
});

const submit = () => {
  const t = title.value.trim();
  const c = content.value.trim();
  if (!t || !c) return;

  emit("submit", {
    prefix_name: props.showPrefix ? (prefixName.value.trim() || null) : undefined,
    title: t,
    content: c,
  });
};
</script>

<style scoped>
.error { color:#d33; }
.form { display:flex; flex-direction:column; gap:10px; max-width:680px; }
.input, .textarea { border:1px solid #ddd; border-radius:10px; padding:10px 12px; }
.textarea { min-height:180px; resize:vertical; }
.actions { display:flex; gap:8px; }
.btn { border:1px solid #ddd; background:white; border-radius:10px; padding:10px 12px; cursor:pointer; }
.btn:hover { border-color:#1a73e8; color:#1a73e8; }
.btn:disabled { opacity:.6; cursor:not-allowed; }
</style>
