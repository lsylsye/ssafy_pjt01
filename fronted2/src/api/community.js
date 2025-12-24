import api from "@/api/axios";

/**
 * GET /api/community/free/
 * Query(옵션): q, prefix
 * 인증 X  → auth:false로 토큰 안 붙여서 401 이슈 방지
 */
export function getFreePosts({ q = "", prefix = "" } = {}) {
  const params = {};
  if (q) params.q = q;
  if (prefix) params.prefix = prefix;

  return api.get("community/free/", {
    params,
    auth: false,
  });
}
