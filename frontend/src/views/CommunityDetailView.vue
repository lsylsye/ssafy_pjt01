<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getPostDetail, getComments, createComment, deleteComment } from '@/api/community';
import { useAuthStore } from "@/stores/auth.store";
import { useCommunityStore } from "@/stores/community.store";
import { useUiStore } from "@/stores/ui.store";
import { meApi } from '@/api/auth.store';
import { Heart, MessageCircle, Reply, Trash2, SendHorizontal } from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const communityStore = useCommunityStore();
const uiStore = useUiStore();

const post = ref(null);
const comments = ref([]);
const commentContent = ref("");
const replyContent = ref("");
const loading = ref(true);
const userProfile = ref(null);
const replyTargetId = ref(null);

const fetchData = async () => {
    try {
        const id = route.params.id; 
        if(!id) return;
        
        // 병렬 요청: 게시글, 댓글
        const promises = [
            getPostDetail(id),
            getComments(id)
        ];
        
        // 토큰이 있을 때만 meApi 호출 추가
        if (authStore.access || localStorage.getItem("access_token")) {
            promises.push(meApi().catch(err => {
                console.warn("Failed to fetch me:", err);
                return null;
            }));
        }

        const results = await Promise.all(promises);
        const postRes = results[0];
        const commentRes = results[1];
        const meRes = results[2] || null;

        post.value = postRes.data;
        
        if (commentRes.data && Array.isArray(commentRes.data.comments)) {
            comments.value = commentRes.data.comments;
        } else if (Array.isArray(commentRes.data)) {
            comments.value = commentRes.data;
        } else {
             comments.value = [];
        }

        if (meRes && meRes.data) {
            userProfile.value = meRes.data; 
        }

    } catch (e) {
        console.error(e);
        if (e.response?.status === 401) {
            // 토큰 만료 혹은 비정상 토큰인 경우
            localStorage.removeItem("access_token");
            authStore.access = null;
            authStore.user = null;
            uiStore.alert('세션이 만료되었습니다. 다시 로그인해주세요.');
            router.push('/login'); // 혹은 적절한 로그인 페이지로
        } else {
            uiStore.alert('게시글을 불러오지 못했습니다.');
            router.back();
        }
    } finally {
        loading.value = false;
    }
};

const toggleReply = (commentId) => {
    if (replyTargetId.value === commentId) {
        replyTargetId.value = null; // 토글 오프
    } else {
        replyTargetId.value = commentId;
    }
};

const handleCommentLike = async (comment) => {
    if (!authStore.access && !localStorage.getItem("access_token")) {
        uiStore.alert('로그인이 필요합니다.');
        return;
    }
    await communityStore.handleCommentLike(comment);
};

const handleDeleteComment = async (commentId) => {
    const isConfirmed = await uiStore.confirm('정말 이 댓글을 삭제하시겠습니까?', '댓글 삭제');
    if (!isConfirmed) return;

    try {
        await deleteComment(post.value.id, commentId);
        
        // 데이터 갱신
        const [cmtRes, postRes] = await Promise.all([
             getComments(post.value.id),
             getPostDetail(post.value.id)
        ]);
        
        if (cmtRes.data && Array.isArray(cmtRes.data.comments)) {
            comments.value = cmtRes.data.comments;
        } else if (Array.isArray(cmtRes.data)) {
            comments.value = cmtRes.data;
        }
        post.value = postRes.data;
        uiStore.addToast({ message: '댓글이 삭제되었습니다.', variant: 'info' });
    } catch (e) {
        console.error(e);
        uiStore.alert('댓글 삭제에 실패했습니다.');
    }
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
    if (isReply) {
        payload.parent_comment_id = replyTargetId.value;
    }

    try {
        await createComment(post.value.id, payload);
        
        if (isReply) {
            replyContent.value = "";
            replyTargetId.value = null;
        } else {
            commentContent.value = "";
        }
        
        // 댓글 목록 갱신 및 좋아요/댓글 수 갱신
        const [cmtRes, postRes] = await Promise.all([
             getComments(post.value.id),
             getPostDetail(post.value.id)
        ]);
        
        if (cmtRes.data && Array.isArray(cmtRes.data.comments)) {
            comments.value = cmtRes.data.comments;
        } else if (Array.isArray(cmtRes.data)) {
            comments.value = cmtRes.data;
        }
        post.value = postRes.data; 
    } catch (e) {
        console.error(e);
        uiStore.alert('댓글 등록에 실패했습니다.');
    }
};

