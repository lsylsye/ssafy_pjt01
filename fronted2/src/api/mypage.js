import api from "./axios";

export const getMyProfile = () => api.get("mypage/me/");
export const updateMyProfile = (data) => api.patch("mypage/me/", data);
export const getMyBookmarks = () => api.get("mypage/bookmarks/");
export const getMyPosts = (type) => api.get(`mypage/posts/${type ? `?type=${type}` : ""}`);
export const getMyComments = () => api.get("mypage/comments/");

// 팔로우 관련
export const toggleFollow = (userId) => api.post(`mypage/follow/${userId}/`);
export const getFollowers = (userId = null) =>
  userId ? api.get(`mypage/followers/${userId}/`) : api.get("mypage/followers/");
export const getFollowing = (userId = null) =>
  userId ? api.get(`mypage/following/${userId}/`) : api.get("mypage/following/");
export const getUserProfile = (userId) => api.get(`mypage/profile/${userId}/`);
