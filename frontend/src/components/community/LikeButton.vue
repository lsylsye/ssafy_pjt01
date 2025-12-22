<template>
  <button class="btn" :disabled="disabled" @click="$emit('toggle')">
    {{ liked ? "좋아요 취소" : "좋아요" }}
    <span v-if="typeof count === 'number'"> ({{ count }})</span>
  </button>
</template>

<script setup>
defineProps({
  liked: { type: Boolean, default: false },
  count: { type: Number, default: 0 },
  disabled: { type: Boolean, default: false },
});
defineEmits(["toggle"]);
</script>

<style scoped>
.btn {
  border: 1px solid #ddd;
  background: white;
  border-radius: 10px;
  padding: 8px 12px;
  cursor: pointer;
}
.btn:hover { border-color: #1a73e8; color: #1a73e8; }
.btn:disabled { opacity: .6; cursor: not-allowed; }
</style>
