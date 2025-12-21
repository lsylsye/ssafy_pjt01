<template>
  <section>
    <p v-if="loading">불러오는 중...</p>
    <p v-else-if="errorMsg" class="error">{{ errorMsg }}</p>

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

      <!-- 본문 / 수정모드 -->
      <div v-if="!isEditing">
        <div class="submeta">
          <span>{{ review.book_author }}</span>
          <span>· {{ review.publisher || '-' }}</span>
          <span>· 평점 {{ review.rating ?? '-' }}</span>
        </div>

        <p class="content">{{ review.content }}</p>
      </div>

      <div v-else class="editbox">
        <!-- ✅ 보이되 수정 불가 -->
        <input v-model="editBookTitle" class="input" placeholder="책 제목" disabled />
        <input v-model="editBookAuthor" class="input" placeholder="저자" disabled />

        <input
          v-model.number="editRating"
          class="input"
          type="number"
          min="1"
          max="5"
          placeholder="평점(선택) 1~5"
        />
        <textarea v-model="editContent" class="textarea" placeholder="리뷰 내용"></textarea>

        <div class="actions">
          <button class="btn" :disabled="saving" @click="saveEdit">저장</button>
          <button class="btn" :disabled="saving" @click="cancelEdit">취소</button>
        </div>

        <p v-if="editError" class="error">{{ editError }}</p>
      </div>

      <!-- 버튼 영역 -->
      <div class="actions" v-if="!isEditing">
        <button class="btn" @click="toggleLike" :disabled="likeLoading">
          {{ liked ? '좋아요 취소' : '좋아요' }}
        </button>

        <template v-if="auth.isLoggedIn">
          <button class="btn" @click="startEdit">수정</button>
          <button class="btn danger" @click="removeReview">삭제</button>
        </template>
      </div>

      <!-- ✅ 수정모드에서는 댓글 영역 숨김 -->
      <template v-if="!isEditing">
        <hr class="line" />

        <h3>댓글</h3>

        <div v-if="!auth.isLoggedIn" class="need-login">
          댓글 작성/좋아요/삭제는 로그인 후 이용할 수 있습니다.
        </div>

        <div class="comment-write" v-if="auth.isLoggedIn">
          <input v-model="newComment" class="input" placeholder="댓글을 입력하세요" />
          <button class="btn" :disabled="commentSaving" @click="writeComment()">등록</button>
        </div>

        <p v-if="cLoading">댓글 불러오는 중...</p>
        <p v-else-if="cError" class="error">{{ cError }}</p>

        <div v-else>
          <p v-if="comments.length === 0">댓글이 없습니다.</p>

          <ul v-else class="clist">
            <li v-for="c in comments" :key="c.id" class="citem">
              <div class="cmeta">
                <span class="nick">{{ c.user_nickname }}</span>
                <span class="date">{{ formatDate(c.created_at) }}</span>
                <span class="count">좋아요 {{ c.like_count }}</span>
              </div>

              <p class="ctext">{{ c.content }}</p>

              <div class="cactions">
                <button class="linkbtn" v-if="auth.isLoggedIn" @click="likeComment(c)">
                  {{ c.liked ? '좋아요 취소' : '좋아요' }}
                </button>
                <button class="linkbtn" v-if="auth.isLoggedIn" @click="removeComment(c.id)">
                  삭제
                </button>
                <button class="linkbtn" v-if="auth.isLoggedIn" @click="startReply(c.id)">
                  답글
                </button>
              </div>

              <div v-if="replyingTo === c.id" class="replybox">
                <input v-model="replyText" class="input" placeholder="답글 입력" />
                <button class="btn" :disabled="replySaving" @click="writeComment(c.id)">
                  등록
                </button>
                <button class="btn" :disabled="replySaving" @click="cancelReply">
                  취소
                </button>
              </div>

              <ul v-if="c.replies && c.replies.length" class="rlist">
                <li v-for="r in c.replies" :key="r.id" class="ritem">
                  <div class="cmeta">
                    <span class="nick">{{ r.user_nickname }}</span>
                    <span class="date">{{ formatDate(r.created_at) }}</span>
                    <span class="count">좋아요 {{ r.like_count }}</span>
                  </div>

                  <p class="ctext">{{ r.content }}</p>

                  <div class="cactions">
                    <button class="linkbtn" v-if="auth.isLoggedIn" @click="likeComment(r)">
                      {{ r.liked ? '좋아요 취소' : '좋아요' }}
                    </button>
                    <button class="linkbtn" v-if="auth.isLoggedIn" @click="removeComment(r.id)">
                      삭제
                    </button>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </template>
    </div>

    <p v-else>리뷰가 없습니다.</p>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import {
  getReviewDetail,
  patchReview,
  deleteReview,
  toggleReviewLike,
  getReviewComments,
  createReviewComment,
  deleteComment,
  toggleCommentLike,
} from "@/api/review";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const country = computed(() => String(route.params.country || "kr"));
const reviewId = computed(() => String(route.params.reviewId || ""));

