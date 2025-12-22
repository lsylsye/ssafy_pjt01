import { defineStore } from "pinia";
import {
  getFreeList,
  getFreeDetail,
  createFreePost,
  patchFreePost,
  deleteFreePost,
  toggleFreeLike,
  getFreeComments,
  writeFreeComment,
  deleteComment,
  toggleCommentLike,
} from "@/api/free";

export const useFreeStore = defineStore("communityFree", {
  state: () => ({
    loading: false,
    errorMsg: "",
    posts: [],

    detailLoading: false,
    detailError: "",
    post: null,

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
      this.posts = [];

      return getFreeList(country, params || {})
        .then((res) => {
          this.posts = Array.isArray(res.data) ? res.data : [];
        })
        .catch(() => {
          this.errorMsg = "게시글을 불러오지 못했습니다.";
        })
        .finally(() => {
          this.loading = false;
        });
    },

    fetchDetail(country, postId) {
      this.detailLoading = true;
      this.detailError = "";
      this.post = null;

      return getFreeDetail(country, postId)
        .then((res) => {
          this.post = res.data || null;
          this.likeCount = Number(res.data?.like_count || 0);
          this.liked = !!res.data?.liked; // ✅ 백엔드 liked 내려줘야 유지
        })
        .catch(() => {
          this.detailError = "게시글을 불러오지 못했습니다.";
        })
        .finally(() => {
          this.detailLoading = false;
        });
    },

    toggleLike(country, postId) {
      this.likeLoading = true;

      return toggleFreeLike(country, postId)
        .then((res) => {
          this.liked = !!res.data?.liked;
          this.likeCount = Number(res.data?.like_count ?? this.likeCount);
        })
        .finally(() => {
          this.likeLoading = false;
        });
    },

    fetchComments(country, postId) {
      this.cLoading = true;
      this.cError = "";
      this.comments = [];

      return getFreeComments(country, postId)
        .then((res) => {
          this.comments = Array.isArray(res.data?.comments) ? res.data.comments : [];
          if (this.post) this.post.comment_count = this.comments.length;
        })
        .catch(() => {
          this.cError = "댓글을 불러오지 못했습니다.";
        })
        .finally(() => {
          this.cLoading = false;
        });
    },

    createComment(country, postId, payload) {
      return writeFreeComment(country, postId, payload).then(() =>
        this.fetchComments(country, postId)
      );
    },

    removeComment(country, postId, commentId) {
      return deleteComment(commentId).then(() => this.fetchComments(country, postId));
    },

    likeComment(country, postId, commentId) {
      return toggleCommentLike(commentId).then(() => this.fetchComments(country, postId));
    },

    createPost(country, payload) {
      return createFreePost(country, payload).then((res) => res.data);
    },

    patchPost(country, postId, payload) {
      return patchFreePost(country, postId, payload).then(() =>
        this.fetchDetail(country, postId)
      );
    },

    removePost(country, postId) {
      return deleteFreePost(country, postId);
    },
  },
});
