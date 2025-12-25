// src/stores/mypage.store.js
import { defineStore } from "pinia";
import api from "@/api/axios"; // 너가 쓰는 axios 인스턴스 경로에 맞춰져 있어야 함

export const useMypageStore = defineStore("mypage", {
  state: () => ({
    me: null,
    posts: [],
    comments: [],
    grass: [],
    loading: false,
    error: "",
  }),

  actions: {
    async fetchMe() {
      this.loading = true;
      this.error = "";
      try {
        const res = await api.get("mypage/me/");
        this.me = res.data || null;
      } catch (err) {
        this.me = null;
        this.error = "내 정보 조회 실패";
      } finally {
        this.loading = false;
      }
    },

    async fetchMyActivity() {
      try {
        const [postsRes, commentsRes] = await Promise.all([
          api.get("mypage/posts/?type=FREE"),
          api.get("mypage/comments/")
        ]);
        this.posts = Array.isArray(postsRes.data) ? postsRes.data : [];
        this.comments = Array.isArray(commentsRes.data) ? commentsRes.data : [];
      } catch (err) {
        console.error("Failed to fetch activity", err);
        this.posts = [];
        this.comments = [];
      }
    },

    async fetchGrass() {
      try {
        const res = await api.get("grass/me/");
        this.grass = res.data?.values || [];
      } catch (err) {
        console.error("Failed to fetch grass", err);
        this.grass = [];
      }
    },

    clear() {
      this.me = null;
      this.posts = [];
      this.comments = [];
      this.grass = [];
      this.loading = false;
      this.error = "";
    },
  },
});
