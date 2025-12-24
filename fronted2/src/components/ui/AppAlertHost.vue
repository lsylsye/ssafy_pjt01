<template>
  <teleport to="body">
    <!-- Toasts -->
    <div class="toast-wrap" aria-live="polite" aria-relevant="additions">
      <div
        v-for="t in ui.toasts"
        :key="t.id"
        class="toast"
        :data-variant="t.variant"
        @click="ui.removeToast(t.id)"
        role="status"
      >
        <span class="dot" />
        <span class="msg">{{ t.message }}</span>
      </div>
    </div>

    <!-- Dialog -->
    <div v-if="ui.dialog.open" class="backdrop" @click.self="onBackdrop">
      <div class="dialog" :data-variant="ui.dialog.variant" role="dialog" aria-modal="true">
        <div class="head">
          <div class="badge" />
          <div class="titles">
            <div class="title">{{ ui.dialog.title }}</div>
            <div class="desc" v-if="ui.dialog.message">{{ ui.dialog.message }}</div>
          </div>
        </div>

        <div class="actions">
          <button
            v-if="ui.dialog.mode === 'confirm'"
            class="btn ghost"
            @click="ui.closeDialog(false)"
          >
            {{ ui.dialog.cancelText }}
          </button>

          <button class="btn solid" @click="ui.closeDialog(true)">
            {{ ui.dialog.confirmText }}
          </button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { useUiStore } from "@/stores/ui.store";

const ui = useUiStore();

function onBackdrop() {
  // alert는 배경 클릭 닫기 허용, confirm은 막는 게 안전
  if (ui.dialog.mode === "alert") ui.closeDialog(true);
}
</script>

<style scoped>
/* 톤은 네 시안 변수(토스 느낌) 그대로 맞춤 */
.toast-wrap{
  position: fixed;
  top: 84px;
  right: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 9999;
}
.toast{
  min-width: 240px;
  max-width: 360px;
  padding: 12px 14px;
  border-radius: 18px;
  background: rgba(255,255,255,0.75);
  border: 1px solid rgba(255,255,255,0.55);
  backdrop-filter: blur(18px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.10);
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  animation: pop 0.18s ease-out;
}
.toast .dot{
  width: 10px; height: 10px; border-radius: 50%;
  background: #00d15b;
  box-shadow: 0 0 10px rgba(0,209,91,0.25);
}
.toast[data-variant="danger"] .dot{ background:#ff4040; box-shadow:0 0 10px rgba(255,64,64,0.25); }
.toast[data-variant="warning"] .dot{ background:#ffb020; box-shadow:0 0 10px rgba(255,176,32,0.25); }
.toast[data-variant="info"] .dot{ background:#3b82f6; box-shadow:0 0 10px rgba(59,130,246,0.25); }
.toast .msg{ font-weight: 650; font-size: 0.92rem; color:#191f28; }

@keyframes pop{
  from{ opacity:0; transform: translateY(-8px) scale(0.98); }
  to{ opacity:1; transform: translateY(0) scale(1); }
}

.backdrop{
  position: fixed; inset: 0;
  background: rgba(17,24,39,0.18);
  backdrop-filter: blur(6px);
  display:flex; align-items:center; justify-content:center;
  z-index: 9998;
  padding: 18px;
}
.dialog{
  width: min(520px, 100%);
  border-radius: 26px;
  background: rgba(255,255,255,0.82);
  border: 1px solid rgba(255,255,255,0.55);
  backdrop-filter: blur(22px);
  box-shadow: 0 24px 70px rgba(0,0,0,0.14);
  padding: 22px 20px 18px;
  animation: pop 0.18s ease-out;
}
.head{
  display:flex; gap: 12px;
  align-items:flex-start;
}
.badge{
  width: 12px; height: 12px; border-radius: 50%;
  margin-top: 6px;
  background: #00d15b;
  box-shadow: 0 0 14px rgba(0,209,91,0.22);
}
.dialog[data-variant="danger"] .badge{ background:#ff4040; box-shadow:0 0 14px rgba(255,64,64,0.22); }
.dialog[data-variant="warning"] .badge{ background:#ffb020; box-shadow:0 0 14px rgba(255,176,32,0.22); }
.dialog[data-variant="info"] .badge{ background:#3b82f6; box-shadow:0 0 14px rgba(59,130,246,0.22); }

.title{
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.4px;
  color:#191f28;
}
.desc{
  margin-top: 6px;
  font-size: 0.95rem;
  color:#4e5968;
  line-height: 1.55;
}

.actions{
  margin-top: 18px;
  display:flex;
  justify-content:flex-end;
  gap: 10px;
}
.btn{
  height: 42px;
  padding: 0 16px;
  border-radius: 999px;
  font-weight: 800;
  cursor:pointer;
  transition: 0.18s;
}
.btn.ghost{
  background: rgba(242,244,246,0.9);
  border: 1px solid rgba(0,0,0,0.06);
  color:#191f28;
}
.btn.ghost:hover{ transform: translateY(-1px); }
.btn.solid{
  background: #191f28;
  color: white;
}
.btn.solid:hover{
  background:#00d15b;
  box-shadow: 0 10px 22px rgba(0,209,91,0.28);
  transform: translateY(-1px);
}
</style>
