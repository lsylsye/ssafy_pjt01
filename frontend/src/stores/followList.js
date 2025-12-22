// src/stores/followList.js
import { defineStore } from "pinia";
import api from "@/api/axios";

export const useFollowListStore = defineStore("followList", {
  state: () => ({
    followers: [],
    following: [],
    loadingFollowers: false,
    loadingFollowing: false,
    errorFollowers: "",
    errorFollowing: "",
    togglingId: null, // 버튼 잠금용
  }),

  actions: {
    fetchFollowers(userId) {
      if (!userId) return Promise.reject(new Error("missing userId"));

      this.loadingFollowers = true;
      this.errorFollowers = "";

      return api
        .get(`/api/users/${userId}/followers/`)
        .then((res) => {
          this.followers = Array.isArray(res.data) ? res.data : [];
          return this.followers;
        })
        .catch((err) => {
          console.error("[followers 불러오기 실패]", err.response?.data || err.message);
          this.errorFollowers = "팔로워 목록을 불러오지 못했습니다.";
          return Promise.reject(err);
        })
        .finally(() => {
          this.loadingFollowers = false;
        });
    },

    fetchFollowing(userId) {
      if (!userId) return Promise.reject(new Error("missing userId"));

      this.loadingFollowing = true;
      this.errorFollowing = "";

      return api
        .get(`/api/users/${userId}/following/`)
        .then((res) => {
          this.following = Array.isArray(res.data) ? res.data : [];
          return this.following;
        })
        .catch((err) => {
          console.error("[following 불러오기 실패]", err.response?.data || err.message);
          this.errorFollowing = "팔로잉 목록을 불러오지 못했습니다.";
          return Promise.reject(err);
        })
        .finally(() => {
          this.loadingFollowing = false;
        });
    },

    // 팔로잉 목록에서 "언팔로우" 버튼용 (토글 API)
    unfollow(targetUserId, myIdForReload) {
      if (!targetUserId) return Promise.reject(new Error("missing targetUserId"));

      this.togglingId = targetUserId;

      return api
        .post(`/api/users/${targetUserId}/follow/`)
        .then(() => {
          // 1) 즉시 UI 반영: 목록에서 제거
          this.following = this.following.filter((u) => String(u.id) !== String(targetUserId));

          // 2) 더 안전하게 하려면 재조회(선택)
          if (myIdForReload) {
            return this.fetchFollowing(myIdForReload);
          }
        })
        .catch((err) => {
          console.error("[언팔로우 실패]", err.response?.data || err.message);
          return Promise.reject(err);
        })
        .finally(() => {
          this.togglingId = null;
        });
    },
  },
});
