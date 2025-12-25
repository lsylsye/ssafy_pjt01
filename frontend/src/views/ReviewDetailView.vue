<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  getReviewDetail, 
  toggleReviewLike, 
  getReviewComments, 
  createReviewComment, 
  deleteReviewComment,
  updateReview,
  deleteReview
} from '@/api/review';
import { toggleCommentLike } from '@/api/community';
import { useAuthStore } from "@/stores/auth.store";
import { useCommunityStore } from "@/stores/community.store";
import { useUiStore } from "@/stores/ui.store";
import { meApi } from '@/api/auth.store';
import { 
  Heart, 
  MessageCircle, 
  Reply, 
  Trash2, 
  SendHorizontal,
  MoreHorizontal
} from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const communityStore = useCommunityStore();
const uiStore = useUiStore();

const review = ref(null);
const comments = ref([]);
const commentContent = ref("");
const replyContent = ref("");
const loading = ref(true);
const userProfile = ref(null);
const replyTargetId = ref(null);
const showMenu = ref(false);
const isEditing = ref(false);
const editContent = ref("");

const fetchData = async () => {
    try {
        const id = route.params.id; 
        if(!id) return;
        
        const promises = [
            getReviewDetail(id),
            getReviewComments(id)
        ];
        
        if (authStore.access || localStorage.getItem("access_token")) {
            promises.push(meApi().catch(() => null));
        }

        const results = await Promise.all(promises);
        review.value = results[0].data;
        
        const commentData = results[1].data;
        if (commentData && Array.isArray(commentData.comments)) {
            comments.value = commentData.comments;
        } else if (Array.isArray(commentData)) {
            comments.value = commentData;
        }

        if (results[2] && results[2].data) {
            userProfile.value = results[2].data; 
        }

    } catch (e) {
        console.error(e);
        uiStore.alert('리뷰를 불러오지 못했습니다.');
        router.back();
    } finally {
        loading.value = false;
    }
};

const handleLike = async () => {
    if (!authStore.access && !localStorage.getItem("access_token")) {
        uiStore.alert('로그인이 필요합니다.');
        return;
    }
    await communityStore.handleReviewLike(review.value);
};

const handleCommentLike = async (comment) => {
    if (!authStore.access && !localStorage.getItem("access_token")) {
        uiStore.alert('로그인이 필요합니다.');
        return;
    }
    await communityStore.handleCommentLike(comment);
};

const toggleReply = (commentId) => {
    replyTargetId.value = (replyTargetId.value === commentId) ? null : commentId;
    replyContent.value = "";
};

const submitComment = async () => {
    if (!authStore.access && !localStorage.getItem("access_token")) {
        uiStore.alert('로그인이 필요합니다.');
        return;
    }
    
    const isReply = !!replyTargetId.value;
    const contentVal = isReply ? replyContent.value.trim() : commentContent.value.trim();
    if (!contentVal) return; 

    const payload = { content: contentVal };
    if (isReply) payload.parent_comment_id = replyTargetId.value;

    try {
        await createReviewComment(review.value.id, payload);
        
        if (isReply) {
            replyContent.value = "";
            replyTargetId.value = null;
        } else {
            commentContent.value = "";
        }
        
        const [cmtRes, revRes] = await Promise.all([
             getReviewComments(review.value.id),
             getReviewDetail(review.value.id)
        ]);
        
        if (cmtRes.data && Array.isArray(cmtRes.data.comments)) {
            comments.value = cmtRes.data.comments;
        } else if (Array.isArray(cmtRes.data)) {
            comments.value = cmtRes.data;
        }
        review.value = revRes.data; 
    } catch (e) {
        uiStore.alert('댓글 등록에 실패했습니다.');
    }
};

const deleteCommentAction = async (commentId) => {
    const ok = await uiStore.confirm('댓글을 삭제하시겠습니까?');
    if (!ok) return;

    try {
        await deleteReviewComment(review.value.id, commentId);
        const [cmtRes, revRes] = await Promise.all([
             getReviewComments(review.value.id),
             getReviewDetail(review.value.id)
        ]);
        if (cmtRes.data && Array.isArray(cmtRes.data.comments)) {
            comments.value = cmtRes.data.comments;
        } else if (Array.isArray(cmtRes.data)) {
            comments.value = cmtRes.data;
        }
        review.value = revRes.data;
    } catch (e) {
        uiStore.alert('삭제에 실패했습니다.');
    }
};

