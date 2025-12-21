import api from "@/api/axios";

// ✅ 반드시 /api/community 로 맞춰야 함 (지금 404 원인)
const base = (country) => `/api/community/${String(country).toLowerCase()}`;

// 목록 (q 옵션) - 인증 X
export const getReviews = (country, q = "") => {
  const params = {};
  if (q) params.q = q;
  return api.get(`${base(country)}/review/`, { params, auth: false });
};

// 작성 - 인증 O (write 뒤 슬래시 없음)
export const createReview = (country, payload) =>
  api.post(`${base(country)}/review/write`, payload);

// 상세 - 인증 X
export const getReviewDetail = (country, reviewId) =>
  api.get(`${base(country)}/review/${reviewId}/`, { auth: false });

// 수정 - 인증 O
export const patchReview = (country, reviewId, payload) =>
  api.patch(`${base(country)}/review/${reviewId}/`, payload);

// 삭제 - 인증 O
export const deleteReview = (country, reviewId) =>
  api.delete(`${base(country)}/review/${reviewId}/`);

// 좋아요 토글 - 인증 O
export const toggleReviewLike = (country, reviewId) =>
  api.post(`${base(country)}/review/${reviewId}/like/`);

// 댓글 목록 - 인증 X
export const getReviewComments = (country, reviewId) =>
  api.get(`${base(country)}/review/${reviewId}/comments/`, { auth: false });

// 댓글 작성(대댓글 포함) - 인증 O (write 뒤 슬래시 없음)
export const createReviewComment = (country, reviewId, payload) =>
  api.post(`${base(country)}/review/${reviewId}/comments/write`, payload);

// 댓글 삭제(공통) - 인증 O
export const deleteComment = (commentId) =>
  api.delete(`/api/community/comments/${commentId}/`);

// 댓글 좋아요(공통) - 인증 O
export const toggleCommentLike = (commentId) =>
  api.post(`/api/community/comments/${commentId}/like/`);
