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

      <p class="content">{{ post.content }}</p>

      <div class="actions">
        <button class="btn" @click="toggleLike">
          {{ liked ? '좋아요 취소' : '좋아요' }}
        </button>
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

              <!-- replies (2단계까지만) -->
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

const formatDate = (iso) => (typeof iso === 'string' ? iso.slice(0, 10) : '')

const fetchDetail = () => {
  loading.value = true
  errorMsg.value = ''
  post.value = null

  api.get(`/api/community/${country.value}/free/${postId.value}/`)
    .then((res) => {
      post.value = res.data
      likeCount.value = res.data?.like_count || 0
      liked.value = false // 서버에서 liked를 안 주니까 초기 false
    })
    .catch((err) => {
      console.error('[상세 실패]', err.response?.data || err.message)
      errorMsg.value = '게시글을 불러오지 못했습니다.'
    })
    .finally(() => {
      loading.value = false
    })
}

const toggleLike = () => {
  if (!auth.isLoggedIn) {
    router.push('/login')
    return
  }
  const token = localStorage.getItem('access_token')

  api.post(
    `/api/community/${country.value}/free/${postId.value}/like/`,
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
        auth.logout()
        router.push('/login')
        return
      }
      alert('좋아요 처리에 실패했습니다.')
    })
}

const fetchComments = () => {
  if (!auth.isLoggedIn) return

  const token = localStorage.getItem('access_token')
  cLoading.value = true
  cError.value = ''
  comments.value = []

  api.get(`/api/community/${country.value}/free/${postId.value}/comments/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((res) => {
      comments.value = Array.isArray(res.data?.comments) ? res.data.comments : []
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[댓글 목록 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout()
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
  if (!auth.isLoggedIn) {
    router.push('/login')
    return
  }

  const text = parentId ? replyText.value.trim() : newComment.value.trim()
  if (!text) return

  const token = localStorage.getItem('access_token')
  const body = parentId
    ? { content: text, parent_comment_id: parentId }
    : { content: text }

  api.post(
    `/api/community/${country.value}/free/${postId.value}/comments/write`,
    body,
    { headers: { Authorization: `Bearer ${token}` } }
  )
    .then(() => {
      newComment.value = ''
      replyingTo.value = null
      replyText.value = ''
      fetchComments()
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[댓글 작성 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout()
        router.push('/login')
        return
      }
      alert('댓글 작성에 실패했습니다.')
    })
}

const removeComment = (commentId) => {
  if (!auth.isLoggedIn) {
    router.push('/login')
    return
  }
  const token = localStorage.getItem('access_token')

  api.delete(`/api/community/comments/${commentId}/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then(() => {
      fetchComments()
    })
    .catch((err) => {
      const status = err.response?.status
      console.error('[댓글 삭제 실패]', err.response?.data || err.message)

      if (status === 401) {
        auth.logout()
        router.push('/login')
        return
      }
      alert('댓글 삭제에 실패했습니다.')
    })
}

const likeComment = (commentId) => {
  if (!auth.isLoggedIn) {
    router.push('/login')
    return
  }
  const token = localStorage.getItem('access_token')

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
        auth.logout()
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

.line { border: none; border-top: 1px solid #eee; margin: 16px 0; }

.need-login { color: #666; background: #fafafa; border: 1px solid #eee; padding: 10px; border-radius: 10px; }

.comment-write { display: flex; gap: 8px; margin: 10px 0 14px; }
.input { flex: 1; border: 1px solid #ddd; border-radius: 10px; padding: 8px 10px; }

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
</style>
