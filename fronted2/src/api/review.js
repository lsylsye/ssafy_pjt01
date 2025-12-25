import api from "@/api/axios";

/**
 * GET /api/review/
 */
export function getReviews() {
    const token = localStorage.getItem("access_token");
    const config = {};
    if (token) {
        config.headers = { Authorization: `Bearer ${token}` };
    }
    return api.get("review/", config);
}

/**
 * POST /api/review/write/
 * payload: { book_title, book_author, content, rating, ... }
 */
export function createReview(payload) {
    return api.post("review/write/", payload);
}

/**
 * GET /api/review/{review_id}/
 */
export function getReviewDetail(reviewId) {
    const token = localStorage.getItem("access_token");
    const config = {};
    if (token) {
        config.headers = { Authorization: `Bearer ${token}` };
    }
    return api.get(`review/${reviewId}/`, config);
}

/**
 * POST /api/review/{review_id}/like/
 */
export function toggleReviewLike(reviewId) {
    return api.post(`review/${reviewId}/like/`, {});
}

/**
 * GET /api/review/{review_id}/comments/
 */
export function getReviewComments(reviewId) {
    const token = localStorage.getItem("access_token");
    const config = {};
    if (token) {
        config.headers = { Authorization: `Bearer ${token}` };
    }
    return api.get(`review/${reviewId}/comments/`, config);
}

/**
 * POST /api/review/{review_id}/comments/
 */
export function createReviewComment(reviewId, payload) {
    return api.post(`review/${reviewId}/comments/`, payload);
}

/**
 * DELETE /api/review/{review_id}/comments/{comment_id}/
 */
export function deleteReviewComment(reviewId, commentId) {
    return api.delete(`review/${reviewId}/comments/${commentId}/`);
}

/**
 * GET /api/review/me/ (My Reviews)
 */
export function getMyReviews() {
    return api.get("review/me/");
}

/**
 * GET /api/review/user/{user_id}/
 */
export function getUserReviews(userId) {
    return api.get(`review/user/${userId}/`);
}

export function getTodayReviews() {
    return api.get("review/today/");
}

/**
 * PATCH /api/review/{review_id}/
 */
export function updateReview(reviewId, payload) {
    return api.patch(`review/${reviewId}/`, payload);
}

/**
 * DELETE /api/review/{review_id}/
 */
export function deleteReview(reviewId) {
    return api.delete(`review/${reviewId}/`);
}
