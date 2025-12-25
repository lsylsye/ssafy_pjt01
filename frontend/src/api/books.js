// src/api/books.js
import api from "@/api/axios";

export const getBookDetail = (isbn13) =>
  api.get(`/books/${isbn13}/`);

export const getAiDetail = (isbn13) =>
  api.get(`/ai_curator/${isbn13}/`);

export const getBookReviews = (isbn13) =>
  api.get(`/books/${isbn13}/reviews/`);

export const toggleBookmark = (isbn13) =>
  api.post(`/books/${isbn13}/bookmark/`);

