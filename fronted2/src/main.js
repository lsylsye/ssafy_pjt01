// src/main.js
import { createApp } from "vue";
import { createPinia } from "pinia";
import "./styles/main.css";
import App from "./App.vue";
import router from "./router";
import api from "@/api/axios";
import { useAuthStore } from "@/stores/auth.store";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

// Axios 요청 인터셉터 설정: 인증 토큰 자동 첨부
api.interceptors.request.use((config) => {
  const useAuth = config.auth !== false;
  if (!useAuth) return config;

  const auth = useAuthStore(pinia);
  const token = auth.access;

  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

app.mount("#app");
