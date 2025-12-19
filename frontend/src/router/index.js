import { createRouter, createWebHistory } from 'vue-router'

import MainView from '@/views/MainView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import SearchView from '@/views/SearchView.vue'
import CommunityView from '@/views/CommunityView.vue'
import LibraryView from '@/views/LibraryView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: MainView },          // 베스트셀러
    { path: '/login', component: LoginView },    // 로그인 API
    { path: '/signup', component: SignupView },  // 회원가입 API
    { path: '/search', component: SearchView },  // 도서 검색 API
    { path: '/community/:country', component: CommunityView },
    { path: '/library', component: LibraryView },
  ],
})

export default router
