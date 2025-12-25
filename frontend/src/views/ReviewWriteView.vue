<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { searchBooks } from '@/api/books.api';
import { createReview } from '@/api/review';
import { useUiStore } from '@/stores/ui.store';
import { useAuthStore } from '@/stores/auth.store';
import { Search, Star, ArrowLeft, Check, X } from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();
const uiStore = useUiStore();

const searchQuery = ref('');
const searchResults = ref([]);
const selectedBook = ref(null);
const rating = ref(0);
const content = ref('');
const isSearching = ref(false);

const handleSearch = async () => {
    if (!searchQuery.value.trim()) {
        searchResults.value = [];
        return;
    }
    isSearching.value = true;
    try {
        const res = await searchBooks(searchQuery.value);
        // 백엔드 응답 구조에 맞게 수정: items 필드 확인
        const data = res.data?.items || res.data || [];
        // isbn13이 있는 유효한 도서만 필터링
        searchResults.value = Array.isArray(data) ? data.filter(b => b.isbn13) : [];
    } catch (e) {
        console.error(e);
    } finally {
        isSearching.value = false;
    }
};

// 디바운스 처리 (간단히 watch로)
let timeoutId = null;
watch(searchQuery, (newVal) => {
    if (timeoutId) clearTimeout(timeoutId);
    if (!newVal.trim()) {
        searchResults.value = [];
        return;
    }
    timeoutId = setTimeout(() => {
        handleSearch();
    }, 500);
});

const selectBook = (book) => {
    selectedBook.value = book;
    searchQuery.value = '';
    searchResults.value = [];
};

const setRating = (val) => {
    rating.value = val;
};

const submitReview = async () => {
    if (!selectedBook.value) {
        uiStore.alert('기록할 책을 선택해주세요.');
        return;
    }
    if (rating.value === 0) {
        uiStore.alert('별점을 선택해주세요.');
        return;
    }
    if (!content.value.trim()) {
        uiStore.alert('내용을 입력해주세요.');
        return;
    }

    try {
        const payload = {
            book_title: selectedBook.value.title,
            book_author: selectedBook.value.author,
            content: content.value,
            rating: rating.value,
            isbn13: selectedBook.value.isbn13,
            publisher: selectedBook.value.publisher,
            pub_date: selectedBook.value.pub_date,
            cover: selectedBook.value.cover
        };
        await createReview(payload);
        uiStore.addToast({ message: '기록이 성공적으로 심어졌습니다! 🌱', variant: 'success' });
        
        // 이전 페이지로 돌아가기
        router.back();
    } catch (e) {
        console.error(e);
        if (e.response?.status === 401) {
            const authStore = useAuthStore();
            authStore.logout();
            uiStore.alert('세션이 만료되었습니다. 다시 로그인해주세요.');
            router.push('/login');
        } else {
            uiStore.alert('기록 저장 중 오류가 발생했습니다.');
        }
    }
};

const goBack = () => {
    router.back();
};

onMounted(() => {
    const { isbn13, title, author, publisher, cover, pub_date } = route.query;
    if (isbn13 && title) {
        selectedBook.value = {
            isbn13,
            title,
            author: author || '-',
            publisher: publisher || '-',
            cover: cover || '',
            pub_date: pub_date || ''
        };
    }
});
</script>

<template>
  <div class="review-page">
    <button class="back-btn" @click="goBack">
      <ArrowLeft :size="20" /> 뒤로가기
    </button>

    <div class="glass-panel">
      <button class="close-panel-btn" @click="goBack" aria-label="Close">
        <X :size="24" />
      </button>
      <h2 class="page-title">어떤 책을 심으시겠어요? 🌱</h2>

      <!-- 1. 책 검색 영역 -->
      <div v-if="!selectedBook" class="search-box">
        <Search class="search-icon" :size="20" />
        <input
          v-model="searchQuery"
          type="text"
          class="input-field"
          placeholder="책 제목이나 작가를 검색하세요"
        />
        
        <!-- 검색 결과 레이어 -->
        <div v-if="searchResults.length > 0" class="search-dropdown">
            <div 
                v-for="book in searchResults" 
                :key="book.isbn13" 
                class="search-item"
                @click="selectBook(book)"
            >
                <img :src="book.cover" class="mini-cover" v-if="book.cover" />
                <div class="book-info">
                    <div class="book-title">{{ book.title }}</div>
                    <div class="book-author">{{ book.author }}</div>
                </div>
            </div>
        </div>
        <div v-else-if="searchQuery && !isSearching" class="no-result">
            검색 결과가 없습니다.
        </div>
      </div>

      <!-- 2. 선택된 책 카드 -->
      <div v-else class="selected-book">
        <img :src="selectedBook.cover" class="selected-cover" />
        <div class="selected-info">
          <h4 class="selected-title">{{ selectedBook.title }}</h4>
          <p class="selected-author">{{ selectedBook.author }}</p>
          <span class="selected-tag"><Check :size="14" /> 선택됨</span>
        </div>
        <button class="change-btn" @click="selectedBook = null">변경</button>
      </div>

      <!-- 3. 별점 입력 -->
      <div class="star-rating">
        <Star 
            v-for="i in 5" 
            :key="i"
            :size="36"
            :class="{ active: i <= rating }"
            :fill="i <= rating ? '#ffd700' : 'none'"
            @click="setRating(i)"
            class="star-icon"
        />
      </div>

      <!-- 4. 내용 입력 -->
      <textarea
        v-model="content"
        class="review-textarea"
        placeholder="이 책을 읽으며 어떤 생각이 들었나요? 자유롭게 기록을 남겨보세요."
      ></textarea>

      <!-- 5. 제출 버튼 -->
      <button class="btn-submit" @click="submitReview">
        기록 완료하고 잔디 심기
      </button>
    </div>
  </div>
