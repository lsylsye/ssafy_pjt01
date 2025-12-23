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
.mypage {
  padding: 32px;
  background: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

.tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0;
}

.tabs a {
  text-decoration: none;
  color: var(--text-secondary);
  padding: 12px 16px;
  border: none;
  border-radius: 0;
  font-weight: 600;
  font-size: 15px;
  transition: var(--transition);
  position: relative;
  cursor: pointer;
}

.tabs a:hover {
  color: var(--primary-color);
}

.tabs a.active {
  color: var(--primary-color);
  border-bottom: 3px solid var(--primary-color);
  margin-bottom: -2px;
}

.content {
  margin-top: 0;
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow-sm);
}

@media (max-width: 640px) {
  .mypage {
    padding: 20px 16px;
  }

  .tabs {
    gap: 8px;
  }

  .tabs a {
    padding: 10px 12px;
    font-size: 14px;
  }

  .content {
    padding: 20px;
  }
}
</style>
