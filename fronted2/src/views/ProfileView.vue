<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api/axios';

const route = useRoute();
const router = useRouter();
const profile = ref(null);
const loading = ref(true);

const fetchProfile = async () => {
    try {
        const id = route.params.id;
        const res = await api.get(`users/profile/${id}/`);
        profile.value = res.data;
    } catch (e) {
        console.error(e);
        alert("프로필 정보를 불러오지 못했습니다.");
        router.back();
    } finally {
        loading.value = false;
    }
};

const getProfileImage = (url) => {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return `http://127.0.0.1:8000${url}`;
};

onMounted(fetchProfile);
</script>

<template>
  <div class="profile-page">
    <div v-if="loading" class="loading">불러오는 중...</div>
    <div v-else-if="profile" class="profile-container">
      <div class="header-card">
        <div 
          class="profile-avatar"
          :style="{ 
            backgroundImage: profile.profile_image ? `url(${getProfileImage(profile.profile_image)})` : 'none' 
          }"
        ></div>
        <h1 class="nickname">{{ profile.nickname }}</h1>
        <p class="email" v-if="profile.email">{{ profile.email }}</p>
        <div class="stats">
            <div class="stat-item">
                <span class="label">게시글</span>
                <span class="value">{{ profile.post_count || 0 }}</span>
            </div>
            <div class="stat-item">
                <span class="label">댓글</span>
                <span class="value">{{ profile.comment_count || 0 }}</span>
            </div>
        </div>
      </div>

      <div class="info-section">
        <h2>소개</h2>
        <p class="bio">{{ profile.bio || '등록된 소개가 없습니다.' }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
    min-height: 100vh;
    background: #f2f4f6;
    padding: 40px 20px;
    font-family: "Pretendard", sans-serif;
}
.profile-container {
    max-width: 600px;
    margin: 0 auto;
}
.header-card {
    background: #fff;
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.profile-avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    margin: 0 auto 20px;
    background: #eee;
    background-size: cover;
    background-position: center;
}
.nickname {
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 8px;
    color: #191f28;
}
.email {
    color: #8b95a1;
    margin-bottom: 24px;
}
.stats {
    display: flex;
    justify-content: center;
    gap: 40px;
    border-top: 1px solid #f2f4f6;
    padding-top: 24px;
}
.stat-item .label {
    display: block;
    font-size: 0.9rem;
    color: #8b95a1;
    margin-bottom: 4px;
}
.stat-item .value {
    font-size: 1.2rem;
    font-weight: 700;
    color: #191f28;
}
.info-section {
    background: #fff;
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}
.info-section h2 {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 16px;
}
.bio {
    color: #4e5968;
    line-height: 1.6;
}
.loading {
    text-align: center;
    padding: 100px;
    color: #8b95a1;
}
</style>
