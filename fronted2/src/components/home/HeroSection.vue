<template>
  <section class="container hero-section">
    <h1 class="hero-title">
      마음의 양식을 심다.<br /><span>잔디북</span>
    </h1>
    <p class="hero-desc">
      나만의 도서 페이지에 취향을 심고, 매일매일 자라나는 기록을 확인하세요.
    </p>

    <slot />
  </section>
</template>

<style scoped>
.hero-section { text-align:center; padding: 40px 0 80px; }
.hero-title {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 12px;
  letter-spacing: -1px;
  line-height: 1.2;
}
.hero-title span { color: var(--primary); }
.hero-desc {
  font-size: 1.1rem;
  color: var(--text-sub);
  margin-bottom: 50px;
}
@media (max-width: 700px){
  .hero-title{ font-size: 2.3rem; }
}
</style>
