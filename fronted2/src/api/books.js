// src/api/books.js
import api from "@/api/axios";

export const getBookDetail = (isbn13) =>
  api.get(`/books/${isbn13}/`, { auth: false });

export const getAiDetail = (isbn13) =>
  api.get(`/ai_curator/${isbn13}/`, { auth: false });

export const getBookReviews = (isbn13) =>
  api.get(`/books/${isbn13}/reviews/`, { auth: false });

export const toggleBookmark = (isbn13) =>
  api.post(`/books/${isbn13}/bookmark/`);

