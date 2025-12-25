import api from "@/api/axios";

/**
 * GET /api/community/free/
 * Query(옵션): q, prefix
 * 인증 X  → auth:false로 토큰 안 붙여서 401 이슈 방지
 */
// 이미 존재하는 getFreePosts ...
export function getFreePosts({ q = "", prefix = "", page = 1 } = {}) {
  const params = {};
  if (q) params.q = q;
  if (prefix) params.prefix = prefix;
  if (page) params.page = page;

  return api.get("community/free/", {
    params,
    auth: false,
  });
}

/**
 * GET /api/community/free/prefixes/
 * 말머리 목록 조회
 */
export function getPrefixes() {
  return api.get("community/free/prefixes/", {
    auth: false, // 만약 인증 필요없으면. 보통 말머리 목록은 공개.
  });
}

/**
 * POST /api/community/free/write/
 * 게시글 작성
 * payload: { title, content, prefix_id(옵션?) }
 */
export function createPost(payload) {
  // 인증 필요 (헤더에 토큰 등은 인터셉터 처리가 되어있다고 가정하거나, auth:true 플래그 사용)
  // axios.js를 보면 인터셉터 설정이 안보임. 
  // router/index.js에서 localStorage 체크함.
  // 보통 axios 인터셉터에서 토큰을 넣는데, 여기 axios.js는 단순함.
  // 직접 헤더를 넣어야 할 수도 있음.
  // 하지만 auth.store.js나 다른 곳에서 인터셉터를 추가하는지 확인해봐야함.
  // 일단 단순히 post 호출. 인터셉터가 없으면 headers에 넣어줘야 할 수도 있음.
  const token = localStorage.getItem("access_token");
  const config = {};
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }

  return api.post("community/free/write/", payload, config);
}

/**
 * GET /api/community/free/{id}/
 */
export function getPostDetail(id) {
  const token = localStorage.getItem("access_token");
  const config = {};
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  return api.get(`community/free/${id}/`, config);
}

/**
 * DELETE /api/community/free/{id}/
 */
export function deletePost(id) {
  const token = localStorage.getItem("access_token");
  const config = {};
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  return api.delete(`community/free/${id}/`, config);
}

/**
 * PATCH /api/community/free/{id}/
 */
export function updatePost(id, payload) {
  const token = localStorage.getItem("access_token");
  const config = {};
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  return api.patch(`community/free/${id}/`, payload, config);
}

/**
 * POST /api/community/free/{id}/like/
 */
export function toggleLike(id) {
  const token = localStorage.getItem("access_token");
  const config = {};
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  return api.post(`community/free/${id}/like/`, {}, config);
}

/**
 * GET /api/community/free/{id}/comments/
 */
export function getComments(postId) {
  const token = localStorage.getItem("access_token");
  const config = {};
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  return api.get(`community/free/${postId}/comments/`, config);
}

/**
 * POST /api/community/free/{id}/comments/write/
 * payload: { content }
 */
export function createComment(postId, payload) {
  const token = localStorage.getItem("access_token");
  const config = {};
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  return api.post(`community/free/${postId}/comments/write/`, payload, config);
}

/**
 * DELETE /api/community/free/{postId}/comments/{commentId}/
 */
export function deleteComment(postId, commentId) {
  const token = localStorage.getItem("access_token");
  const config = {};
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  return api.delete(`community/free/${postId}/comments/${commentId}/`, config);
}

/**
 * POST /api/community/comments/{commentId}/like/
 */
export function toggleCommentLike(commentId) {
  const token = localStorage.getItem("access_token");
  const config = {};
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  return api.post(`community/comments/${commentId}/like/`, {}, config);
}

/**
 * DELETE /api/community/comments/{comment_id}/ (가정)
 * URL 구조가 명확하지 않으므로, 보통 댓글 삭제는 
 * DELETE /api/community/free/{postId}/comments/{commentId}/ 
 * 혹은 DELETE /api/community/comments/{commentId}/ 일 수 있음.
 * 일단 명확하지 않으니 생략하거나 필요시 추가.
 */
