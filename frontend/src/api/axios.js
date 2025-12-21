import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// ✅ 요청마다 토큰 자동 첨부 (단, auth:false면 제외)
api.interceptors.request.use((config) => {
  const useAuth = config.auth !== false; // 기본 true, 명시적으로 false면 토큰 미첨부

  if (useAuth) {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
  } else {
    // 혹시 다른 곳에서 Authorization이 들어간 상태면 제거
    if (config.headers && config.headers.Authorization) {
      delete config.headers.Authorization;
    }
  }

  return config;
});

export default api;
