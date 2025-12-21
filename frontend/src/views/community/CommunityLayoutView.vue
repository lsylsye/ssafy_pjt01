<template>
  <section class="community">
    <h1 class="title">{{ pageTitle }}</h1>

    <!-- 게시판 탭 -->
    <nav class="board-tabs">
      <router-link
        :to="`/community/${country}/free`"
        exact-active-class="tab-active"
      >
        자유게시판
      </router-link>

      <router-link
        :to="`/community/${country}/review`"
        exact-active-class="tab-active"
      >
        리뷰게시판
      </router-link>
    </nav>

    <router-view />
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const country = computed(() => String(route.params.country || 'kr'))

const titleMap = {
  kr: '한국 커뮤니티',
  jp: '일본 커뮤니티',
  cn: '중화권 커뮤니티',
  en: '영미권 커뮤니티',
}
const pageTitle = computed(() => titleMap[country.value] || '커뮤니티')
</script>

<style scoped>
.community { padding: 24px; }
.title { margin: 0 0 12px; }

.country-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 14px;
}
.country-tabs a {
  text-decoration: none;
  color: #444;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.country-tabs a.active {
  font-weight: bold;
  border-color: #1a73e8;
  color: #1a73e8;
}

.board-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}
.board-tabs a {
  text-decoration: none;
  color: #333;
  padding: 8px 14px;
  border: 1px solid #ddd;
  border-radius: 10px;
}
.board-tabs a.tab-active {
  border-color: #1a73e8;
  color: #1a73e8;
  font-weight: bold;
}
</style>
