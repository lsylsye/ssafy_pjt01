// src/stores/auth.store.js
import { defineStore } from "pinia";
import { loginApi, signupApi, meApi } from "@/api/auth.store";

function pickErrorMessage(err) {
  const data = err?.response?.data;
  if (!data) return err?.message || "요청에 실패했습니다.";

  if (typeof data === "string") return data;

  // dj-rest-auth는 보통 {key: ["msg"]} 형태
  const firstKey = Object.keys(data)[0];
  const v = data[firstKey];

  if (Array.isArray(v) && v.length) return v[0];
  if (typeof v === "string") return v;

  return "요청에 실패했습니다.";
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    access: localStorage.getItem("access_token") || "",
    refresh: localStorage.getItem("refresh_token") || "",
    me: null,
    loading: false,
    error: "",
  }),

  actions: {
    setTokens({ access, refresh }) {
      this.access = access || "";
      this.refresh = refresh || "";
      if (this.access) localStorage.setItem("access_token", this.access);
      else localStorage.removeItem("access_token");
      if (this.refresh) localStorage.setItem("refresh_token", this.refresh);
      else localStorage.removeItem("refresh_token");
    },

    async fetchMe() {
      if (!this.access) return null;
      try {
        const res = await meApi();
        this.me = res.data || null;
        return this.me;
      } catch (e) {
        // 토큰 만료 등
        this.me = null;
        return null;
      }
    },

    async login({ username, password }) {
      this.loading = true;
      this.error = "";
      try {
        const res = await loginApi({ username, password });

        // dj-rest-auth 기본 응답: { access, refresh, user... } 또는 key가 다를 수 있음
        const access = res.data?.access || res.data?.access_token || "";
        const refresh = res.data?.refresh || res.data?.refresh_token || "";

        this.setTokens({ access, refresh });
        await this.fetchMe();
        return true;
      } catch (e) {
        this.error = pickErrorMessage(e);
        return false;
      } finally {
        this.loading = false;
      }
    },

    async signup(payload) {
      this.loading = true;
      this.error = "";
      try {
        const res = await signupApi(payload);

        // 회원가입 직후 토큰이 같이 오는 경우가 많음(dj-rest-auth 설정에 따라 다름)
        const access = res.data?.access || res.data?.access_token || "";
        const refresh = res.data?.refresh || res.data?.refresh_token || "";

        if (access || refresh) {
          this.setTokens({ access, refresh });
          await this.fetchMe();
        }

        return true;
      } catch (e) {
        this.error = pickErrorMessage(e);
        return false;
      } finally {
        this.loading = false;
      }
    },

    logout() {
      this.setTokens({ access: "", refresh: "" });
      this.me = null;
      this.error = "";
    },
  },
});
