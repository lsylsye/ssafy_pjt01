<template>
  <section>
    <p v-if="detailLoading">불러오는 중...</p>
    <p v-else-if="detailError" class="error">{{ detailError }}</p>

    <div v-else-if="review" class="card">
      <div class="head">
        <div class="hrow">
          <h2 class="title">{{ review.book_title }}</h2>
        </div>

        <div class="meta">
          <span>{{ review.user_nickname }}</span>
          <span>· {{ formatDate(review.created_at) }}</span>
          <span>· 좋아요 {{ likeCount }}</span>
          <span>· 댓글 {{ review.comment_count }}</span>
        </div>
      </div>

      <div class="submeta">
        <span>{{ review.book_author }}</span>
        <span>· {{ review.publisher || "-" }}</span>
        <span>· 평점 {{ review.rating ?? "-" }}</span>
      </div>

      <p class="content">{{ review.content }}</p>

      <div class="actions">
        <LikeButton
          :liked="liked"
          :count="likeCount"
          :disabled="likeLoading || !auth.isLoggedIn"
          @toggle="toggleLike"
        />

        <template v-if="auth.isLoggedIn">
          <button class="btn" @click="goEdit">수정</button>
          <button class="btn danger" @click="removeReview">삭제</button>
        </template>
      </div>

      <hr class="line" />

      <h3>댓글</h3>

      <div v-if="!auth.isLoggedIn" class="need-login">
        댓글 작성/좋아요/삭제는 로그인 후 이용할 수 있습니다.
      </div>

      <div v-else>
        <CommentForm @submit="writeComment" />
      </div>

      <CommentList
        :items="comments"
        :loading="cLoading"
        :error="cError"
        :actions-enabled="auth.isLoggedIn"
        @reply="writeReply"
        @like="likeComment"
        @remove="removeComment"
      />
    </div>

    <p v-else>리뷰가 없습니다.</p>
  </section>
</template>

<script setup>
import { onMounted, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";

import useCountry from "@/composables/useCountry";
import { useAuthStore } from "@/stores/auth";
import { useReviewStore } from "@/stores/community/review";

import LikeButton from "@/components/community/LikeButton.vue";
import CommentForm from "@/components/community/CommentForm.vue";
import CommentList from "@/components/community/CommentList.vue";

const route = useRoute();
const router = useRouter();
const { country } = useCountry();

const auth = useAuthStore();
const store = useReviewStore();

const {
  detailLoading,
  detailError,
  review,
  liked,
  likeCount,
  likeLoading,
  cLoading,
  cError,
  comments,
} = storeToRefs(store);

const reviewId = computed(() => String(route.params.reviewId || ""));

const formatDate = (iso) => (typeof iso === "string" ? iso.slice(0, 10) : "");

const fetchAll = () => {
  store
    .fetchDetail(country.value, reviewId.value)
    .then(() => {
      if (auth.isLoggedIn) return store.fetchComments(country.value, reviewId.value);
    })
    .catch(() => {});
};

onMounted(fetchAll);

watch(
  () => `${country.value}-${reviewId.value}-${auth.isLoggedIn}`,
  () => fetchAll()
);

const toggleLike = () => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }

  store.toggleLike(country.value, reviewId.value).catch(() => {
    alert("좋아요 처리에 실패했습니다.");
  });
};

const goEdit = () => {
  router.push(`/community/${country.value}/review/${reviewId.value}/edit`);
};

const removeReview = () => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }
  if (!confirm("정말 삭제할까요?")) return;

  store
    .removeReview(country.value, reviewId.value)
    .then(() => {
      router.push(`/community/${country.value}/review`);
    })
    .catch(() => {
      alert("리뷰 삭제에 실패했습니다.");
    });
};

const writeComment = (content) => {
  store
    .createComment(country.value, reviewId.value, { content })
    .catch(() => alert("댓글 작성에 실패했습니다."));
};

const writeReply = ({ parentId, content }) => {
  store
    .createComment(country.value, reviewId.value, { content, parent_comment_id: parentId })
    .catch(() => alert("답글 작성에 실패했습니다."));
};

const removeComment = (commentId) => {
  if (!confirm("댓글을 삭제할까요?")) return;

  store
    .removeComment(country.value, reviewId.value, commentId)
    .catch(() => alert("댓글 삭제에 실패했습니다."));
};

const likeComment = (commentId) => {
  store
    .likeComment(country.value, reviewId.value, commentId)
    .catch(() => alert("댓글 좋아요에 실패했습니다."));
};
</script>

<style scoped>
section {
  padding: 24px;
  min-height: auto;
  max-width: 900px;
  margin: 0 auto;
  background: #ffffff;
}

.error {
  color: #dc2626;
  background: #fee2e2;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 12px 0;
}

.card {
  border: none;
  border-radius: 8px;
  padding: 24px;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.head {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.hrow {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.title {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.meta {
  margin-top: 12px;
  color: #999;
  font-size: 12px;
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.submeta {
  margin-top: 12px;
  color: #666;
  font-size: 12px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding: 10px 12px;
  background: #f9f9f9;
  border-radius: 8px;
}

.content {
  margin: 20px 0 0;
  line-height: 1.8;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 14px;
  color: var(--text-primary);
}

.actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.btn {
  border: 1px solid #ddd;
  background: #ffffff;
  border-radius: 6px;
  padding: 10px 14px;
  cursor: pointer;
  color: var(--text-primary);
  font-weight: 500;
  transition: var(--transition);
  font-size: 13px;
}

.btn:hover {
  border-color: var(--primary-color);
  background: #f5f5f5;
  color: var(--primary-color);
}

.btn.danger {
  border-color: #fecaca;
}

.btn.danger:hover {
  border-color: #dc2626;
  color: #dc2626;
  background: #fee2e2;
}

.line {
  border: none;
  border-top: 1px solid #f0f0f0;
  margin: 24px 0;
}

.need-login {
  color: #666;
  background: #f9f9f9;
  border: 1px solid #f0f0f0;
  padding: 12px 14px;
  border-radius: 8px;
  margin: 16px 0;
  font-size: 13px;
}

h3 {
  margin: 20px 0 16px;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}
</style>
