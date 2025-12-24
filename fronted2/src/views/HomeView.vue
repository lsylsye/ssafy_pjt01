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

    <ReviewGrid :reviews="dummyReviews" @more="onMoreReviews" />
  </main>
</template>

<script setup>
import { onMounted } from "vue";
import HeroSection from "@/components/home/HeroSection.vue";
import JandiWidget from "@/components/home/JandiWidget.vue";
import BookScroller from "@/components/home/BookScroller.vue";
import TestBanner from "@/components/home/TestBanner.vue";
import ReviewGrid from "@/components/home/ReviewGrid.vue";

import { useHomeStore } from "@/stores/home";
import { useAlertStore } from "@/stores/alert";

const home = useHomeStore();
const alert = useAlertStore();

const dummyReviews = [
  { id: 1, user: "개발자L", time: "2시간 전", bookTitle: "클린 코드", content: "코드를 작성하는 태도를 다시 생각하게 해주는 책. 개발자라면 꼭 한 번은!" },
  { id: 2, user: "책벌레", time: "5시간 전", bookTitle: "물고기는 존재하지 않는다", content: "과학과 에세이가 절묘하게 섞인 명작. 생각보다 더 충격적이었어요." },
  { id: 3, user: "잔디콜렉터", time: "1일 전", bookTitle: "사피엔스", content: "두껍지만 술술 읽힘. 인류의 역사를 통찰력 있게 풀어내서 좋았어요." },
];

onMounted(() => {
  home.fetchBestsellers();
});

function onMoreJandi() {
  alert.open({ type: "info", title: "잔디 위젯", message: "잔디 위젯 API 연결은 나중에 붙일게요." });
}
function onMoreBestsellers() {
  alert.open({ type: "info", title: "베스트셀러", message: "더보기 페이지 라우트 연결하면 돼요." });
}
function onSelectBestseller(b) {
  alert.open({ type: "success", title: "책 선택", message: `${b.title} (${b.author})` });
}
function onStartTasteTest() {
  alert.open({ type: "info", title: "취향 분석", message: "취향 테스트 페이지 라우트 연결하면 돼요." });
}
function onMoreReviews() {
  alert.open({ type: "info", title: "전체 리뷰", message: "전체 리뷰 페이지 라우트 연결하면 돼요." });
}
</script>
