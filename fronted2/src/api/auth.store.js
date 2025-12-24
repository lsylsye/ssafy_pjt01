// src/api/auth.js
import api from "@/api/axios";

const ROOT = "http://127.0.0.1:8000"; 

export function loginApi(payload) {
  // payload: { username, password }
  return api.post("/accounts/login/", payload, {
    baseURL: ROOT,   
    auth: false,
  });
}

export function signupApi(payload) {
  // payload: 백엔드 signup serializer에 맞춰 전달
  return api.post("/accounts/signup/", payload, {
    baseURL: ROOT,   
    auth: false,
  });
}

export function meApi() {
  return api.get("mypage/me/");
}
