// src/api/books.js
import api from "@/api/axios";

// (기존)
export const getNewSpecial = () => {
  return api.get("/api/books/new/special/", { auth: false });
};

// (기존 추천1)
export const recommendBookmarkAuthor = () => {
  return api.get("/api/books/recommend/bookmark/");
};

// ✅ 추천2(팔로잉버전)
export const recommendFollowBased = () => {
  return api.get("/api/books/recommend/follow/");
};