const handleDeleteReview = async () => {
    const ok = await uiStore.confirm('리뷰를 정말 삭제하시겠습니까?');
    if (!ok) return;
    try {
        await deleteReview(review.value.id);
        uiStore.addToast({ message: '리뷰가 삭제되었습니다.', variant: 'success' });
        router.back();
    } catch (e) {
        uiStore.alert('리뷰 삭제에 실패했습니다.');
    }
};

const startEdit = () => {
    isEditing.value = true;
    editContent.value = review.value.content;
    showMenu.value = false;
};

const handleUpdateReview = async () => {
    if (!editContent.value.trim()) return;
    try {
        await updateReview(review.value.id, { content: editContent.value });
        review.value.content = editContent.value;
        isEditing.value = false;
        uiStore.addToast({ message: '리뷰가 수정되었습니다.', variant: 'success' });
    } catch (e) {
        uiStore.alert('리뷰 수정에 실패했습니다.');
    }
};

const getAbsoluteUrl = (url) => {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return `http://127.0.0.1:8000${url.startsWith('/') ? '' : '/'}${url}`;
};

const fromNow = (iso) => {
    if (!iso) return '';
    const d = new Date(iso);
    const diff = Date.now() - d.getTime();
    const sec = Math.floor(diff / 1000);
    if (sec < 60) return "방금 전";
    const min = Math.floor(sec / 60);
    if (min < 60) return `${min}분 전`;
    const hr = Math.floor(min / 60);
    if (hr < 24) return `${hr}시간 전`;
    return `${Math.floor(hr / 24)}일 전`;
};

const goProfile = (id) => router.push(`/profile/${id}`);
const goBook = (isbn) => router.push(`/books/${isbn}`);

onMounted(fetchData);
</script>

