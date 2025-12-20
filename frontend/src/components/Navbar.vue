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
          <li><router-link to="/community/kr">한국</router-link></li>
          <li><router-link to="/community/jp">일본</router-link></li>
          <li><router-link to="/community/cn">중화권</router-link></li>
          <li><router-link to="/community/en">영미권</router-link></li>
        </ul>
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
  padding: 14px 24px;
  border-bottom: 1px solid #e0e0e0;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  text-decoration: none;
  color: #2c2c2c;
}

.menu {
  display: flex;
  gap: 18px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu a {
  text-decoration: none;
  color: #444;
}

.menu a.router-link-active {
  font-weight: bold;
}

/* ✅ 로그아웃 버튼(링크처럼 보이게) */
.logout-btn {
  border: none;
  background: none;
  padding: 0;
  color: #444;
  cursor: pointer;
  font-size: 16px;
}

.logout-btn:hover {
  color: #1a73e8;
}

/* 드롭다운 */
.dropdown {
  position: relative;
}

.dropdown-title {
  cursor: pointer;
}

/* 서브메뉴 */
.dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid #ddd;
  padding: 8px 0;
  min-width: 120px;
}

.dropdown-menu li {
  padding: 8px 16px;
}

.dropdown-menu li a {
  display: block;
  color: #333;
}

/* 호버 시 서브메뉴 표시 */
.dropdown:hover .dropdown-menu {
  display: block;
}

/* ✅ 호버 효과 */
.dropdown-menu li:hover {
  background-color: #f5f7fa;
}

.dropdown-menu li:hover a {
  color: #1a73e8;
}
</style>
