import { createRouter, createWebHistory } from 'vue-router'

import MainView from '@/views/main/MainView.vue'

import LoginView from '@/views/auth/LoginView.vue'
import SignupView from '@/views/auth/SignupView.vue'

import SearchView from '@/views/books/SearchView.vue'
import BookDetailView from '@/views/books/BookDetailView.vue'

import LibraryView from '@/views/library/LibraryView.vue'

import MyPageView from '@/views/mypage/MyPageView.vue'
import MyInfoView from '@/views/mypage/MyInfoView.vue'
import MyBookmarksView from '@/views/mypage/MyBookmarksView.vue'

// ✅ Community
import CommunityLayoutView from '@/views/community/CommunityLayoutView.vue'
import CommunityFreeLayoutView from '@/views/community/free/CommunityFreeLayoutView.vue'
import CommunityFreeListView from '@/views/community/free/CommunityFreeListView.vue'
import CommunityFreeWriteView from '@/views/community/free/CommunityFreeWriteView.vue'
import CommunityFreeDetailView from '@/views/community/free/CommunityFreeDetailView.vue'

// ✅ Review (추가)
import CommunityReviewLayoutView from '@/views/community/review/CommunityReviewLayoutView.vue'
import ReviewListView from '@/views/community/review/ReviewListView.vue'
import ReviewWriteView from '@/views/community/review/ReviewWriteView.vue'
import ReviewDetailView from '@/views/community/review/ReviewDetailView.vue'
import ReviewEditView from '@/views/community/review/ReviewEditView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: MainView },
    { path: '/login', component: LoginView },
    { path: '/signup', component: SignupView },
    { path: '/search', component: SearchView },
    { path: '/books/:isbn13', component: BookDetailView },
    { path: '/library', component: LibraryView },

    {
      path: '/mypage',
      component: MyPageView,
      children: [
        { path: '', component: MyInfoView },
        { path: 'bookmarks', component: MyBookmarksView },
      ],
    },

    // ✅ /community/:country 아래에 free / review 탭 중첩
    {
      path: '/community/:country',
      component: CommunityLayoutView,
      children: [
        { path: '', redirect: 'free' },

        {
          path: 'free',
          component: CommunityFreeLayoutView,
          children: [
            { path: '', component: CommunityFreeListView },          // /community/kr/free
            { path: 'write', component: CommunityFreeWriteView },     // /community/kr/free/write
            { path: ':postId', component: CommunityFreeDetailView },  // /community/kr/free/3
          ],
        },

        {
          path: 'review',
          component: CommunityReviewLayoutView,
          children: [
            { path: '', component: ReviewListView },                 // /community/kr/review
            { path: 'write', component: ReviewWriteView },           // /community/kr/review/write
            { path: ':reviewId', component: ReviewDetailView },      // /community/kr/review/2
            { path: ':reviewId/edit', component: ReviewEditView },
            

          ],
        },
      ],
    },
  ],
})

export default router
