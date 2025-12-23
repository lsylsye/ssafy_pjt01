<template>
  <section class="mypage">
    <h1>마이페이지</h1>

    <nav class="tabs">
      <router-link to="/mypage" exact-active-class="active">내 정보</router-link>

      <router-link to="/mypage/bookmarks" active-class="active">북마크</router-link>

      <router-link to="/mypage/activity" active-class="active">내 활동</router-link>
    </nav>

    <div class="content">
      <router-view />
    </div>
  </section>
</template>

<style scoped>
.mypage { padding: 24px; }

.tabs {
  display: flex;
  gap: 12px;
  margin: 12px 0 16px;
}

.tabs a {
  text-decoration: none;
  color: #444;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.tabs a.active {
  font-weight: bold;
  border-color: #1a73e8;
  color: #1a73e8;
}

.content { margin-top: 12px; }
</style>
