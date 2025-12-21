<template>
  <section>
    <p v-if="loading">불러오는 중...</p>
    <p v-else-if="errorMsg" class="error">{{ errorMsg }}</p>

    <div v-else-if="post" class="card">
      <div class="head">
        <div class="hrow">
          <span v-if="post.prefix_name" class="prefix">[{{ post.prefix_name }}]</span>
          <h2 class="title">{{ post.title }}</h2>
        </div>

        <div class="meta">
          <span>{{ post.user_nickname }}</span>
          <span>· {{ formatDate(post.created_at) }}</span>
          <span>· 좋아요 {{ likeCount }}</span>
          <span>· 댓글 {{ post.comment_count }}</span>
        </div>
      </div>

      <!-- ✅ 본문 / 수정모드 -->
      <div v-if="!isEditing">
        <p class="content">{{ post.content }}</p>
      </div>

      <div v-else class="editbox">
        <input v-model="editTitle" class="input" placeholder="제목" />
        <textarea v-model="editContent" class="textarea" placeholder="내용"></textarea>

        <div class="actions">
          <button class="btn" :disabled="saving" @click="saveEdit">저장</button>
          <button class="btn" :disabled="saving" @click="cancelEdit">취소</button>
        </div>

        <p v-if="editError" class="error">{{ editError }}</p>
      </div>

      <!-- ✅ 버튼 영역 -->
      <div class="actions" v-if="!isEditing">
        <button class="btn" @click="toggleLike">
          {{ liked ? '좋아요 취소' : '좋아요' }}
        </button>

        <!-- ✅ 수정/삭제: 로그인 상태에서만 노출 (백엔드가 작성자만 허용) -->
        <template v-if="auth.isLoggedIn">
          <button class="btn" @click="startEdit">수정</button>
          <button class="btn danger" @click="deletePost">삭제</button>
        </template>
      </div>

      <hr class="line" />

      <h3>댓글</h3>

      <div v-if="!auth.isLoggedIn" class="need-login">
        댓글은 로그인 후 확인/작성할 수 있습니다.
      </div>

      <div v-else>
        <div class="comment-write">
          <input v-model="newComment" class="input" placeholder="댓글을 입력하세요" />
          <button class="btn" @click="writeComment()">등록</button>
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
                <button class="linkbtn" @click="likeComment(c.id)">좋아요</button>
                <button class="linkbtn" @click="removeComment(c.id)">삭제</button>
                <button class="linkbtn" @click="startReply(c.id)">답글</button>
              </div>

              <div v-if="replyingTo === c.id" class="replybox">
                <input v-model="replyText" class="input" placeholder="답글 입력" />
                <button class="btn" @click="writeComment(c.id)">등록</button>
                <button class="btn" @click="cancelReply">취소</button>
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
                    <button class="linkbtn" @click="likeComment(r.id)">좋아요</button>
                    <button class="linkbtn" @click="removeComment(r.id)">삭제</button>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <p v-else>게시글이 없습니다.</p>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const country = computed(() => String(route.params.country || 'kr'))
const postId = computed(() => String(route.params.postId || ''))

const apiCountry = (c) => String(c || 'kr').toLowerCase()
const formatDate = (iso) => (typeof iso === 'string' ? iso.slice(0, 10) : '')

const requireTokenOrGoLogin = () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return null
  }
  return token
}

const loading = ref(false)
const errorMsg = ref('')
const post = ref(null)

const liked = ref(false)
const likeCount = ref(0)

const cLoading = ref(false)
const cError = ref('')
const comments = ref([])

const newComment = ref('')
const replyingTo = ref(null)
const replyText = ref('')

/* =========================
   ✅ 게시글 상세
========================= */
const fetchDetail = () => {
  loading.value = true
  errorMsg.value = ''
  post.value = null

  const c = apiCountry(country.value)

  api.get(`/api/community/${c}/free/${postId.value}/`)
    .then((res) => {
      post.value = res.data
      likeCount.value = res.data?.like_count || 0
      liked.value = false
    })
    .catch((err) => {
      console.error('[상세 실패]', err.response?.data || err.message)
      errorMsg.value = '게시글을 불러오지 못했습니다.'
    })
    .finally(() => {
      loading.value = false
    })
}

