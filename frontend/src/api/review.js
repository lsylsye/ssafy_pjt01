import api from "@/api/axios";

const c = (country) => String(country || "kr").toLowerCase();

// list/detail
export const getReviewList = (country, params = {}) =>
  api.get(`/api/community/${c(country)}/review/`, { params, auth: false });

export const getReviewDetail = (country, reviewId) =>
  api.get(`/api/community/${c(country)}/review/${reviewId}/`, { auth: false });

// write/edit/delete
export const createReview = (country, payload) =>
  api.post(`/api/community/${c(country)}/review/write/`, payload);

export const patchReview = (country, reviewId, payload) =>
  api.patch(`/api/community/${c(country)}/review/${reviewId}/`, payload);

export const deleteReview = (country, reviewId) =>
  api.delete(`/api/community/${c(country)}/review/${reviewId}/`);

// likes
export const toggleReviewLike = (country, reviewId) =>
  api.post(`/api/community/${c(country)}/review/${reviewId}/like/`, {});

// comments (review)
export const getReviewComments = (country, reviewId) =>
  api.get(`/api/community/${c(country)}/review/${reviewId}/comments/`);

export const createReviewComment = (country, reviewId, payload) =>
  api.post(`/api/community/${c(country)}/review/${reviewId}/comments/write/`, payload);

// shared comment endpoints
export const deleteComment = (commentId) =>
  api.delete(`/api/community/comments/${commentId}/`);

export const toggleCommentLike = (commentId) =>
  api.post(`/api/community/comments/${commentId}/like/`, {});