// Helper for Profile Image
const getProfileImage = (url) => {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return `http://127.0.0.1:8000${url}`;
};

const goProfile = (userId) => {
    if (!userId) return;
    router.push(`/profile/${userId}`);
};

const handleLike = async () => {
    if (!authStore.access && !localStorage.getItem("access_token")) {
        uiStore.alert('로그인이 필요합니다.');
        return;
    }
    await communityStore.handlePostLike(post.value);
};

const normalizedPrefix = (name) => name || '자유';

const fromNow = (iso) => {
  try {
    const d = new Date(iso);
    const diff = Date.now() - d.getTime();
    const sec = Math.floor(diff / 1000);
    if (sec < 60) return "방금 전";
    const min = Math.floor(sec / 60);
    if (min < 60) return `${min}분 전`;
    const hr = Math.floor(min / 60);
    if (hr < 24) return `${hr}시간 전`;
    const day = Math.floor(hr / 24);
    return `${day}일 전`;
  } catch {
    return "";
  }
};

onMounted(() => {
    fetchData();
});
</script>


<template>
  <div class="page" v-if="post">
    <div class="container">
        <!-- 본문 카드 -->
        <div class="post-card">
            <span class="badge">
                {{ normalizedPrefix(post.prefix_name) }}
            </span>
            <div class="post-title">
                {{ post.title }}
            </div>

            <div class="post-meta">
                <div 
                    class="avatar clickable"
                    @click="goProfile(post.user_id || post.user)"
                    :style="{ 
                        backgroundImage: post.user_profile_image ? `url(${getProfileImage(post.user_profile_image)})` : 'none' 
                    }"
                ></div>
                <div class="user-info">
                    <div class="clickable" @click="goProfile(post.user_id || post.user)">
                        {{ post.user_nickname }}
                    </div>
                    <div>{{ new Date(post.created_at).toLocaleString() }}</div>
                </div>
            </div>

            <div class="post-content">
                {{ post.content }}
            </div>

            <div class="action-bar">
                <!-- 좋아요 -->
                <button 
                    class="action-btn-pill like" 
                    :class="{ active: post.liked }"
                    @click="handleLike"
                >
                    <Heart :size="18" :fill="post.liked ? 'currentColor' : 'none'" />
                    좋아요 {{ post.like_count }}
                </button>
                <!-- 댓글 수 -->
                <div class="action-btn-pill comment">
                    <MessageCircle :size="18" />
                    댓글 {{ post.comment_count }}
                </div>
            </div>
        </div>

        <!-- 댓글 리스트 -->
        <div class="comments-section">
            <div class="comment-header">댓글 {{ comments.length }}</div>

            <div 
                v-for="cmt in comments" 
                :key="cmt.id"
            >
                <!-- 부모 댓글 -->
                <div class="comment-item">
                    <div 
                        class="avatar clickable" 
                        @click="goProfile(cmt.user_id || cmt.user)"
                        :style="{ 
                            backgroundImage: (cmt.user_profile_image || cmt.profile_image || cmt.author_image || cmt.user_profile) ? `url(${getProfileImage(cmt.user_profile_image || cmt.profile_image || cmt.author_image || cmt.user_profile)})` : 'none' 
                        }"
                    ></div> 
                    <div class="comment-bubble">
                        <div class="comment-author clickable" @click="goProfile(cmt.user_id || cmt.user)">
                            {{ cmt.user_nickname }} <span class="comment-time">{{ fromNow(cmt.created_at) }}</span>
                        </div>
                        <div class="comment-text">
                            {{ cmt.content }}
                        </div>
                        <!-- 댓글 액션 (좋아요, 답글달기) -->
                        <div class="comment-actions">
                            <button 
                                class="action-btn" 
                                :class="{ active: cmt.liked }"
                                @click="handleCommentLike(cmt)"
                            >
                                <Heart 
                                    :size="14" 
                                    :fill="cmt.liked ? '#ff4d6d' : 'none'" 
                                    :stroke="cmt.liked ? '#ff4d6d' : 'currentColor'"
                                />
                                좋아요 {{ cmt.like_count }}
                            </button>
                            <button class="action-btn" @click="toggleReply(cmt.id)">
                                <Reply :size="14" />
                                답글 달기
                            </button>
                            <button 
                                v-if="userProfile && (cmt.user_id === userProfile.id || cmt.user === userProfile.id)"
                                class="action-btn delete-btn"
                                @click="handleDeleteComment(cmt.id)"
                            >
                                <Trash2 :size="14" />
                                삭제
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 답글 입력창 (인라인) -->
                <div v-if="replyTargetId === cmt.id" class="reply-input-wrapper">
                    <div class="reply-avatar-sm" :style="{ 
                        backgroundImage: userProfile?.user_profile_image ? `url(${getProfileImage(userProfile.user_profile_image)})` : 'none' 
                    }"></div>
                    <div class="reply-input-box">
                        <input 
                            type="text" 
                            v-model="replyContent" 
                            placeholder="답글을 남겨주세요..."
                            @keydown.enter="submitComment"
                            class="r-input"
                        />
                        <button class="r-btn" @click="submitComment">
                            <SendHorizontal :size="18" />
                        </button>
                    </div>
                </div>

                <!-- 대댓글 (replies) -->
                <div 
                    v-for="reply in cmt.replies" 
                    :key="reply.id" 
                    class="reply-item"
                >
                    <div 
                        class="avatar reply-avatar clickable"
                        @click="goProfile(reply.user_id || reply.user)"
                        :style="{ 
                            backgroundImage: (reply.user_profile_image || reply.profile_image || reply.author_image || reply.user_profile) ? `url(${getProfileImage(reply.user_profile_image || reply.profile_image || reply.author_image || reply.user_profile)})` : 'none' 
                        }"
                    ></div>
                    <div class="comment-bubble reply-bubble">
                        <div class="comment-author clickable" @click="goProfile(reply.user_id || reply.user)">
                            {{ reply.user_nickname }} <span class="comment-time">{{ fromNow(reply.created_at) }}</span>
                        </div>
                        <div class="comment-text">
                            {{ reply.content }}
                        </div>
                        <div class="comment-actions">
                            <button 
                                class="action-btn" 
                                :class="{ active: reply.liked }"
                                @click="handleCommentLike(reply)"
                            >
                                <Heart 
                                    :size="14" 
                                    :fill="reply.liked ? '#ff4d6d' : 'none'" 
                                    :stroke="reply.liked ? '#ff4d6d' : 'currentColor'"
                                />
                                좋아요 {{ reply.like_count }}
                            </button>
                            <button 
                                v-if="userProfile && (reply.user_id === userProfile.id || reply.user === userProfile.id)"
                                class="action-btn delete-btn"
                                @click="handleDeleteComment(reply.id)"
                            >
                                <Trash2 :size="14" />
                                삭제
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 하단 입력창 -->
    <div class="comment-input-bar">
        <div class="input-wrapper">
            <input
                type="text"
                class="c-input"
                placeholder="따뜻한 댓글을 남겨주세요..."
                v-model="commentContent"
                @keydown.enter="submitComment"
            />
            <button class="c-btn-icon" @click="submitComment">
                <SendHorizontal :size="20" />
            </button>
        </div>
    </div>
  </div>
  <div v-else class="loading-container">
      불러오는 중...
  </div>
