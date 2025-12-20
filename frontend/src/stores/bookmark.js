import { defineStore } from 'pinia'
import { fetchMyBookmarks, toggleBookmarkApi } from '@/api/bookmark'

export const useBookmarkStore = defineStore('bookmark', {
  state: () => ({
    isbnSet: new Set(),     // 로그인 유저 북마크 isbn13 캐시
    synced: false,          // 한 번이라도 불러왔는지
  }),

  actions: {
    _token() {
      return localStorage.getItem('access_token')
    },

    _normalizeToIsbnList(data) {
      const arr = Array.isArray(data) ? data : (Array.isArray(data?.results) ? data.results : [])
      return arr
        .map((x) => (typeof x === 'string' ? x : (x?.isbn13 || x?.book?.isbn13 || null)))
        .filter(Boolean)
        .map(String)
    },

    isBookmarked(isbn13) {
      return this.isbnSet.has(String(isbn13))
    },

    sync() {
      const token = this._token()
      if (!token) {
        this.isbnSet = new Set()
        this.synced = false
        return Promise.resolve()
      }

      return fetchMyBookmarks(token)
        .then((res) => {
          const list = this._normalizeToIsbnList(res.data)
          this.isbnSet = new Set(list)
          this.synced = true
        })
        .catch((err) => {
          if (err.response?.status === 401) {
            localStorage.removeItem('access_token')
          }
          this.isbnSet = new Set()
          this.synced = false
        })
    },

    toggle(isbn13) {
      const token = this._token()
      if (!token) return Promise.reject({ code: 'LOGIN_REQUIRED' })

      return toggleBookmarkApi(isbn13, token)
        .then((res) => {
          const on = !!res.data.bookmarked
          const key = String(isbn13)

          if (on) this.isbnSet.add(key)
          else this.isbnSet.delete(key)

          return res.data // {bookmarked, created}
        })
    },
  },
})
