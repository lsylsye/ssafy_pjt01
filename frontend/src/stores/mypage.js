// src/stores/mypage.js
import { defineStore } from "pinia";
import { getMyMe } from "@/api/mypage";

export const useMyPageStore = defineStore("mypage", {
  state: () => ({
    me: null,
    loading: false,
    error: "",
  }),

  actions: {
    // ✅ /api/mypage/me/ 불러오기 (then/catch)
    fetchMe() {
      this.loading = true;
      this.error = "";

      return getMyMe()
        .then((res) => {
          this.me = res.data; // ✅ 통째로 교체(반응성 확실)
          return res.data;
        })
        .catch((err) => {
          this.error = "내 정보를 불러오지 못했습니다.";
          throw err;
        })
        .finally(() => {
          this.loading = false;
        });
    },

    // ✅ 새로고침 없이 즉시 반영: 레벨/경험치만 부분 업데이트 (반응성 확실하게 통째로 교체)
    patchLevel(payload) {
      if (!payload) return;

      if (!this.me) this.me = {};

      const next = { ...this.me };

      if (payload.exp_total !== undefined) next.exp_total = payload.exp_total;
      if (payload.level !== undefined) next.level = payload.level;
      if (payload.level_progress !== undefined) next.level_progress = payload.level_progress;

      this.me = next; // ✅ 객체 교체
    },

    // ✅ 서버 값으로 재동기화 (글/댓글 작성 후 최신 레벨을 확실히 받고 싶을 때)
    refreshLevel() {
      return this.fetchMe();
    },
  },
});
