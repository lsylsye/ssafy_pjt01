import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
  }),

  getters: {
    isLoggedIn: (state) => !!state.accessToken,
  },

  actions: {
    setTokens({ access, refresh }) {
      this.accessToken = access || ''
      this.refreshToken = refresh || ''

      if (access) localStorage.setItem('access_token', access)
      else localStorage.removeItem('access_token')

      if (refresh) localStorage.setItem('refresh_token', refresh)
      else localStorage.removeItem('refresh_token')
    },

    logout() {
      this.accessToken = ''
      this.refreshToken = ''
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
})
