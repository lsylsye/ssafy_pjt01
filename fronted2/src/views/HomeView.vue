<template>
  <main>
    <HeroSection>
      <JandiWidget @more="onMoreJandi" />
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
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import HeroSection from "@/components/home/HeroSection.vue";
import JandiWidget from "@/components/home/JandiWidget.vue";
import BookScroller from "@/components/home/BookScroller.vue";
import TestBanner from "@/components/home/TestBanner.vue";
import ReviewGrid from "@/components/home/ReviewGrid.vue";

import { useHomeStore } from "@/stores/home";
import { useAlertStore } from "@/stores/alert";

const home = useHomeStore();
const alert = useAlertStore();
const router = useRouter();

onMounted(() => {
  home.fetchBestsellers();
  home.fetchLatestReviews();
});

function onMoreJandi() {
  alert.open({ type: "info", title: "잔디 위젯", message: "잔디 위젯 API 연결은 나중에 붙일게요." });
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
