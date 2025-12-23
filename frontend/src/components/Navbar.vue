<template>
  <nav class="navbar">
    <!-- 로고: 베스트셀러 메인 -->
    <router-link to="/" class="logo">
      잔디북
    </router-link>

    <!-- 메뉴 -->
    <ul class="menu">
      <!-- ✅ 로그인 전 -->
      <template v-if="!auth.isLoggedIn">
        <li>
          <router-link to="/signup">회원가입</router-link>
        </li>
        <li>
          <router-link to="/login">로그인</router-link>
        </li>
      </template>

      <!-- ✅ 로그인 후 -->
      <template v-else>
        <li>
          <router-link to="/mypage">마이페이지</router-link>
        </li>
        <li>
          <button class="logout-btn" @click="handleLogout">로그아웃</button>
        </li>
      </template>

      <li>
        <router-link to="/search">도서 검색</router-link>
      </li>

      <!-- 커뮤니티 드롭다운 -->
      <li class="dropdown">
        <span class="dropdown-title">커뮤니티</span>

        <ul class="dropdown-menu">
          <li><router-link to="/community/kr/free">한국</router-link></li>
          <li><router-link to="/community/jp/free">일본</router-link></li>
          <li><router-link to="/community/cn/free">중화권</router-link></li>
          <li><router-link to="/community/en/free">영미권</router-link></li>
        </ul>
      </li>
      <li>
        <router-link to="/survey">도서 취향 테스트</router-link>
      </li>
      <li>
        <router-link to="/library">근처 도서관 찾기</router-link>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useBookmarkStore } from '@/stores/bookmark'

const router = useRouter()
const auth = useAuthStore()
const bookmarkStore = useBookmarkStore()

const handleLogout = () => {
  auth.logout()

  // ✅ 로그인 사용자 전용 캐시 초기화
  bookmarkStore.isbnSet = new Set()
  bookmarkStore.synced = false

  router.push('/login')
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-primary);
  backdrop-filter: var(--blur-sm);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  text-decoration: none;
  color: var(--primary-color);
  transition: var(--transition);
  letter-spacing: -0.5px;
}

.logo:hover {
  color: var(--primary-dark);
  transform: scale(1.05);
}

.menu {
  display: flex;
  gap: 32px;
  list-style: none;
  margin: 0;
  padding: 0;
  align-items: center;
}

.menu a {
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 15px;
  transition: var(--transition);
  position: relative;
}

.menu a:hover {
  color: var(--primary-color);
}

.menu a::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary-color);
  transition: width 0.3s ease;
}

.menu a:hover::after {
  width: 100%;
}

.menu a.router-link-active {
  color: var(--primary-color);
  font-weight: 600;
}

.menu a.router-link-active::after {
  width: 100%;
}

/* ✅ 로그아웃 버튼 */
.logout-btn {
  border: none;
  background: none;
  padding: 0;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
  transition: var(--transition);
  position: relative;
}

.logout-btn:hover {
  color: var(--primary-color);
}

.logout-btn::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary-color);
  transition: width 0.3s ease;
}

.logout-btn:hover::after {
  width: 100%;
}

/* 드롭다운 */
.dropdown {
  position: relative;
  padding: 12px 0;
  margin: 0 -8px;
  padding-left: 8px;
  padding-right: 8px;
}

.dropdown-title {
  cursor: pointer;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 15px;
  transition: var(--transition);
  position: relative;
  display: inline-block;
}

.dropdown-title:hover {
  color: var(--primary-color);
}

.dropdown-title::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary-color);
  transition: width 0.3s ease;
}

.dropdown-title:hover::after {
  width: 100%;
}

/* 서브메뉴 */
.dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 8px 0;
  min-width: 140px;
  box-shadow: var(--shadow-lg);
  backdrop-filter: var(--blur-sm);
  animation: slideDown 0.3s ease;
  margin-top: 0;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-menu li {
  padding: 0;
}

.dropdown-menu li a {
  display: block;
  padding: 10px 16px;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 14px;
  border-radius: 8px;
  margin: 0 4px;
  position: relative;
}

.dropdown-menu li a::after {
  display: none;
}

/* 호버 시 서브메뉴 표시 */
.dropdown:hover .dropdown-menu {
  display: block;
}

/* ✅ 호버 효과 */
.dropdown-menu li:hover a {
  color: var(--primary-color);
  background-color: var(--primary-lighter);
}
</style>
