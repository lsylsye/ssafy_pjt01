<template>
  <div class="my-lib-container">
    <h1>My Library</h1>
    
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <!-- Profile Section -->
      <section class="profile-section">
        <h2>Profile</h2>
        <div v-if="user" class="profile-card">
          <img :src="user.profile_image || '/default-profile.png'" alt="Profile Image" class="profile-img" />
          <div class="profile-info">
            <p><strong>Nickname:</strong> {{ user.nickname }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>Level:</strong> {{ user.level }} (EXP: {{ user.exp_total }})</p>
            <p><strong>Favorite Country:</strong> {{ user.favorite_country }}</p>
            <p><strong>Favorite Genre:</strong> {{ user.favorite_genre }}</p>
          </div>
        </div>
      </section>

      <!-- Bookmarks Section -->
      <section class="bookmarks-section">
        <h2>My Bookmarks</h2>
        <div v-if="bookmarks.length === 0">No bookmarks yet.</div>
        <ul v-else class="bookmark-list">
          <li v-for="bookmark in bookmarks" :key="bookmark.id" class="bookmark-item">
            {{ bookmark.book.title }}
          </li>
        </ul>
      </section>

      <!-- Posts Section -->
      <section class="posts-section">
        <h2>My Posts & Reviews</h2>
        <div v-if="posts.length === 0">No posts yet.</div>
        <ul v-else class="post-list">
          <li v-for="(post, index) in posts" :key="index" class="post-item">
            <span class="post-type">[{{ post.type_name }}]</span>
            <span class="post-title">{{ post.title }}</span>
            <span class="post-date">{{ new Date(post.created_at).toLocaleDateString() }}</span>
          </li>
        </ul>
      </section>

      <!-- Comments Section -->
      <section class="comments-section">
        <h2>My Comments</h2>
        <div v-if="comments.length === 0">No comments yet.</div>
        <ul v-else class="comment-list">
          <li v-for="comment in comments" :key="comment.comment_id" class="comment-item">
             <p class="comment-content">{{ comment.content }}</p>
             <small>On: {{ comment.post_title }} ({{ new Date(comment.created_at).toLocaleDateString() }})</small>
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getMyProfile, getMyBookmarks, getMyPosts, getMyComments } from '@/api/mypage';

const user = ref(null);
const bookmarks = ref([]);
const posts = ref([]);
const comments = ref([]);
const loading = ref(true);

const fetchData = async () => {
  try {
    loading.value = true;
    const [profileRes, bookmarksRes, postsRes, commentsRes] = await Promise.all([
      getMyProfile(),
      getMyBookmarks(),
      getMyPosts(),
      getMyComments()
    ]);

    user.value = profileRes.data;
    bookmarks.value = bookmarksRes.data;
    posts.value = postsRes.data;
    comments.value = commentsRes.data;
  } catch (error) {
    console.error("Failed to fetch My Page data:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.my-lib-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

section {
  margin-bottom: 40px;
}

.profile-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.profile-img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
}
</style>
