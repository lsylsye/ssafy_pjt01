// src/stores/mypage.store.js
import { defineStore } from "pinia";
import api from "@/api/axios"; // 너가 쓰는 axios 인스턴스 경로에 맞춰져 있어야 함

export const useMypageStore = defineStore("mypage", {
  state: () => ({
    me: null,
    loading: false,
    error: "",
  }),

  actions: {
    async fetchMe() {
      this.loading = true;
      this.error = "";
      try {
        // baseURL이 /api/ 라면 "mypage/me/"가 맞고,
        // baseURL이 그냥 서버면 "/api/mypage/me/"로 바꿔줘
        const res = await api.get("mypage/me/");
        this.me = res.data || null;
      } catch (err) {
        this.me = null;
        this.error = "내 정보 조회 실패";
        console.error("[mypage/me 실패]", err?.response?.status, err?.response?.data || err?.message);
      } finally {
        this.loading = false;
      }
    },

    clear() {
      this.me = null;
      this.loading = false;
      this.error = "";
    },
  },
});