</template>

<style scoped>
.page {
    /* 변수 스코프 문제 해결 위해 직접 정의하거나 App.vue/global css에 있어야 함.
       여기선 직접 정의
    */
    --primary: #00d15b;
    --bg: #f2f4f6;
    --text: #191f28;
    --card-bg: #fff;

    font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--text);
    padding-bottom: 80px;
    min-height: 100vh;
}
.container {
    max-width: 700px;
    margin: 0 auto;
    padding: 20px;
}

/* 게시글 카드 */
.post-card {
    background: var(--card-bg);
    border-radius: 24px;
    padding: 40px 30px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    margin-bottom: 20px;
}

.badge {
    background: #e3f2fd;
    color: #007aff;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 4px 8px;
    border-radius: 6px;
    margin-bottom: 10px;
    display: inline-block;
}

.post-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}
.avatar {
    width: 40px;
    height: 40px;
    background: #eee;
    border-radius: 50%;
    background-size: cover;
    background-position: center;
}
.user-info div:first-child {
    font-weight: 700;
    font-size: 1rem;
}
.user-info div:last-child {
    font-size: 0.85rem;
    color: #8b95a1;
}

.post-title {
    font-size: 1.6rem;
    font-weight: 800;
    margin-bottom: 20px;
    line-height: 1.4;
}
.post-content {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #333;
    min-height: 100px;
    margin-bottom: 30px;
    white-space: pre-wrap; /* 줄바꿈 반영 */
}

