import { defineStore } from "pinia";

export const useUiStore = defineStore("ui", {
  state: () => ({
    alertOpen: false,
    alertType: "info", // info | success | warning | error
    alertTitle: "알림",
    alertMessage: "",
    alertOkText: "확인",
    alertOnOk: null,
  }),

  actions: {
    openAlert(payload = {}) {
      this.alertType = payload.type || "info";
      this.alertTitle = payload.title || "알림";
      this.alertMessage = payload.message || "";
      this.alertOkText = payload.okText || "확인";
      this.alertOnOk = typeof payload.onOk === "function" ? payload.onOk : null;
      this.alertOpen = true;
    },
    closeAlert() {
      this.alertOpen = false;
      this.alertOnOk = null;
    },
    okAlert() {
      const fn = this.alertOnOk;
      this.closeAlert();
      if (fn) fn();
    },
  },
});
