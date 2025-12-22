<template>
  <section>
    <p v-if="detailLoading">불러오는 중...</p>
    <p v-else-if="detailError" class="error">{{ detailError }}</p>

    <div v-else-if="post" class="card">
      <div class="head">
        <div class="hrow">
          <span v-if="post.prefix_name" class="prefix">[{{ post.prefix_name }}]</span>
          <h2 class="title">{{ post.title }}</h2>
        </div>

        <div class="meta">
          <!-- ✅ 작성자 닉네임 클릭 → 유저 프로필 이동 -->
          <router-link class="user-link" :to="`/users/${post.user_id}`">
            {{ post.user_nickname }}
          </router-link>

          <span>· {{ formatDate(post.created_at) }}</span>
          <span>· 좋아요 {{ likeCount }}</span>
          <span>· 댓글 {{ post.comment_count }}</span>
        </div>
      </div>

      <div v-if="!isEditing">
        <p class="content">{{ post.content }}</p>
      </div>

      <div v-else class="editbox">
        <FreePostForm
          :initial-title="post.title"
          :initial-content="post.content"
          :show-prefix="false"
          :disabled="saving"
          submit-text="저장"
          show-cancel
          :error-msg="editError"
          @submit="saveEdit"
          @cancel="cancelEdit"
        />
      </div>

      <div class="actions" v-if="!isEditing">
        <LikeButton
          :liked="liked"
          :count="likeCount"
          :disabled="likeLoading || !auth.isLoggedIn"
          @toggle="toggleLike"
        />

        <template v-if="auth.isLoggedIn">
          <button class="btn" @click="startEdit">수정</button>
          <button class="btn danger" @click="removePost">삭제</button>
        </template>
      </div>

      <hr class="line" />

      <h3>댓글</h3>

      <div v-if="!auth.isLoggedIn" class="need-login">
        댓글은 로그인 후 확인/작성할 수 있습니다.
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

    <p v-else>게시글이 없습니다.</p>
  </section>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";

import useCountry from "@/composables/useCountry";
import { useAuthStore } from "@/stores/auth";
import { useFreeStore } from "@/stores/community/free";

import LikeButton from "@/components/community/LikeButton.vue";
import CommentForm from "@/components/community/CommentForm.vue";
import CommentList from "@/components/community/CommentList.vue";
import FreePostForm from "@/components/community/free/FreePostForm.vue";

const route = useRoute();
const router = useRouter();
const { country } = useCountry();

const auth = useAuthStore();
const store = useFreeStore();

const {
  detailLoading,
  detailError,
  post,
  liked,
  likeCount,
  likeLoading,
  cLoading,
  cError,
  comments,
} = storeToRefs(store);

const postId = computed(() => String(route.params.postId || ""));

const formatDate = (iso) => (typeof iso === "string" ? iso.slice(0, 10) : "");

const fetchAll = () => {
  store
    .fetchDetail(country.value, postId.value)
    .then(() => {
      if (auth.isLoggedIn) return store.fetchComments(country.value, postId.value);
    })
    .catch(() => {});
};

onMounted(fetchAll);

watch(
  () => `${country.value}-${postId.value}-${auth.isLoggedIn}`,
  () => fetchAll()
);

const toggleLike = () => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }

  store.toggleLike(country.value, postId.value).catch(() => {
    alert("좋아요 처리에 실패했습니다.");
  });
};

const isEditing = ref(false);
const saving = ref(false);
const editError = ref("");

const startEdit = () => {
  isEditing.value = true;
  editError.value = "";
};

const cancelEdit = () => {
  isEditing.value = false;
  editError.value = "";
};

const saveEdit = (payload) => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }

  const body = {};
  if (payload.title && payload.title !== (post.value?.title || "")) body.title = payload.title;
  if (payload.content && payload.content !== (post.value?.content || "")) body.content = payload.content;

  if (Object.keys(body).length === 0) {
    isEditing.value = false;
    return;
  }

  saving.value = true;
  editError.value = "";

  store
    .patchPost(country.value, postId.value, body)
    .then(() => {
      isEditing.value = false;
    })
    .catch(() => {
      editError.value = "글 수정에 실패했습니다.";
    })
    .finally(() => {
      saving.value = false;
    });
};

const removePost = () => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }
  if (!confirm("정말 삭제할까요?")) return;

  store
    .removePost(country.value, postId.value)
    .then(() => {
      router.push(`/community/${country.value}/free`);
    })
    .catch(() => {
      alert("글 삭제에 실패했습니다.");
    });
};

// comments
const writeComment = (content) => {
  store
    .createComment(country.value, postId.value, { content })
    .catch(() => alert("댓글 작성에 실패했습니다."));
};

const writeReply = ({ parentId, content }) => {
  store
    .createComment(country.value, postId.value, { content, parent_comment_id: parentId })
    .catch(() => alert("답글 작성에 실패했습니다."));
};

const removeComment = (commentId) => {
  if (!confirm("댓글을 삭제할까요?")) return;

  store
    .removeComment(country.value, postId.value, commentId)
    .catch(() => alert("댓글 삭제에 실패했습니다."));
};

const likeComment = (commentId) => {
  store
    .likeComment(country.value, postId.value, commentId)
    .catch(() => alert("댓글 좋아요에 실패했습니다."));
};
</script>

<style scoped>
.error { color:#d33; }
.card { border:1px solid #eee; border-radius:12px; padding:14px; }
.head { margin-bottom:12px; }
.hrow { display:flex; gap:8px; align-items:center; }
.prefix { color:#1a73e8; font-weight:800; }
.title { margin:0; }
.meta { margin-top:6px; color:#666; font-size:14px; display:flex; gap:8px; flex-wrap:wrap; }

.user-link{
  color:#1a73e8;
  text-decoration:none;
  cursor:pointer;
}
.user-link:hover{
  text-decoration:underline;
}

.content { margin:12px 0 0; line-height:1.6; white-space:pre-wrap; }
.actions { margin-top:12px; display:flex; gap:8px; align-items:center; }
.btn { border:1px solid #ddd; background:white; border-radius:10px; padding:8px 12px; cursor:pointer; }
.btn:hover { border-color:#1a73e8; color:#1a73e8; }
.btn.danger { border-color:#f2b8b5; }
.btn.danger:hover { border-color:#d33; color:#d33; }
.line { border:none; border-top:1px solid #eee; margin:16px 0; }
.need-login { color:#666; background:#fafafa; border:1px solid #eee; padding:10px; border-radius:10px; }
.editbox { margin-top:12px; }
</style>