<template>
  <div class="page" v-if="review">
    <div class="container">
      <!-- 1. 책 정보 임베드 -->
      <div class="book-embed" @click="goBook(review.isbn13)">
        <div class="embed-thumb">
          <img :src="review.cover" alt="" v-if="review.cover" />
        </div>
        <div class="embed-info">
          <h4 class="embed-title">{{ review.book_title }}</h4>
          <div class="embed-meta">
            {{ review.book_author }} · <span class="star">★ {{ review.rating }}</span>
          </div>
        </div>
      </div>

      <!-- 2. 리뷰 본문 -->
      <main class="review-card">
        <div class="user-header">
          <div class="u-info" @click="goProfile(review.user_id)">
            <div class="avatar" :style="{ backgroundImage: `url(${getAbsoluteUrl(review.user_profile_image)})` }"></div>
            <span class="nickname">{{ review.user_nickname }}</span>
          </div>
          
          <div class="menu-wrap" v-if="userProfile && review.user_id === userProfile.id">
            <button class="more-btn" @click="showMenu = !showMenu">
              <MoreHorizontal :size="20" />
            </button>
            <div v-if="showMenu" class="dropdown-menu glass-panel" @click.stop>
              <button class="menu-item" @click="startEdit">수정하기</button>
              <button class="menu-item delete" @click="handleDeleteReview">삭제하기</button>
            </div>
          </div>
        </div>
        
        <div class="review-body" v-if="!isEditing">
          {{ review.content }}
        </div>
        <div class="edit-mode" v-else>
          <textarea v-model="editContent" class="edit-textarea"></textarea>
          <div class="edit-actions">
            <button class="btn-cancel" @click="isEditing = false">취소</button>
            <button class="btn-save" @click="handleUpdateReview">저장</button>
          </div>
        </div>

        <div class="action-bar">
          <button 
            class="btn-action like" 
            :class="{ active: review.liked }"
            @click="handleLike"
          >
            <Heart :size="18" :fill="review.liked ? 'currentColor' : 'none'" />
            좋아요 {{ review.like_count }}
          </button>
          <div class="btn-action comment">
            <MessageCircle :size="18" />
            댓글 {{ review.comment_count }}
          </div>
        </div>
      </main>

      <!-- 3. 댓글 목록 -->
      <section class="comment-sec">
        <h3>댓글 {{ review.comment_count }}</h3>

        <div v-for="cmt in comments" :key="cmt.id" class="comment-group">
          <!-- 댓글 -->
          <div class="comment-item">
            <div 
              class="avatar sm" 
              @click="goProfile(cmt.user_id)"
              :style="{ backgroundImage: `url(${getAbsoluteUrl(cmt.user_profile_image || cmt.profile_image)})` }"
            ></div>
            <div class="c-bubble">
              <div class="c-top">
                <span class="c-name" @click="goProfile(cmt.user_id)">{{ cmt.user_nickname }}</span>
                <span class="c-time">{{ fromNow(cmt.created_at) }}</span>
              </div>
              <div class="c-text">{{ cmt.content }}</div>
              <div class="c-actions">
                <span 
                    class="act-link" 
                    :class="{ active: cmt.liked }" 
                    @click="handleCommentLike(cmt)"
                >
                    <Heart 
                        :size="14" 
                        :fill="cmt.liked ? '#ff4d6d' : 'none'" 
                        :stroke="cmt.liked ? '#ff4d6d' : 'currentColor'"
                        style="display: inline-block; vertical-align: middle; margin-right: 2px;"
                    />
                    좋아요 {{ cmt.like_count }}
                </span>
                <span class="act-link" @click="toggleReply(cmt.id)">답글 달기</span>
                <span 
                    v-if="userProfile && cmt.user_id === userProfile.id" 
                    class="act-link del" 
                    @click="deleteCommentAction(cmt.id)"
                >삭제</span>
              </div>
            </div>
          </div>

          <!-- 답글 입력창 -->
          <div v-if="replyTargetId === cmt.id" class="reply-input-box">
             <input 
                type="text" 
                v-model="replyContent" 
                placeholder="답글을 남겨주세요..."
                @keydown.enter="submitComment"
             />
             <button @click="submitComment"><SendHorizontal :size="18" /></button>
          </div>

          <!-- 대댓글 -->
          <div v-for="reply in cmt.replies" :key="reply.id" class="reply-item">
            <div 
              class="avatar sm" 
              @click="goProfile(reply.user_id)"
              :style="{ backgroundImage: `url(${getAbsoluteUrl(reply.user_profile_image || reply.profile_image)})` }"
            ></div>
            <div class="c-bubble reply-bubble">
              <div class="c-top">
                <span class="c-name" @click="goProfile(reply.user_id)">
                    {{ reply.user_nickname }}
                    <span v-if="reply.user_id === review.user_id" class="author-tag">작성자</span>
                </span>
                <span class="c-time">{{ fromNow(reply.created_at) }}</span>
              </div>
              <div class="c-text">{{ reply.content }}</div>
              <div class="c-actions">
                <span 
                    class="act-link" 
                    :class="{ active: reply.liked }" 
                    @click="handleCommentLike(reply)"
                >
                    <Heart 
                        :size="14" 
                        :fill="reply.liked ? '#ff4d6d' : 'none'" 
                        :stroke="reply.liked ? '#ff4d6d' : 'currentColor'"
                        style="display: inline-block; vertical-align: middle; margin-right: 2px;"
                    />
                    좋아요 {{ reply.like_count }}
                </span>
                <span 
                    v-if="userProfile && reply.user_id === userProfile.id" 
                    class="act-link del" 
                    @click="deleteCommentAction(reply.id)"
                >삭제</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 하단 고정 입력창 -->
    <div class="input-area">
      <div class="input-box">
        <input
          type="text"
          class="c-input"
          v-model="commentContent"
          placeholder="따뜻한 댓글을 남겨주세요..."
          @keydown.enter="submitComment"
        />
        <button class="btn-send" @click="submitComment"><SendHorizontal :size="20" /></button>
      </div>
    </div>
  </div>
  <div v-else class="loading">불러오는 중...</div>
</template>

<style scoped>
.page {
  background: #f2f4f6;
  min-height: 100vh;
  padding-bottom: 100px;
  color: #191f28;
}
.container {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
}

/* 책 정보 임베드 */
.book-embed {
  display: flex;
  gap: 15px;
  background: white;
  padding: 16px;
  border-radius: 20px;
  margin-bottom: 20px;
  cursor: pointer;
  border: 1px solid white;
  transition: 0.2s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}
