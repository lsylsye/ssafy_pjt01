<template>
  <div>
    <h1>{{ title }}</h1>
    <p>여기에 게시글 리스트가 들어옵니다</p>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const titleMap = {
  kr: '한국 커뮤니티',
  jp: '일본 커뮤니티',
  cn: '중화권 커뮤니티',
  en: '영미권 커뮤니티',
}

const title = computed(() => titleMap[route.params.country])
</script>


