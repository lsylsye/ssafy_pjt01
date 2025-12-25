<script setup>
import { ref, onMounted, computed, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { getBookTravelInfo, getSupportedCountries } from "@/api/ai";
import { useRouter } from "vue-router";

const router = useRouter();

// 1. 데이터 준비
const countries = [
  { name: "일본", flag: "🇯🇵", lat: 36.2048, lng: 138.2529 },
  { name: "베트남", flag: "🇻🇳", lat: 14.0583, lng: 108.2772 },
  { name: "중국", flag: "🇨🇳", lat: 35.8617, lng: 104.1954 },
  { name: "필리핀", flag: "🇵🇭", lat: 12.8797, lng: 121.774 },
  { name: "미국", flag: "🇺🇸", lat: 37.0902, lng: -95.7129 },
  { name: "대만", flag: "🇹🇼", lat: 23.6978, lng: 120.9605 },
  { name: "홍콩", flag: "🇭🇰", lat: 22.3193, lng: 114.1694 },
  { name: "몽골", flag: "🇲🇳", lat: 46.8625, lng: 103.8467 },
  { name: "호주", flag: "🇦🇺", lat: -25.2744, lng: 133.7751 },
  { name: "캐나다", flag: "🇨🇦", lat: 56.1304, lng: -106.3468 },
  { name: "터키", flag: "🇹🇷", lat: 38.9637, lng: 35.2433 },
  { name: "영국", flag: "🇬🇧", lat: 55.3781, lng: -3.436 },
  { name: "프랑스", flag: "🇫🇷", lat: 46.2276, lng: 2.2137 },
  { name: "이탈리아", flag: "🇮🇹", lat: 41.8719, lng: 12.5674 },
  { name: "스페인", flag: "🇪🇸", lat: 40.4637, lng: -3.7492 },
  { name: "독일", flag: "🇩🇪", lat: 51.1657, lng: 10.4515 },
  { name: "스위스", flag: "🇨🇭", lat: 46.8182, lng: 8.2275 },
  { name: "네덜란드", flag: "🇳🇱", lat: 52.1326, lng: 5.2913 },
  { name: "체코", flag: "🇨🇿", lat: 49.8175, lng: 15.473 },
  { name: "오스트리아", flag: "🇦🇹", lat: 47.5162, lng: 14.5501 },
];

const searchQuery = ref("");
const isDropdownActive = ref(false);
const showInfoSection = ref(false);
const isLoading = ref(false);
const selectedCountryName = ref("");

const isListLoading = ref(true);
const supportedCountryNames = ref([]);

const filteredCountries = computed(() => {
  // 백엔드 지원 목록이 아직 로딩 중이라면 빈 배열
  if (isListLoading.value) return [];
  
  // 1. 백엔드 지원 국가만 필터링 (NFC 정규화 및 트림 적용하여 매칭 확률 극대화)
  const baseList = countries.filter(c => {
    const normalizedName = c.name.trim().normalize("NFC");
    return supportedCountryNames.value.some(sn => 
      typeof sn === 'string' && sn.trim().normalize("NFC") === normalizedName
    );
  });
  
  // 2. 검색어 필터링 (트림 및 정규화 적용)
  const query = searchQuery.value.trim().normalize("NFC");
  if (!query) return baseList;
  
  return baseList.filter((c) => 
    c.name.normalize("NFC").includes(query)
  );
});

const resultData = ref({
  country: "",
  flag: "",
  literary_guide: "",
  author: {
    name: "",
    description: "",
    image: "",
    wiki_url: "",
  },
  books: [],
});

let map = null;
let currentMarker = null;

onMounted(async () => {
  initMap();
  await fetchSupportedCountries();
});

async function fetchSupportedCountries() {
  isListLoading.value = true;
  try {
    const res = await getSupportedCountries();
    supportedCountryNames.value = res.data.countries;
  } catch (err) {
    console.error("Failed to fetch supported countries", err);
  } finally {
    isListLoading.value = false;
  }
}

function initMap() {
  map = L.map("map", {
    center: [20, 0],
    zoom: 2,
    zoomControl: false,
    scrollWheelZoom: false,
  });

  L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: "abcd",
      maxZoom: 19,
    }
  ).addTo(map);
}

