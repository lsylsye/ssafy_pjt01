import api from "@/api/axios";

// ✅ 다른 유저 프로필 조회
export const getUserProfile = (userId) => {
  return api.get(`/api/users/profile/${userId}/`);
};

// ✅ 팔로우/언팔로우 토글 (로그인 필요)
export const toggleFollow = (userId) => {
  return api.post(`/api/users/${userId}/follow/`);
};