const formatDate = (iso) => (typeof iso === "string" ? iso.slice(0, 10) : "");

const requireTokenOrGoLogin = () => {
  const token =
    localStorage.getItem("access_token") ||
    localStorage.getItem("access") ||
    localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return null;
  }
  return token;
};

const loading = ref(false);
const errorMsg = ref("");
const review = ref(null);

const liked = ref(false);
const likeCount = ref(0);
const likeLoading = ref(false);

const cLoading = ref(false);
const cError = ref("");
const comments = ref([]);

const newComment = ref("");
const commentSaving = ref(false);

const replyingTo = ref(null);
const replyText = ref("");
const replySaving = ref(false);

/* 리뷰 상세 */
const fetchDetail = () => {
  loading.value = true;
  errorMsg.value = "";
  review.value = null;

  getReviewDetail(country.value, reviewId.value)
    .then((res) => {
      review.value = res.data;
      likeCount.value = Number(res.data?.like_count || 0);
      liked.value = !!res.data?.liked;
    })
    .catch((err) => {
      console.error("[리뷰 상세 실패]", err.response?.status, err.response?.data || err.message);
      errorMsg.value = "리뷰를 불러오지 못했습니다.";
    })
    .finally(() => {
      loading.value = false;
    });
};

/* 리뷰 좋아요 */
const toggleLike = () => {
  const token = requireTokenOrGoLogin();
  if (!token) return;

  likeLoading.value = true;
  toggleReviewLike(country.value, reviewId.value)
    .then((res) => {
      liked.value = !!res.data?.liked;
      likeCount.value = Number(res.data?.like_count || likeCount.value);
    })
    .catch((err) => {
      const status = err.response?.status;
      if (status === 401) {
        auth.logout?.();
        router.push("/login");
        return;
      }
      alert("좋아요 처리에 실패했습니다.");
    })
    .finally(() => {
      likeLoading.value = false;
    });
};

/* 리뷰 수정/삭제 */
const isEditing = ref(false);
const saving = ref(false);
const editError = ref("");

const editBookTitle = ref("");
const editBookAuthor = ref("");
const editRating = ref(null);
const editContent = ref("");

const startEdit = () => {
  if (!review.value) return;
  isEditing.value = true;
  editError.value = "";

  editBookTitle.value = review.value.book_title || "";
  editBookAuthor.value = review.value.book_author || "";
  editRating.value = review.value.rating ?? null;
  editContent.value = review.value.content || "";
};

const cancelEdit = () => {
  isEditing.value = false;
  editError.value = "";
};

const saveEdit = () => {
  const token = requireTokenOrGoLogin();
  if (!token) return;
  if (!review.value) return;

  const ct = editContent.value.trim();
  if (!ct) {
    editError.value = "내용은 필수입니다.";
    return;
  }

  // book_title / book_author는 절대 보내지 않음
  const body = {};

  const r = editRating.value;
  const rNum = r === null || r === "" ? null : Number(r);
  if (rNum !== (review.value.rating ?? null)) body.rating = rNum;

  if (ct !== (review.value.content || "")) body.content = ct;

  if (Object.keys(body).length === 0) {
    isEditing.value = false;
    return;
  }

  saving.value = true;
  editError.value = "";

  patchReview(country.value, reviewId.value, body)
    .then(() => {
      isEditing.value = false;
      fetchDetail();
    })
    .catch((err) => {
      const status = err.response?.status;
      if (status === 401) {
        auth.logout?.();
        router.push("/login");
        return;
      }
      if (status === 403) {
        editError.value = "작성자만 수정할 수 있습니다.";
        return;
      }
      editError.value = "리뷰 수정에 실패했습니다.";
    })
    .finally(() => {
      saving.value = false;
    });
};

const removeReview = () => {
  const token = requireTokenOrGoLogin();
  if (!token) return;

  const ok = confirm("정말 삭제할까요?");
  if (!ok) return;

  deleteReview(country.value, reviewId.value)
    .then(() => {
      router.push(`/community/${country.value}/review`);
    })
    .catch((err) => {
      const status = err.response?.status;
      if (status === 401) {
        auth.logout?.();
        router.push("/login");
        return;
      }
      if (status === 403) {
        alert("작성자만 삭제할 수 있습니다.");
        return;
      }
      alert("리뷰 삭제에 실패했습니다.");
    });
};

/* 댓글 */
const normalizeComment = (obj) => ({
  ...obj,
  liked: !!obj.liked,
  replies: (obj.replies || []).map((r) => ({ ...r, liked: !!r.liked })),
});

const fetchComments = () => {
  cLoading.value = true;
  cError.value = "";
  comments.value = [];

  getReviewComments(country.value, reviewId.value)
    .then((res) => {
      const list = Array.isArray(res.data?.comments) ? res.data.comments : [];
      comments.value = list.map(normalizeComment);
      if (review.value) review.value.comment_count = list.length;
    })
    .catch(() => {
      cError.value = "댓글을 불러오지 못했습니다.";
    })
    .finally(() => {
      cLoading.value = false;
    });
};

