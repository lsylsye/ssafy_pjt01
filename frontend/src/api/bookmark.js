import api from '@/api/axios'

export const fetchMyBookmarks = (token) =>
  api.get('/api/mypage/bookmarks/', {
    headers: { Authorization: `Bearer ${token}` },
  })

export const toggleBookmarkApi = (isbn13, token) =>
  api.post(
    `/api/books/${isbn13}/bookmark/`,
    {},
    { headers: { Authorization: `Bearer ${token}` } }
  )
