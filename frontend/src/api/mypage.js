// src/api/mypage.js
import api from "@/api/axios";

export const getMyMe = () => api.get("/api/mypage/me/");
export const getMyPosts = () => api.get("/api/mypage/posts/");
export const getMyComments = () => api.get("/api/mypage/comments/");
