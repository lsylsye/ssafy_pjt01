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
.error {
  color: #dc2626;
  background: #fee2e2;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 12px 0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 800px;
  padding: 18px;
  background: #ffffff;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.input,
.textarea {
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 10px 12px;
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
  min-height: 180px;
  resize: vertical;
  line-height: 1.5;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 6px;
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
