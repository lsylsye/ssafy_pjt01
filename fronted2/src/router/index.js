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
  { path: "/community", component: () => import("@/views/CommunityView.vue"),}
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