/* =========================
   ✅ 좋아요
========================= */
const toggleLike = () => {
  const token = requireTokenOrGoLogin()
  if (!token) return

  const c = apiCountry(country.value)

  api.post(
    `/api/community/${c}/free/${postId.value}/like/`,
    {},
    { headers: { Authorization: `Bearer ${token}` } }
  )
    .then((res) => {
      liked.value = !!res.data.liked
      likeCount.value = res.data.like_count ?? likeCount.value
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[좋아요 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout?.()
        router.push('/login')
        return
      }
      alert('좋아요 처리에 실패했습니다.')
    })
}

/* =========================
   ✅ 게시글 수정/삭제 (말머리 건드리지 않음)
========================= */
const isEditing = ref(false)
const saving = ref(false)
const editError = ref('')

const editTitle = ref('')
const editContent = ref('')

const startEdit = () => {
  if (!post.value) return
  isEditing.value = true
  editError.value = ''
  editTitle.value = post.value.title || ''
  editContent.value = post.value.content || ''
}

const cancelEdit = () => {
  isEditing.value = false
  editError.value = ''
}

const saveEdit = () => {
  const token = requireTokenOrGoLogin()
  if (!token) return
  if (!post.value) return

  const t = editTitle.value.trim()
  const ctt = editContent.value.trim()

  if (!t || !ctt) {
    editError.value = '제목/내용은 필수입니다.'
    return
  }

  // ✅ 바뀐 값만 PATCH로 전송 (title, content만)
  const body = {}
  if (t !== (post.value.title || '')) body.title = t
  if (ctt !== (post.value.content || '')) body.content = ctt

  if (Object.keys(body).length === 0) {
    isEditing.value = false
    return
  }

  const c = apiCountry(country.value)

  saving.value = true
  editError.value = ''

  api.patch(
    `/api/community/${c}/free/${postId.value}/`,
    body,
    { headers: { Authorization: `Bearer ${token}` } }
  )
    .then(() => {
      isEditing.value = false
      fetchDetail() // ✅ 서버 데이터로 싱크
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[글 수정 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout?.()
        router.push('/login')
        return
      }
      if (status === 403) {
        editError.value = '작성자만 수정할 수 있습니다.'
        return
      }
      editError.value = '글 수정에 실패했습니다.'
    })
    .finally(() => {
      saving.value = false
    })
}

const deletePost = () => {
  const token = requireTokenOrGoLogin()
  if (!token) return

  const ok = confirm('정말 삭제할까요?')
  if (!ok) return

  const c = apiCountry(country.value)

  api.delete(
    `/api/community/${c}/free/${postId.value}/`,
    { headers: { Authorization: `Bearer ${token}` } }
  )
    .then(() => {
      router.push(`/community/${country.value}/free`)
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[글 삭제 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout?.()
        router.push('/login')
        return
      }
      if (status === 403) {
        alert('작성자만 삭제할 수 있습니다.')
        return
      }
      alert('글 삭제에 실패했습니다.')
    })
}

/* =========================
   ✅ 댓글
========================= */
const syncCommentCountWithList = () => {
  if (post.value) post.value.comment_count = comments.value.length
}

