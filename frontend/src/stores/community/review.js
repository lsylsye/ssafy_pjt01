import { defineStore } from "pinia";
import {
  getReviewList,
  getReviewDetail,
  createReview,
  patchReview,
  deleteReview,
  toggleReviewLike,
  getReviewComments,
  createReviewComment,
  deleteComment,
  toggleCommentLike,
} from "@/api/review";

export const useReviewStore = defineStore("communityReview", {
  state: () => ({
    loading: false,
    errorMsg: "",
    reviews: [],

    detailLoading: false,
    detailError: "",
    review: null,

    liked: false,
    likeCount: 0,
    likeLoading: false,

    cLoading: false,
    cError: "",
    comments: [],
  }),

  actions: {
    fetchList(country, params) {
      this.loading = true;
      this.errorMsg = "";
      this.reviews = [];

      return getReviewList(country, params || {})
        .then((res) => {
          this.reviews = Array.isArray(res.data) ? res.data : [];
        })
        .catch(() => {
          this.errorMsg = "리뷰를 불러오지 못했습니다.";
        })
        .finally(() => {
          this.loading = false;
        });
    },

    fetchDetail(country, reviewId) {
      this.detailLoading = true;
      this.detailError = "";
      this.review = null;

      return getReviewDetail(country, reviewId)
        .then((res) => {
          this.review = res.data || null;
          this.likeCount = Number(res.data?.like_count || 0);
          this.liked = !!res.data?.liked;
        })
        .catch(() => {
          this.detailError = "리뷰를 불러오지 못했습니다.";
        })
        .finally(() => {
          this.detailLoading = false;
        });
    },

    toggleLike(country, reviewId) {
      this.likeLoading = true;

      return toggleReviewLike(country, reviewId)
        .then((res) => {
          this.liked = !!res.data?.liked;
          this.likeCount = Number(res.data?.like_count ?? this.likeCount);
        })
        .finally(() => {
          this.likeLoading = false;
        });
    },

    fetchComments(country, reviewId) {
      this.cLoading = true;
      this.cError = "";
      this.comments = [];

      return getReviewComments(country, reviewId)
        .then((res) => {
          this.comments = Array.isArray(res.data?.comments) ? res.data.comments : [];
          if (this.review) this.review.comment_count = this.comments.length;
        })
        .catch(() => {
          this.cError = "댓글을 불러오지 못했습니다.";
        })
        .finally(() => {
          this.cLoading = false;
        });
    },

    createComment(country, reviewId, payload) {
      return createReviewComment(country, reviewId, payload).then(() =>
        this.fetchComments(country, reviewId)
      );
    },

    removeComment(country, reviewId, commentId) {
      return deleteComment(commentId).then(() => this.fetchComments(country, reviewId));
    },

    likeComment(country, reviewId, commentId) {
      return toggleCommentLike(commentId).then(() => this.fetchComments(country, reviewId));
    },

    createReview(country, payload) {
      return createReview(country, payload).then((res) => res.data);
    },

    patchReview(country, reviewId, payload) {
      return patchReview(country, reviewId, payload).then(() =>
        this.fetchDetail(country, reviewId)
      );
    },

    removeReview(country, reviewId) {
      return deleteReview(country, reviewId);
    },
  },
});
