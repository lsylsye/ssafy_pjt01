// src/stores/mypage.js
import { defineStore } from "pinia";
import api from "@/api/axios";
import { useAuthStore } from "@/stores/auth";

export const useMyPageStore = defineStore("mypage", {
  state: () => ({
    me: null,
    loading: false,
    error: "",
  }),

  actions: {
    fetchMe() {
      const auth = useAuthStore();

      this.loading = true;
      this.error = "";

      return api
        .get("/api/mypage/me/") // 인터셉터가 토큰 자동 첨부d
        .then((res) => {
          this.me = res.data;
          return this.me;
        })
        .catch((err) => {
          const status = err.response?.status;

          if (status === 401) {
            auth.logout();
          }

          this.error = "내 정보를 불러오지 못했습니다.";
          return Promise.reject(err);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
});
