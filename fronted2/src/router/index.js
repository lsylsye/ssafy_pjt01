// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { name: "home", path: "/", component: () => import("@/views/HomeView.vue") },
  { name: "search", path: "/search", component: () => import("@/views/SearchView.vue") },
  { name: "book-detail", path: "/books/:isbn13", component: () => import("@/views/BookDetailView.vue") },
  { name: "login", path: "/login", component: () => import("@/views/LoginView.vue") },
  { name: "signup", path: "/signup", component: () => import("@/views/SignupView.vue") },
  { name: "taste", path: "/taste", component: () => import("@/views/TasteView.vue") },
  { name: "taste-test", path: "/taste/test", component: () => import("@/views/TasteTestView.vue") },
  { name: "taste-result", path: "/taste/result", component: () => import("@/views/TasteResultView.vue") },
  { name: "community-write", path: "/community/free/write", component: () => import("@/views/CommunityWriteView.vue"), meta: { hideHeader: true } },
  { name: "community-detail", path: "/community/free/:id", component: () => import("@/views/CommunityDetailView.vue") },
  { name: "community", path: "/community", component: () => import("@/views/CommunityView.vue") },
  { name: "review-write", path: "/review/write", component: () => import("@/views/ReviewWriteView.vue") },
  { name: "review-detail", path: "/reviews/:id", component: () => import("@/views/ReviewDetailView.vue") },
  { name: "bestsellers", path: "/bestsellers", component: () => import("@/views/BestsellerListView.vue") },
  { name: "mylibrary", path: "/mylib", component: () => import("@/views/MyLibraryView.vue") },
  { name: "mypage", path: "/mypage", component: () => import("@/views/MyPageView.vue") },
  { name: "profile", path: "/profile/:id", component: () => import("@/views/MyPageView.vue") }, // MyPageView로 통일
  { name: "travel", path: "/travel", component: () => import("@/views/BookTravelView.vue") }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// 로그인 상태에 따른 접근 제어
router.beforeEach((to) => {
  const loggedIn = !!localStorage.getItem("access_token");

  // 로그인 상태에서 로그인/회원가입 접근 시 홈으로
  if (loggedIn && (to.name === "login" || to.name === "signup")) {
    return { name: "home" };
  }

  // 로그인이 필요한 페이지 접근 시 로그인으로 (단순 예시)
  const protectedRoutes = ["mylibrary", "mypage", "review-write"];
  if (!loggedIn && protectedRoutes.includes(to.name)) {
    return { name: "login" };
  }

  return true;
});

export default router;