const fetchComments = () => {
  if (!auth.isLoggedIn) return
  const token = requireTokenOrGoLogin()
  if (!token) return

  const c = apiCountry(country.value)

  cLoading.value = true
  cError.value = ''
  comments.value = []

  api.get(`/api/community/${c}/free/${postId.value}/comments/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((res) => {
      comments.value = Array.isArray(res.data?.comments) ? res.data.comments : []
      syncCommentCountWithList()
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[댓글 목록 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout?.()
        router.push('/login')
        return
      }
      cError.value = '댓글을 불러오지 못했습니다.'
    })
    .finally(() => {
      cLoading.value = false
    })
}

const writeComment = (parentId) => {
  const token = requireTokenOrGoLogin()
  if (!token) return

  const text = parentId ? replyText.value.trim() : newComment.value.trim()
  if (!text) return

  const c = apiCountry(country.value)
  const body = parentId
    ? { content: text, parent_comment_id: parentId }
    : { content: text }

  api.post(
    `/api/community/${c}/free/${postId.value}/comments/write`,
    body,
    { headers: { Authorization: `Bearer ${token}` } }
  )
    .then(() => {
      newComment.value = ''
      replyingTo.value = null
      replyText.value = ''

      if (post.value) post.value.comment_count = (post.value.comment_count || 0) + 1
      fetchComments()
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[댓글 작성 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout?.()
        router.push('/login')
        return
      }
      alert('댓글 작성에 실패했습니다.')
    })
}

const removeComment = (commentId) => {
  const token = requireTokenOrGoLogin()
  if (!token) return

  api.delete(`/api/community/comments/${commentId}/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then(() => {
      if (post.value && post.value.comment_count > 0) post.value.comment_count -= 1
      fetchComments()
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[댓글 삭제 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout?.()
        router.push('/login')
        return
      }
      alert('댓글 삭제에 실패했습니다.')
    })
}

const likeComment = (commentId) => {
  const token = requireTokenOrGoLogin()
  if (!token) return

  api.post(
    `/api/community/comments/${commentId}/like/`,
    {},
    { headers: { Authorization: `Bearer ${token}` } }
  )
    .then(() => {
      fetchComments()
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[댓글 좋아요 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout?.()
        router.push('/login')
        return
      }
      alert('댓글 좋아요에 실패했습니다.')
    })
}

const startReply = (commentId) => {
  replyingTo.value = commentId
  replyText.value = ''
}
const cancelReply = () => {
  replyingTo.value = null
  replyText.value = ''
}

onMounted(() => {
  fetchDetail()
  fetchComments()
})

watch(
  () => `${country.value}-${postId.value}-${auth.isLoggedIn}`,
  () => {
    fetchDetail()
    fetchComments()
  }
)
</script>

<style scoped>
.error { color: #d33; }
.card { border: 1px solid #eee; border-radius: 12px; padding: 14px; }

.head { margin-bottom: 12px; }
.hrow { display: flex; gap: 8px; align-items: center; }
.prefix { color: #1a73e8; font-weight: 800; }
.title { margin: 0; }

.meta { margin-top: 6px; color: #666; font-size: 14px; display: flex; gap: 8px; flex-wrap: wrap; }

.content { margin: 12px 0 0; line-height: 1.6; }

.actions { margin-top: 12px; }
.btn {
  border: 1px solid #ddd;
  background: white;
  border-radius: 10px;
  padding: 8px 12px;
  cursor: pointer;
  margin-right: 8px;
}
.btn:hover { border-color: #1a73e8; color: #1a73e8; }

.btn.danger { border-color: #f2b8b5; }
.btn.danger:hover { border-color: #d33; color: #d33; }

.line { border: none; border-top: 1px solid #eee; margin: 16px 0; }

.need-login { color: #666; background: #fafafa; border: 1px solid #eee; padding: 10px; border-radius: 10px; }

.comment-write { display: flex; gap: 8px; margin: 10px 0 14px; }
.input { flex: 1; border: 1px solid #ddd; border-radius: 10px; padding: 8px 10px; }
.textarea{
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 10px 12px;
  min-height: 160px;
  resize: vertical;
}

.clist { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.citem { border: 1px solid #eee; border-radius: 12px; padding: 10px 12px; }

.cmeta { color: #666; font-size: 13px; display: flex; gap: 10px; flex-wrap: wrap; }
.nick { font-weight: 700; color: #333; }
.ctext { margin: 6px 0 0; }

.cactions { margin-top: 8px; display: flex; gap: 10px; }
.linkbtn { border: none; background: none; color: #1a73e8; cursor: pointer; padding: 0; }

.replybox { display: flex; gap: 8px; margin-top: 8px; }

.rlist { list-style: none; padding: 0; margin: 10px 0 0 18px; display: flex; flex-direction: column; gap: 10px; }
.ritem { border: 1px dashed #e6e6e6; border-radius: 12px; padding: 10px 12px; background: #fcfcfc; }

.editbox { margin-top: 12px; }
</style>
