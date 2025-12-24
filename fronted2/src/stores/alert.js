import { defineStore } from "pinia";

export const useAlertStore = defineStore("alert", {
  state: () => ({
    isOpen: false,
    type: "info",     // info | success | warning | error
    title: "알림",
    message: "",
    okText: "확인",
    onOk: null,
  }),

  actions: {
    open(payload = {}) {
      this.type = payload.type || "info";
      this.title = payload.title || "알림";
      this.message = payload.message || "";
      this.okText = payload.okText || "확인";
      this.onOk = typeof payload.onOk === "function" ? payload.onOk : null;
      this.isOpen = true;
    },
    close() {
      this.isOpen = false;
      this.onOk = null;
    },
    ok() {
      const fn = this.onOk;
      this.close();
      if (fn) fn();
    },
  },
});
