// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", component: () => import("@/views/HomeView.vue") },
  { path: "/search", component: () => import("@/views/SearchView.vue") },
  { path: "/books/:isbn13", component: () => import("@/views/BookDetailView.vue") },
  { path: "/login", component: () => import("@/views/LoginView.vue") },
  { path: "/signup", component: () => import("@/views/SignupView.vue") },
  { path: "/taste", component: () => import("@/views/TasteView.vue") },
  { path: "/taste/test", component: () => import("@/views/TasteTestView.vue") },
  { path: "/taste/result", component: () => import("@/views/TasteResultView.vue") },
  { path: "/community/free/write", component: () => import("@/views/CommunityWriteView.vue"), meta: { hideHeader: true } },
  { path: "/community/free/:id", component: () => import("@/views/CommunityDetailView.vue") },
  { path: "/community", component: () => import("@/views/CommunityView.vue"), },
  { path: "/review/write", component: () => import("@/views/ReviewWriteView.vue") },
  { path: "/bestsellers", component: () => import("@/views/BestsellerListView.vue") },
  // { path: "/reviews", component: () => import("@/views/AllReviewsView.vue") },  // 제거됨
  { path: "/mylib", component: () => import("@/views/MyLibraryView.vue") },
  { path: "/mypage", component: () => import("@/views/MyPageView.vue") },
  { path: "/profile/:id", component: () => import("@/views/MyPageView.vue") },  // 다른 사용자 프로필
  { path: "/travel", component: () => import("@/views/BookTravelView.vue") }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 로그인 상태에 따른 접근 제어
router.beforeEach((to) => {
  const loggedIn = !!localStorage.getItem("access_token");

  if (loggedIn && (to.path === "/login" || to.path === "/signup")) {
    return { path: "/" };
  }
  return true;
});

export default router;
