import { createRouter, createWebHistory } from "vue-router";

// ✅ 너 프로젝트 기존 라우트들(경로는 네 프로젝트에 맞게 유지)
import MainView from "@/views/main/MainView.vue";
import LoginView from "@/views/auth/LoginView.vue";
import SignupView from "@/views/auth/SignupView.vue";
import SearchView from "@/views/books/SearchView.vue";
import BookDetailView from "@/views/books/BookDetailView.vue";
import LibraryView from "@/views/library/LibraryView.vue";

import MyPageView from "@/views/mypage/MyPageView.vue";
import MyInfoView from "@/views/mypage/MyInfoView.vue";
import MyBookmarksView from "@/views/mypage/MyBookmarksView.vue";
import FollowersView from "@/views/mypage/FollowersView.vue";
import FollowingView from "@/views/mypage/FollowingView.vue";

// ✅ community
import CommunityLayoutView from "@/views/community/CommunityLayoutView.vue";

// free
import FreeLayoutView from "@/views/community/free/FreeLayoutView.vue";
import FreeListView from "@/views/community/free/FreeListView.vue";
import FreeWriteView from "@/views/community/free/FreeWriteView.vue";
import FreeDetailView from "@/views/community/free/FreeDetailView.vue";

// review
import ReviewLayoutView from "@/views/community/review/ReviewLayoutView.vue";
import ReviewListView from "@/views/community/review/ReviewListView.vue";
import ReviewWriteView from "@/views/community/review/ReviewWriteView.vue";
import ReviewDetailView from "@/views/community/review/ReviewDetailView.vue";
import ReviewEditView from "@/views/community/review/ReviewEditView.vue";

// follow
import UserProfileView from "@/views/users/UserProfileView.vue";

// grass
import MyGrassView from "@/views/mypage/MyGrassView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: MainView },
    { path: "/login", component: LoginView },
    { path: "/signup", component: SignupView },
    { path: "/search", component: SearchView },
    { path: "/books/:isbn13", component: BookDetailView },
    { path: "/library", component: LibraryView },
    { path: "/users/:userId", component: UserProfileView },


    {
      path: "/mypage",
      component: MyPageView,
      children: [
        { path: "", component: MyInfoView },
        { path: "bookmarks", component: MyBookmarksView },
        { path: "followers", name: "mypage-followers", component: FollowersView },
        { path: "following", name: "mypage-following", component: FollowingView },
        { path: "grass", name: "mypage-grass", component: MyGrassView },
      ],
    },

    {
      path: "/community/:country",
      component: CommunityLayoutView,
      children: [
        { path: "", redirect: "free" },

        {
          path: "free",
          component: FreeLayoutView,
          children: [
            { path: "", name: "free-list", component: FreeListView },
            { path: "write", name: "free-write", component: FreeWriteView },
            { path: ":postId", name: "free-detail", component: FreeDetailView },
          ],
        },

        {
          path: "review",
          component: ReviewLayoutView,
          children: [
            { path: "", name: "review-list", component: ReviewListView },
            { path: "write", name: "review-write", component: ReviewWriteView },
            { path: ":reviewId", name: "review-detail", component: ReviewDetailView },
            { path: ":reviewId/edit", name: "review-edit", component: ReviewEditView },
          ],
        },
      ],
    },
  ],
});

export default router;
