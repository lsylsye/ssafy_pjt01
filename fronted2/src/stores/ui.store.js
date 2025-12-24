import { defineStore } from "pinia";

export const useUiStore = defineStore("ui", {
  state: () => ({
    // Toast
    toasts: [],

    // Dialog
    dialog: {
      open: false,
      mode: "alert", // 'alert' | 'confirm'
      variant: "default", // 'default' | 'danger' | 'warning' | 'info'
      title: "",
      message: "",
      cancelText: "취소",
      confirmText: "확인",
      resolve: null,
    },
  }),

  actions: {
    // --- Toast ---
    addToast({ message, variant = "default", duration = 3000 }) {
      const id = Date.now() + Math.random();
      this.toasts.push({ id, message, variant });
      if (duration > 0) {
        setTimeout(() => this.removeToast(id), duration);
      }
    },
    removeToast(id) {
      const idx = this.toasts.findIndex((t) => t.id === id);
      if (idx !== -1) {
        this.toasts.splice(idx, 1);
      }
    },

    // --- Dialog (Promise-based) ---
    openDialog({
      mode = "alert",
      variant = "default",
      title = "알림",
      message = "",
      cancelText = "취소",
      confirmText = "확인",
    } = {}) {
      return new Promise((resolve) => {
        // 기존 다이얼로그 있으면 닫기 (새 다이얼로그 우선)
        if (this.dialog.open && this.dialog.resolve) {
          this.dialog.resolve(false);
        }

        this.dialog = {
          open: true,
          mode,
          variant,
          title,
          message,
          cancelText,
          confirmText,
          resolve,
        };
      });
    },

    closeDialog(result) {
      if (this.dialog.open && this.dialog.resolve) {
        this.dialog.resolve(result);
      }
      this.dialog.open = false;
      this.dialog.resolve = null;
    },

    // 편의 메서드
    alert(message, title = "알림") {
      return this.openDialog({ mode: "alert", title, message });
    },
    confirm(message, title = "확인", confirmText = "네", cancelText = "아니요") {
      return this.openDialog({ mode: "confirm", title, message, confirmText, cancelText });
    },
  },
});