const pinIcon = L.divIcon({
  className: "custom-pin-marker",
  html: `<div class="custom-pin"></div>`,
  iconSize: [40, 40],
  iconAnchor: [20, 40],
});

async function selectCountry(country) {
  searchQuery.value = country.name;
  isDropdownActive.value = false;

  // 지도 이동
  map.flyTo([country.lat, country.lng], 5, {
    duration: 1.5,
  });

  if (currentMarker) map.removeLayer(currentMarker);

  setTimeout(() => {
    currentMarker = L.marker([country.lat, country.lng], {
      icon: pinIcon,
    }).addTo(map);
  }, 1000);

  // API 호출
  fetchData(country);
}

async function fetchData(country) {
  selectedCountryName.value = country.name;
  isLoading.value = true;
  try {
    const res = await getBookTravelInfo(country.name);
    resultData.value = {
      ...res.data,
      flag: country.flag,
    };
    showInfoSection.value = true;

    // 부드럽게 스크롤 이동
    setTimeout(() => {
      const el = document.getElementById("infoSection");
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, 500);
  } catch (err) {
    console.error("Failed to fetch book travel info", err);
    alert("도서 정보를 가져오는데 실패했습니다.");
  } finally {
    isLoading.value = false;
  }
}

function handleFocus() {
  isDropdownActive.value = true;
}

function handleClickOutside(e) {
  if (!e.target.closest(".search-container")) {
    isDropdownActive.value = false;
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

function goToDetail(isbn) {
  if (isbn) {
    router.push(`/books/${isbn}`);
  }
}
</script>

<template>
  <div class="book-travel-page">
    <!-- 1. 헤더 (카피라이팅 + 검색) -->
    <div class="hero-wrap">
      <h1 class="main-copy">"책 한 권으로 국경을 넘어보세요."</h1>
      <p class="sub-copy">
        직접 가지 않아도, 그 나라의 문화와 영혼을 가장 깊이 만날 수 있습니다.<br />
        오늘, 당신의
        <span class="highlight">마음속 숲은 어디로 떠나고 싶나요?</span> ✈️
      </p>

      <!-- 커스텀 검색창 -->
      <div class="search-container">
        <div class="search-box">
          <span style="font-size: 1.2rem; margin-right: 10px">🌍</span>
          <input
            type="text"
            class="search-input"
            v-model="searchQuery"
            @focus="handleFocus"
            placeholder="떠나고 싶은 나라를 검색하세요 (예: 영국, 일본)"
            autocomplete="off"
          />
          <button class="search-btn">➔</button>
        </div>

        <ul class="dropdown-list" :class="{ active: isDropdownActive }">
          <li v-if="isListLoading" class="no-result">
            데이터를 불러오는 중입니다... 🌍
          </li>
          <template v-else>
            <li
              v-for="c in filteredCountries"
              :key="c.name"
              class="country-item"
              @click="selectCountry(c)"
            >
              <span class="flag-icon">{{ c.flag }}</span> {{ c.name }}
            </li>
            <li v-if="filteredCountries.length === 0" class="no-result">
              검색 결과가 없어요 🍂
            </li>
          </template>
        </ul>
      </div>
    </div>

    <!-- 2. 지도 영역 -->
    <div class="map-wrapper">
      <div id="map"></div>

      <!-- 로딩 표시 (지도 위에 오버레이) -->
      <div v-if="isLoading" class="map-loading-overlay">
        <div class="glass-loader">
          <div class="loader"></div>
          <p class="loading-text">
            <span class="country-highlight">{{ selectedCountryName }}</span>를
            선택하셨군요!<br />같이 떠나볼까요? ✈️
          </p>
        </div>
      </div>
    </div>

    <!-- 3. 상세 정보 (선택 시 등장) -->
    <div
      class="info-container"
      id="infoSection"
      :class="{ show: showInfoSection }"
    >
      <div class="country-title">
        <span class="c-flag">{{ resultData.flag }}</span>
        <div class="c-name">{{ resultData.country }}</div>
      </div>

      <div class="content-grid">
        <!-- AI 분석 -->
        <div class="glass-card">
          <div class="ai-badge">✨ AI 문학 가이드</div>
          <div class="ai-desc">
            {{ resultData.literary_guide }}
          </div>
        </div>

        <!-- 대표 작가 -->
        <div class="glass-card author-box">
          <img
            v-if="resultData.author.image"
            :src="resultData.author.image"
            class="author-img"
            :alt="resultData.author.name"
          />
          <div v-else class="author-img-placeholder">👤</div>
          <h3 style="margin-bottom: 4px">{{ resultData.author.name }}</h3>
          <p style="font-size: 0.9rem; color: #666">
            {{ resultData.author.description }}
          </p>
          <a
            v-if="resultData.author.wiki_url"
            :href="resultData.author.wiki_url"
            target="_blank"
            class="wiki-link"
            >위키백과 보기</a
          >
        </div>
      </div>

      <!-- 베스트셀러 -->
      <div class="book-list-wrap">
        <div class="list-title">📚 이 나라의 베스트셀러</div>
        <div class="scroll-view">
          <div
            v-for="book in resultData.books"
            :key="book.isbn13"
            class="book-item"
            @click="goToDetail(book.isbn13)"
          >
            <img
              v-if="book.cover"
              :src="book.cover"
              class="book-cover"
              :alt="book.title"
            />
            <div v-else class="book-cover-placeholder">📖</div>
            <div class="book-t">{{ book.title }}</div>
            <div class="book-a">{{ book.author }} / {{ book.publisher }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --primary: #00d15b;
  --primary-dark: #00a84d;
  --text-main: #191f28;
  --text-sub: #6b7684;
  --bg: #f5f7fa;
}

.book-travel-page {
  background-color: #f5f7fa;
  color: #191f28;
  width: 100%;
  min-height: 100vh;
}

ul {
  list-style: none;
}

/* --- 1. 히어로 & 검색 섹션 --- */
.hero-wrap {
  position: relative;
  padding: 60px 20px 40px;
  text-align: center;
  background: linear-gradient(180deg, #ffffff 0%, #f5f7fa 100%);
}

.main-copy {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 12px;
  line-height: 1.3;
}
.sub-copy {
  font-size: 1.1rem;
  color: #6b7684;
  line-height: 1.6;
  margin-bottom: 40px;
}
.highlight {
  color: #00d15b;
}

/* 커스텀 검색 셀렉트 박스 */
.search-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  z-index: 1000;
}

.search-box {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 50px;
  padding: 8px 8px 8px 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: 0.3s;
}
.search-box:focus-within {
  box-shadow: 0 10px 40px rgba(0, 209, 91, 0.15);
  border-color: #00d15b;
}

.search-input {
  flex: 1;
  border: none;
  font-size: 1.1rem;
  outline: none;
  color: #333;
  font-weight: 500;
}
.search-input::placeholder {
  color: #ccc;
}

.search-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #00d15b;
  color: white;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.2s;
  flex-shrink: 0;
}
.search-btn:hover {
  transform: scale(1.05);
  background: #00a84d;
}

/* 드롭다운 리스트 */
.dropdown-list {
  position: absolute;
  top: 70px;
  left: 0;
  width: 100%;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  max-height: 300px;
  overflow-y: auto;
  display: none;
  padding: 10px;
  border: 1px solid #eee;
}
.dropdown-list.active {
  display: block;
  animation: slideDown 0.2s ease-out;
}

.country-item {
  padding: 12px 20px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: 0.1s;
  font-size: 1rem;
  color: #333;
}
.country-item:hover {
  background: #f2f4f6;
  color: #00d15b;
  font-weight: 700;
}
.no-result {
  padding: 10px;
  color: #888;
  text-align: center;
}
.flag-icon {
  font-size: 1.4rem;
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

/* --- 2. 지도 섹션 --- */
.map-wrapper {
  position: relative;
  width: 100%;
  height: 500px;
  margin-bottom: 60px;
  mask-image: linear-gradient(
    to bottom,
    transparent 0%,
    black 10%,
    black 90%,
    transparent 100%
  );
}
#map {
  width: 100%;
  height: 100%;
  background: #f5f7fa;
}

:deep(.custom-pin) {
  width: 40px;
  height: 40px;
  background: #00d15b;
  border: 3px solid white;
  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pinDrop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
:deep(.custom-pin::after) {
  content: "";
  width: 14px;
  height: 14px;
  background: white;
  border-radius: 50%;
}

@keyframes pinDrop {
  0% {
    transform: translateY(-50px) rotate(-45deg);
    opacity: 0;
  }
  100% {
    transform: translateY(0) rotate(-45deg);
    opacity: 1;
  }
}

/* --- 3. 결과 정보 섹션 --- */
.info-container {
  max-width: 1100px;
  margin: 0 auto 100px;
  padding: 0 20px;
  display: none;
  opacity: 0;
  transform: translateY(20px);
  transition: 0.5s;
}
.info-container.show {
  display: block;
  opacity: 1;
  transform: translateY(0);
}

.country-title {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
}
.c-flag {
  font-size: 3.5rem;
}
.c-name {
  font-size: 2.5rem;
  font-weight: 800;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

/* 글래스 카드 */
.glass-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 30px;
  border: 1px solid white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
}

.ai-badge {
  background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
  color: #5e35b1;
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.9rem;
  display: inline-block;
  margin-bottom: 15px;
}
.ai-desc {
  font-size: 1.15rem;
  line-height: 1.8;
  color: #333;
}

/* 작가 카드 */
.author-box {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.author-img,
.author-img-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
}

.wiki-link {
  margin-top: 10px;
  font-size: 0.85rem;
  color: #00d15b;
  text-decoration: none;
  font-weight: 600;
}
.wiki-link:hover {
  text-decoration: underline;
}

/* 책 리스트 가로 스크롤 */
.book-list-wrap {
  margin-top: 50px;
}
.list-title {
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 25px;
}
.scroll-view {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  padding-bottom: 25px;
}
.scroll-view::-webkit-scrollbar {
  height: 8px;
}
.scroll-view::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}
.scroll-view::-webkit-scrollbar-thumb {
  background: #00d15b;
  border-radius: 10px;
}

.book-item {
  min-width: 180px;
  max-width: 180px;
  cursor: pointer;
  transition: 0.3s;
}
.book-item:hover {
  transform: translateY(-8px);
}
.book-cover,
.book-cover-placeholder {
  width: 100%;
  height: 260px;
  border-radius: 14px;
  background: #eee;
  margin-bottom: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  object-fit: cover;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
}

.book-t {
  font-weight: 700;
  font-size: 1.05rem;
  margin-bottom: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.book-a {
  font-size: 0.85rem;
  color: #888;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 로딩 오버레이 */
.map-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1001;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(4px);
}
.glass-loader {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(15px);
  padding: 40px 60px;
  border-radius: 30px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  border: 1px solid white;
}
.loading-text {
  font-size: 1rem;
  font-weight: 500;
  color: #191f28;
  text-align: center;
  line-height: 1.5;
}
.country-highlight {
  color: #00d15b;
}
.loader {
  width: 54px;
  height: 54px;
  border: 5px solid #00d15b;
  border-bottom-color: transparent;
  border-radius: 50%;
  display: inline-block;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
