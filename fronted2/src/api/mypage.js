import api from "@/api/axios";

// 내 정보 조회
export function getMyProfile() {
  return api.get("mypage/me/");
}

// 내 정보 수정
export function updateMyProfile(data) {
  // data should be FormData if uploading image, or JSON otherwise.
  // The backend supports MultiPartParser, so we can send FormData.
  return api.patch("mypage/me/", data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

// 내 북마크 조회
export function getMyBookmarks() {
  return api.get("mypage/bookmarks/");
}

// 내가 작성한 글 조회
export function getMyPosts() {
  return api.get("mypage/posts/");
}

// 내가 작성한 댓글 조회
export function getMyComments() {
  return api.get("mypage/comments/");
}

export function getMyPageStats() {
  return api.get("mypage/");
}