.book-embed:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.06);
}
.embed-thumb {
  width: 60px;
  height: 88px;
  background: #eee;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
}
.embed-thumb img { width: 100%; height: 100%; object-fit: cover; }
.embed-info { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.embed-title { margin: 0 0 4px 0; font-size: 1.05rem; font-weight: 700; }
.embed-meta { font-size: 0.9rem; color: #6b7684; }
.star { color: #ffbb00; font-weight: 700; }

/* 리뷰 카드 */
.review-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  margin-bottom: 32px;
}
.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.u-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}
.avatar {
  width: 44px;
  height: 44px;
  background: #eee;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
}
.avatar.sm { width: 32px; height: 32px; }
.nickname { font-weight: 700; font-size: 1.05rem; }
.more-btn { background: none; border: none; color: #adb5bd; cursor: pointer; padding: 4px; }
.more-btn:hover { color: #191f28; }

.menu-wrap { position: relative; }
.dropdown-menu {
  position: absolute; top: 100%; right: 0; min-width: 120px;
  background: white; border-radius: 12px; padding: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1); z-index: 50;
  display: flex; flex-direction: column; gap: 4px;
}
.menu-item {
  background: none; border: none; width: 100%; padding: 10px;
  font-size: 0.9rem; font-weight: 700; text-align: left;
  border-radius: 8px; cursor: pointer; color: #4e5968;
}
.menu-item:hover { background: #f2f4f6; color: #191f28; }
.menu-item.delete { color: #ff6b6b; }
.menu-item.delete:hover { background: #fff0f0; }

.edit-mode { display: flex; flex-direction: column; gap: 12px; margin-bottom: 30px; }
.edit-textarea {
  width: 100%; height: 120px; padding: 16px; border-radius: 16px;
  border: 1px solid #e5e8eb; font-family: inherit; font-size: 1rem;
  resize: none; background: #f9fafb;
}
.edit-textarea:focus { outline: none; border-color: #00d15b; background: white; }
.edit-actions { display: flex; justify-content: flex-end; gap: 8px; }
.btn-cancel { background: #f2f4f6; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; cursor: pointer; }
.btn-save { background: #00d15b; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; cursor: pointer; }

.review-body {
  font-size: 1.1rem;
  line-height: 1.7;
  min-height: 120px;
  color: #333;
  margin-bottom: 30px;
  white-space: pre-wrap;
}

.action-bar {
  display: flex;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #f2f4f6;
}
.btn-action {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 30px;
  font-size: 0.9rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: 0.2s;
}
.btn-action.like { background: #fff0f3; color: #ff4d6d; }
.btn-action.like.active { background: #ff4d6d; color: white; }
.btn-action.comment { background: #f2f4f6; color: #4e5968; cursor: default; }

/* 댓글 섹션 */
.comment-sec h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 24px; padding-left: 4px; }
.comment-group { margin-bottom: 20px; }
.comment-item { display: flex; gap: 12px; margin-bottom: 12px; }
.c-bubble { background: white; padding: 16px; border-radius: 0 16px 16px 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); flex: 1; }
.c-top { display: flex; gap: 8px; align-items: center; margin-bottom: 4px; }
.c-name { font-weight: 700; font-size: 0.95rem; cursor: pointer; }
.c-time { font-size: 0.8rem; color: #adb5bd; }
.author-tag { font-size: 0.7rem; background: #00d15b; color: white; padding: 2px 6px; border-radius: 4px; margin-left: 4px; }
.c-text { font-size: 0.95rem; line-height: 1.5; color: #4e5968; }
.c-actions { display: flex; gap: 14px; margin-top: 10px; }
.act-link { font-size: 0.8rem; color: #8b95a1; cursor: pointer; font-weight: 600; }
.act-link:hover, .act-link.active { color: #ff4d6d; }
.act-link.del:hover { color: #ff6b6b; }

.reply-item { margin-left: 44px; display: flex; gap: 12px; margin-top: 12px; }
.reply-bubble { background: #f8f9fa; border: 1px solid #eee; }

.reply-input-box {
  margin-left: 44px;
  margin-bottom: 16px;
  display: flex;
  gap: 8px;
  background: white;
  padding: 8px 8px 8px 16px;
  border-radius: 20px;
  border: 1px solid #e5e8eb;
}
.reply-input-box input { flex: 1; border: none; outline: none; font-size: 0.9rem; }
.reply-input-box button { background: none; border: none; color: #00d15b; cursor: pointer; display: flex; align-items: center; }

/* 하단 입력창 */
.input-area {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  padding: 16px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
  z-index: 100;
}
.input-box { width: 100%; max-width: 700px; display: flex; gap: 12px; }
.c-input {
  flex: 1;
  padding: 12px 20px;
  border-radius: 24px;
  border: 1px solid #eee;
  background: #f2f4f6;
  font-size: 1rem;
  outline: none;
}
.c-input:focus { background: white; border-color: #00d15b; }
.btn-send {
  background: #00d15b;
  color: white;
  border: none;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.2s;
}
.btn-send:hover { background: #00b54f; transform: scale(1.05); }

.loading { padding: 100px; text-align: center; color: #8b95a1; }
</style>
