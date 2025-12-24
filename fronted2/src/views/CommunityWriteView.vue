<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { createPost } from '@/api/community';
import { FREE_PREFIXES } from '@/constants/freePrefixes';

const router = useRouter();

const categories = ref(FREE_PREFIXES);
const category = ref(null); // Selected prefix value (string)
const title = ref('');
const content = ref('');

const submit = async () => {
  if (!title.value.trim()) {
    alert('제목을 입력해주세요.');
    return;
  }
  if (!content.value.trim()) {
    alert('내용을 입력해주세요.');
    return;
  }
  if (!category.value) {
     alert('카테고리를 선택해주세요.');
     return;
  }

  try {
    // 백엔드가 문자열(value)을 받는지 ID를 받는지에 따라 이름이 다를 수 있음
    // 일단 사용자가 요청한 CONST 상수는 value(String) 형식이므로
    // prefix 필드에 해당 문자열을 담아 보냅니다.
    const payload = {
        title: title.value,
        content: content.value,
        prefix: category.value 
    };
    
    await createPost(payload);
    alert('글이 등록되었습니다!');
    router.push('/community');
  } catch (err) {
    console.error(err);
    alert('글 작성에 실패했습니다.');
  }
};

onMounted(() => {
  // 기본 선택 (첫 번째 요소)
  if (categories.value && categories.value.length > 0) {
    category.value = categories.value[0].value;
  }
});
</script>

<template>
  <div class="write-page">
    <!-- 상단 바 -->
    <header class="header">
        <button class="btn-close" @click="router.back()">✕ 닫기</button>
        <button class="btn-submit" @click="submit">발행하기</button>
    </header>

    <div class="container">
        <!-- 카테고리 칩 -->
        <span class="category-label">어떤 이야기를 심으시나요?</span>
        <div class="category-group">
            <template v-for="cat in categories" :key="cat.value">
                <input 
                    type="radio" 
                    name="cat" 
                    :id="`c-${cat.value}`" 
                    :value="cat.value" 
                    v-model="category" 
                />
                <label :for="`c-${cat.value}`" class="chip">
                    {{ cat.icon }} {{ cat.value }}
                </label>
            </template>
        </div>

        <!-- 제목 -->
        <input
            type="text"
            class="input-title"
            placeholder="제목을 입력하세요"
            v-model="title"
        />

        <!-- 구분선 -->
        <div class="divider"></div>

        <!-- 본문 -->
        <textarea
            class="input-content"
            placeholder="오늘 당신의 마음에 심고 싶은 이야기는 무엇인가요?&#13;&#10;자유롭게 기록해보세요."
            v-model="content"
        ></textarea>

        <!-- 헬퍼 텍스트 -->
        <div class="helper-text">
            💡 <strong>작성 팁</strong><br />
            • 굵기 조절이나 사진 첨부는 지원하지 않아요. 오직 '글'에만
            집중해보세요.<br />
            • 타인에게 불쾌감을 주는 언어 사용 시, 싹이 트지 못하고 삭제될
            수 있어요.
        </div>
    </div>
  </div>
</template>

<style scoped>
/* :root 변수는 scoped에서 동작하지 않을 수 있으므로 직접 값 사용하거나 global.css에 있어야 함. 
   여기서는 변수 대신 직접 값을 사용하거나 var 사용하되 fallback 고려 
*/
.write-page {
    --primary: #00d15b;
    --text: #191f28;
    --placeholder: #c0c5c9;
    
    font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: white;
    color: var(--text);
    min-height: 100vh;
}

/* 상단 네비게이션 */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    border-bottom: 1px solid #f5f5f5;
    position: sticky;
    top: 0;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    z-index: 10;
}
.btn-close {
    border: none;
    background: none;
    font-size: 1.1rem;
    color: #888;
    cursor: pointer;
    font-weight: 500;
}
.btn-submit {
    background: var(--primary);
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 24px;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    transition: 0.2s;
}
.btn-submit:hover {
    transform: scale(1.05);
    background: #00b54f;
}

/* 메인 컨테이너 */
.container {
    max-width: 720px;
    margin: 0 auto;
    padding: 60px 20px;
}

/* 카테고리 선택 */
.category-label {
    font-size: 1.1rem;
    font-weight: 500;
    color: #8b95a1;
    margin-bottom: 12px;
    display: block;
}
.category-group {
    display: flex;
    gap: 10px;
    margin-bottom: 40px;
    overflow-x: auto;
    padding-bottom: 5px;
}
.category-group::-webkit-scrollbar {
    display: none;
}

/* 라디오 버튼 숨기고 라벨 스타일링 */
input[type="radio"] {
    display: none;
}
.chip {
    padding: 10px 20px;
    border-radius: 24px;
    background: #f2f4f6;
    color: #6b7684;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s;
    white-space: nowrap;
    font-size: 1rem;
}
input[type="radio"]:checked + .chip {
    background: #e8f5e9;
    color: var(--primary);
    border: 1px solid var(--primary);
    box-shadow: 0 4px 10px rgba(0, 209, 91, 0.1);
}

/* 제목 입력 */
.input-title {
    width: 100%;
    border: none;
    outline: none;
    font-size: 2.0rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 30px;
    line-height: 1.3;
    background: transparent;
}
.input-title::placeholder {
    color: #e0e0e0;
}

/* 구분선 */
.divider {
    width: 40px;
    height: 4px;
    background: #e5e8eb;
    border-radius: 2px;
    margin-bottom: 40px;
}

/* 본문 입력 */
.input-content {
    width: 100%;
    border: none;
    outline: none;
    font-size: 1.05rem;
    line-height: 1.8;
    color: #333;
    min-height: 500px;
    resize: none;
    font-family: inherit;
}
.input-content::placeholder {
    color: var(--placeholder);
}

/* 하단 헬퍼 텍스트 */
.helper-text {
    margin-top: 40px;
    padding: 20px;
    background: #f9fafb;
    border-radius: 12px;
    color: #8b95a1;
    font-size: 0.9rem;
    line-height: 1.5;
}

.loading-text {
    color: #8b95a1;
    font-size: 0.9rem;
}
</style>
