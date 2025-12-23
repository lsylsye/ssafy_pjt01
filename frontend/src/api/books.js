// src/api/books.js
import api from "@/api/axios";

export const getNewSpecial = () => {
  return api.get("/api/books/new/special/", { auth: false });
};

// ✅ 추천 시스템1(작가버전): 북마크 기반 (로그인 필요)
export const recommendBookmarkAuthor = () => {
  return api.get("/api/books/recommend/bookmark/"); // auth 기본 true(토큰 첨부)
};