</template>

<style scoped>
.review-page {
    /* background: #f2f4f6; */
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
    font-family: "Pretendard", -apple-system, sans-serif;
}

.back-btn {
    position: fixed;
    top: 24px;
    left: 24px;
    background: none;
    border: none;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 1rem;
    font-weight: 600;
    color: #4e5968;
    cursor: pointer;
    transition: 0.2s;
    z-index: 10;
}
.back-btn:hover {
    color: #191f28;
}

.glass-panel {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(20px);
    border-radius: 32px;
    padding: 48px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.08);
    width: 100%;
    max-width: 600px;
    margin-top: 40px;
    border: 1px solid rgba(255, 255, 255, 0.5);
}

.page-title {
    text-align: center;
    margin-bottom: 32px;
    font-size: 1.8rem;
    font-weight: 800;
    color: #191f28;
}

.close-panel-btn {
    position: absolute;
    top: 24px;
    right: 24px;
    background: none;
    border: none;
    color: #8b95a1;
    cursor: pointer;
    transition: 0.2s;
    padding: 8px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.close-panel-btn:hover {
    background: #f2f4f6;
    color: #191f28;
}

.search-box {
    position: relative;
    margin-bottom: 32px;
}
.input-field {
    width: 100%;
    padding: 18px 20px 18px 54px;
    border: 1px solid rgba(0,0,0,0.05);
    border-radius: 20px;
    background: #fff;
    font-size: 1.05rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    transition: 0.3s;
}
.input-field:focus {
    outline: none;
    border-color: #00D15B;
    box-shadow: 0 0 0 4px rgba(0, 209, 91, 0.1);
}
.search-icon {
    position: absolute;
    left: 20px;
    top: 18px;
    color: #8b95a1;
}

.search-dropdown {
    position: absolute;
    top: 64px;
    left: 0;
    right: 0;
    background: #fff;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    max-height: 400px;
    overflow-y: auto;
    z-index: 20;
    padding: 8px;
    border: 1px solid #efefef;
}
.search-item {
    display: flex;
    gap: 12px;
    padding: 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.2s;
}
.search-item:hover {
    background: #f2f4f6;
}
.mini-cover {
    width: 48px;
    height: 68px;
    object-fit: cover;
    border-radius: 4px;
}
.book-title {
    font-weight: 700;
    color: #191f28;
    font-size: 1rem;
    margin-bottom: 4px;
}
.book-author {
    color: #8b95a1;
    font-size: 0.85rem;
}

/* 선택물 카드 */
.selected-book {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 24px;
    background: #ffffff;
    border-radius: 24px;
    border: 2px solid #00D15B;
    margin-bottom: 32px;
    position: relative;
}
.selected-cover {
    width: 70px;
    height: 100px;
    border-radius: 8px;
    object-fit: cover;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.selected-info {
    flex: 1;
}
.selected-title {
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 6px 0;
}
.selected-author {
    color: #6b7684;
    font-size: 0.9rem;
    margin-bottom: 12px;
}
.selected-tag {
    font-size: 0.8rem;
    color: #00D15B;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 4px;
}
.change-btn {
    position: absolute;
    top: 12px;
    right: 12px;
    background: #f2f4f6;
    border: none;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 0.8rem;
    color: #4e5968;
    cursor: pointer;
}

/* 별점 */
.star-rating {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 32px;
}
.star-icon {
    cursor: pointer;
    transition: 0.2s;
    color: #ddd;
}
.star-icon.active {
    color: #ffd700;
}
.star-icon:hover {
    transform: scale(1.1);
}

.review-textarea {
    width: 100%;
    height: 180px;
    padding: 24px;
    border-radius: 20px;
    border: none;
    background: #f9fafb;
    font-size: 1.05rem;
    resize: none;
    margin-bottom: 32px;
    transition: 0.3s;
    font-family: inherit;
    line-height: 1.6;
}
.review-textarea:focus {
    outline: none;
    background: white;
    box-shadow: inset 0 0 0 2px #00D15B;
}

.btn-submit {
    width: 100%;
    padding: 20px;
    background: #00D15B;
    color: white;
    border: none;
    border-radius: 20px;
    font-size: 1.15rem;
    font-weight: 800;
    cursor: pointer;
    transition: 0.3s;
    box-shadow: 0 8px 24px rgba(0, 209, 91, 0.25);
}
.btn-submit:hover {
    background: #00b54f;
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(0, 209, 91, 0.3);
}
.no-result {
    padding: 20px;
    text-align: center;
    color: #8b95a1;
}
</style>