const writeComment = (parentId) => {
  const token = requireTokenOrGoLogin();
  if (!token) return;

  const text = parentId ? replyText.value.trim() : newComment.value.trim();
  if (!text) return;

  commentSaving.value = !parentId;
  replySaving.value = !!parentId;

  const payload = parentId ? { content: text, parent_comment_id: parentId } : { content: text };

  createReviewComment(country.value, reviewId.value, payload)
    .then(() => {
      newComment.value = "";
      replyingTo.value = null;
      replyText.value = "";
      fetchComments();
    })
    .catch((err) => {
      const status = err.response?.status;
      if (status === 401) {
        auth.logout?.();
        router.push("/login");
        return;
      }
      alert("댓글 작성에 실패했습니다.");
    })
    .finally(() => {
      commentSaving.value = false;
      replySaving.value = false;
    });
};

const removeComment = (commentId) => {
  const token = requireTokenOrGoLogin();
  if (!token) return;

  const ok = confirm("댓글을 삭제할까요?");
  if (!ok) return;

  deleteComment(commentId)
    .then(() => {
      fetchComments();
    })
    .catch((err) => {
      const status = err.response?.status;
      if (status === 401) {
        auth.logout?.();
        router.push("/login");
        return;
      }
      alert("댓글 삭제에 실패했습니다.");
    });
};

const likeComment = (item) => {
  const token = requireTokenOrGoLogin();
  if (!token) return;

  toggleCommentLike(item.id)
    .then((res) => {
      if (typeof res.data?.liked !== "undefined") item.liked = !!res.data.liked;
      if (typeof res.data?.like_count !== "undefined") item.like_count = Number(res.data.like_count || 0);
      if (typeof res.data?.liked === "undefined") fetchComments();
    })
    .catch((err) => {
      const status = err.response?.status;
      if (status === 401) {
        auth.logout?.();
        router.push("/login");
        return;
      }
      alert("댓글 좋아요에 실패했습니다.");
    });
};

const startReply = (commentId) => {
  replyingTo.value = commentId;
  replyText.value = "";
};

const cancelReply = () => {
  replyingTo.value = null;
  replyText.value = "";
};

onMounted(() => {
  fetchDetail();
  fetchComments();
});

watch(
  () => `${country.value}-${reviewId.value}-${auth.isLoggedIn}`,
  () => {
    fetchDetail();
    fetchComments();
  }
);
</script>

<style scoped>
.error { color: #d33; }
.card { border: 1px solid #eee; border-radius: 12px; padding: 14px; }
.head { margin-bottom: 12px; }
.hrow { display: flex; gap: 8px; align-items: center; }
.title { margin: 0; }

.meta { margin-top: 6px; color: #666; font-size: 14px; display: flex; gap: 8px; flex-wrap: wrap; }
.submeta { margin-top: 10px; color: #666; font-size: 14px; display: flex; gap: 8px; flex-wrap: wrap; }

.content { margin: 12px 0 0; line-height: 1.6; white-space: pre-wrap; }

.actions { margin-top: 12px; }
.btn { border: 1px solid #ddd; background: white; border-radius: 10px; padding: 8px 12px; cursor: pointer; margin-right: 8px; }
.btn:hover { border-color: #1a73e8; color: #1a73e8; }
.btn.danger { border-color: #f2b8b5; }
.btn.danger:hover { border-color: #d33; color: #d33; }

.line { border: none; border-top: 1px solid #eee; margin: 16px 0; }
.need-login { color: #666; background: #fafafa; border: 1px solid #eee; padding: 10px; border-radius: 10px; margin-top: 8px; }

.comment-write { display: flex; gap: 8px; margin: 10px 0 14px; }
.input { flex: 1; border: 1px solid #ddd; border-radius: 10px; padding: 8px 10px; }
.input:disabled { background: #f5f5f5; color: #777; cursor: not-allowed; }

.textarea{ border: 1px solid #ddd; border-radius: 10px; padding: 10px 12px; min-height: 160px; resize: vertical; margin-top: 8px; }

.clist { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.citem { border: 1px solid #eee; border-radius: 12px; padding: 10px 12px; }

.cmeta { color: #666; font-size: 13px; display: flex; gap: 10px; flex-wrap: wrap; }
.nick { font-weight: 700; color: #333; }
.ctext { margin: 6px 0 0; white-space: pre-wrap; }

.cactions { margin-top: 8px; display: flex; gap: 10px; }
.linkbtn { border: none; background: none; color: #1a73e8; cursor: pointer; padding: 0; }

.replybox { display: flex; gap: 8px; margin-top: 8px; }
.rlist { list-style: none; padding: 0; margin: 10px 0 0 18px; display: flex; flex-direction: column; gap: 10px; }
.ritem { border: 1px dashed #e6e6e6; border-radius: 12px; padding: 10px 12px; background: #fcfcfc; }

.editbox { margin-top: 12px; }
</style>
