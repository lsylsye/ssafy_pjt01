<template>
  <main>
    <HeroSection>
      <JandiWidget 
        :count="reviewCount" 
        :nickname="userNickname"
        :levels="grassLevels"
        @more="onMoreJandi" 
      />
    </HeroSection>

    <BookScroller
      :books="home.bestsellers"
      :loading="home.loadingBestsellers"
      :error="home.bestsellersError"
      @more="onMoreBestsellers"
      @select="onSelectBestseller"
    />

    <TestBanner @start="onStartTasteTest" />

    <ReviewGrid :reviews="home.latestReviews" :loading="home.loadingReviews" @more="onMoreReviews" />
  </main>
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import HeroSection from "@/components/home/HeroSection.vue";
import JandiWidget from "@/components/home/JandiWidget.vue";
import BookScroller from "@/components/home/BookScroller.vue";
import TestBanner from "@/components/home/TestBanner.vue";
import ReviewGrid from "@/components/home/ReviewGrid.vue";

import { useHomeStore } from "@/stores/home";
import { useAlertStore } from "@/stores/alert";
import { useMypageStore } from "@/stores/mypage.store";
import { useAuthStore } from "@/stores/auth.store";

const home = useHomeStore();
const mypage = useMypageStore();
const auth = useAuthStore();
const alert = useAlertStore();
const router = useRouter();

const userNickname = computed(() => auth.me?.nickname || "작가");
const reviewCount = computed(() => 24); // 데코용 고정 수치
const grassLevels = computed(() => {
  // 디자인 요소로서 알록달록하게 랜덤 생성 (0~4)
  return Array.from({ length: 80 }, () => Math.floor(Math.random() * 5));
});

onMounted(async () => {
  home.fetchBestsellers();
  home.fetchLatestReviews();
  
  if (auth.access) {
    await mypage.fetchMe();
    // grass 데이터는 홈에서 더 이상 호출하지 않음 (데코용)
  }
});

function onMoreJandi() {
  router.push('/mylib');
}
function onMoreBestsellers() {
  router.push('/bestsellers');
}
function onSelectBestseller(b) {
  const isbn = b.isbn13 || b.id;
  if (isbn) {
    router.push(`/books/${isbn}`);
  }
}
function onStartTasteTest() {
  router.push('/taste/test');
}
function onMoreReviews() {
  router.push('/reviews');
}
</script>
