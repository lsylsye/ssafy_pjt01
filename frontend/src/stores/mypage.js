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

    // ✅ 새로고침 없이 즉시 반영: 레벨/경험치만 부분 업데이트
    patchLevel(payload) {
      if (!payload) return;

      if (!this.me) this.me = {};
      const next = { ...this.me };

      if (payload.exp_total !== undefined) next.exp_total = payload.exp_total;
      if (payload.level !== undefined) next.level = payload.level;
      if (payload.level_progress !== undefined) next.level_progress = payload.level_progress;

      this.me = next; // ✅ 객체 교체
    },

    // ✅ 새로 추가: 팔로워/팔로잉 카운트 즉시 반영
    patchFollowCounts(payload) {
      if (!payload) return;

      if (!this.me) this.me = {};
      const next = { ...this.me };

      if (payload.followers_count !== undefined) next.followers_count = payload.followers_count;
      if (payload.following_count !== undefined) next.following_count = payload.following_count;

      this.me = next; // ✅ 객체 교체
    },

    // ✅ 서버 값으로 재동기화 (원하면 글/댓글/팔로우 이후 모두 이걸로 정리 가능)
    refreshMe() {
      return this.fetchMe();
    },

    // (기존 이름 호환용) ✅ 레벨 재동기화
    refreshLevel() {
      return this.fetchMe();
    },
  },
});