.action-bar {
    display: flex;
    gap: 12px;
    border-top: 1px solid #f2f4f6;
    padding-top: 20px;
    font-weight: 600;
}
.action-btn-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 18px;
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: 0.2s;
}
.action-btn-pill.like {
    background: #fff0f3;
    color: #ff4d6d;
}
.action-btn-pill.like:hover {
    background: #ffe0e6;
}
.action-btn-pill.like.active {
    background: #ff4d6d;
    color: #fff;
}
.action-btn-pill.comment {
    background: #f2f4f6;
    color: #4e5968;
    cursor: default;
}

/* 댓글 영역 */
.comments-section {
    margin-top: 30px;
}
.comment-header {
    font-weight: 700;
    margin-bottom: 20px;
    font-size: 1.1rem;
}

.comment-item {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
}
.comment-bubble {
    background: #fff;
    padding: 16px;
    border-radius: 0 16px 16px 16px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
    flex: 1;
}
.comment-author {
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.clickable {
    cursor: pointer;
}
.clickable:hover {
    opacity: 0.8;
}
.comment-time {
    font-size: 0.8rem;
    color: #b0b8c1;
    font-weight: 400;
}
.comment-text {
    font-size: 0.95rem;
    color: #4e5968;
    line-height: 1.5;
}

/* 대댓글 스타일 */
.reply-item {
    margin-left: 50px;
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
}
.reply-bubble {
    background: #f9fafb;
    border: 1px solid #e5e8eb;
}
.reply-avatar {
    width: 30px; 
    height: 30px;
}

/* 댓글 입력바 */
.comment-input-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 15px 20px;
    border-top: 1px solid #eee;
    display: flex;
    justify-content: center;
    z-index: 50;
}
.input-wrapper {
    max-width: 700px;
    width: 100%;
    display: flex;
    gap: 10px;
}
.c-input {
    flex: 1;
    padding: 12px 20px;
    border-radius: 20px;
    border: 1px solid #eee;
    background: #f2f4f6;
    outline: none;
    font-size: 0.95rem;
}
.c-input:focus {
    background: #fff;
    border-color: var(--primary);
}
.c-btn-icon {
    background: var(--primary);
    color: white;
    border: none;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: 0.2s;
    flex-shrink: 0;
}
.c-btn-icon:hover {
    background: #00b54f;
    transform: scale(1.05);
}

.loading-container {
    padding: 50px;
    text-align: center;
    color: #888;
}

.comment-actions {
    display: flex;
    gap: 12px;
    margin-top: 8px;
}
.action-btn {
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    font-size: 0.8rem;
    color: #8b95a1;
    display: flex;
    align-items: center;
    gap: 4px;
    transition: 0.2s;
    line-height: 1;
}
.action-btn:hover, .action-btn.active {
    color: #ff4d6d;
}

/* 답글 입력창 스타일 */
.reply-input-wrapper {
    margin-left: 52px;
    margin-top: -12px;
    margin-bottom: 24px;
    display: flex;
    gap: 12px;
    align-items: center;
    animation: slideDown 0.2s ease-out;
}
@keyframes slideDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
.reply-avatar-sm {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #eee;
    background-size: cover;
    background-position: center;
}
.reply-input-box {
    flex: 1;
    display: flex;
    gap: 8px;
    background: #fff;
    padding: 6px 6px 6px 16px;
    border-radius: 20px;
    border: 1px solid #e5e8eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.r-input {
    flex: 1;
    border: none;
    outline: none;
    font-size: 0.9rem;
    background: transparent;
}
.r-btn {
    background: none;
    color: #ff4d6d;
    border: none;
    padding: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: 0.2s;
}
.r-btn:hover {
    opacity: 0.7;
}
</style>
