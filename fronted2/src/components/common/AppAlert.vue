<template>
  <teleport to="body">
    <div v-if="alert.isOpen" class="overlay" @click.self="alert.close()">
      <div class="modal glass">
        <div class="top">
          <div class="badge" :data-type="alert.type">{{ typeLabel }}</div>
          <h3 class="title">{{ alert.title }}</h3>
        </div>

        <p class="msg" v-if="alert.message">{{ alert.message }}</p>

        <div class="actions">
          <button class="btn ok" @click="alert.ok()">{{ alert.okText }}</button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { computed } from "vue";
import { useAlertStore } from "@/stores/alert";

const alert = useAlertStore();

const typeLabel = computed(() => {
  const t = alert.type;
  if (t === "success") return "성공";
  if (t === "warning") return "주의";
  if (t === "error") return "오류";
  return "알림";
});
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0;
  background: rgba(15, 23, 42, 0.35);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.glass {
  background: rgba(255,255,255,0.78);
  border: 1px solid rgba(255,255,255,0.5);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow: 0 24px 60px rgba(0,0,0,0.18);
  border-radius: 22px;
}

.modal {
  width: min(420px, 100%);
  padding: 20px 20px 16px;
}

.top { display: grid; gap: 10px; }
.title { font-size: 1.2rem; letter-spacing: -0.3px; }

.badge {
  width: fit-content;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 800;
  color: white;
}
.badge[data-type="info"] { background: #64748b; }
.badge[data-type="success"] { background: var(--primary); }
.badge[data-type="warning"] { background: #f59e0b; }
.badge[data-type="error"] { background: #ef4444; }

.msg {
  margin-top: 10px;
  color: #334155;
  font-weight: 600;
  line-height: 1.6;
}

.actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.btn {
  height: 42px;
  padding: 0 16px;
  border-radius: 999px;
  font-weight: 800;
}
.ok {
  background: #191f28;
  color: white;
}
.ok:hover {
  background: var(--primary);
}
</style>
