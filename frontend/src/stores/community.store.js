import { defineStore } from "pinia";
import { toggleLike, toggleCommentLike } from "@/api/community";
import { toggleReviewLike } from "@/api/review";

export const useCommunityStore = defineStore("community", {
    state: () => ({
        loading: false,
        error: "",
    }),

    actions: {
        async handlePostLike(post) {
            if (!post) return;
            try {
                await toggleLike(post.id);

                // Optimistic update or simple state toggle
                if (post.liked) {
                    post.like_count--;
                } else {
                    post.like_count++;
                }
                post.liked = !post.liked;

                return true;
            } catch (e) {
                console.error("[CommunityStore] Like failed:", e);
                return false;
            }
        },

        async handleCommentLike(comment) {
            if (!comment) return;
            try {
                await toggleCommentLike(comment.id);

                // Optimistic update or simple state toggle
                if (comment.liked) {
                    comment.like_count--;
                } else {
                    comment.like_count++;
                }
                comment.liked = !comment.liked;

                return true;
            } catch (e) {
                console.error("[CommunityStore] Comment Like failed:", e);
                return false;
            }
        },

        async handleReviewLike(review) {
            if (!review) return;
            try {
                await toggleReviewLike(review.id);

                // Optimistic update or simple state toggle
                if (review.liked) {
                    review.like_count--;
                } else {
                    review.like_count++;
                }
                review.liked = !review.liked;

                return true;
            } catch (e) {
                console.error("[CommunityStore] Review Like failed:", e);
                return false;
            }
        }
    },
});
