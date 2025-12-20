import { createRouter, createWebHistory } from 'vue-router'

import MainView from '@/views/main/MainView.vue'

import LoginView from '@/views/auth/LoginView.vue'
import SignupView from '@/views/auth/SignupView.vue'

import SearchView from '@/views/books/SearchView.vue'
import BookDetailView from '@/views/books/BookDetailView.vue'

import CommunityView from '@/views/community/CommunityView.vue'
import LibraryView from '@/views/library/LibraryView.vue'

import MyPageView from '@/views/mypage/MyPageView.vue'
import MyInfoView from '@/views/mypage/MyInfoView.vue'
import MyBookmarksView from '@/views/mypage/MyBookmarksView.vue'


const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: MainView },
    { path: '/login', component: LoginView },
    { path: '/signup', component: SignupView },
    { path: '/search', component: SearchView },
    { path: '/books/:isbn13', component: BookDetailView },
    { path: '/community/:country', component: CommunityView },
    { path: '/library', component: LibraryView },

    {
      path: '/mypage',
      component: MyPageView,
      children: [
        { path: '', component: MyInfoView },
        { path: 'bookmarks', component: MyBookmarksView },
      ],
    },
  ],
})

export default router
