import api from "@/api/axios";

const c = (country) => String(country || "kr").toLowerCase();

// list/detail
export const getFreeList = (country, params = {}) =>
  api.get(`/api/community/${c(country)}/free/`, { params });

export const getFreeDetail = (country, postId) =>
  api.get(`/api/community/${c(country)}/free/${postId}/`);

// write/edit/delete
export const createFreePost = (country, payload) =>
  api.post(`/api/community/${c(country)}/free/write/`, payload);

export const patchFreePost = (country, postId, payload) =>
  api.patch(`/api/community/${c(country)}/free/${postId}/`, payload);

export const deleteFreePost = (country, postId) =>
  api.delete(`/api/community/${c(country)}/free/${postId}/`);

// likes
export const toggleFreeLike = (country, postId) =>
  api.post(`/api/community/${c(country)}/free/${postId}/like/`, {});

// comments (free)
export const getFreeComments = (country, postId) =>
  api.get(`/api/community/${c(country)}/free/${postId}/comments/`);

export const writeFreeComment = (country, postId, payload) =>
  api.post(`/api/community/${c(country)}/free/${postId}/comments/write/`, payload);

// shared comment endpoints
export const deleteComment = (commentId) =>
  api.delete(`/api/community/comments/${commentId}/`);

export const toggleCommentLike = (commentId) =>
  api.post(`/api/community/comments/${commentId}/like/`, {});
