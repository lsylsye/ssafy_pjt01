<template>
  <section class="test-section">
    <div class="container">
      <div class="test-banner">
        <div class="deco-circle"></div>
        <div class="test-content">
          <h2>내 독서 취향은<br />어떤 나무일까요?</h2>
          <p>간단한 테스트로 나만의 도서 취향을 알아보세요.</p>
        </div>
        <button class="test-btn" @click="$emit('start')">테스트 시작하기</button>
      </div>
    </div>
  </section>
</template>

<script setup>
defineEmits(["start"]);
</script>

<style scoped>
.test-section{ width: 100%; }
.container{ max-width: 1100px; margin: 0 auto; padding: 0 24px; width: 100%; }

.test-banner{
  margin-top: 60px;
  padding: 50px;
  background: linear-gradient(120deg, #191f28 0%, #2b3340 100%);
  color: white;
  border-radius: 32px;
  position: relative;
  overflow: hidden;
  display:flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
  gap: 18px;
}
.test-content h2{ font-size: 2rem; margin-bottom: 10px; font-weight: 900; letter-spacing: -0.6px; }
.test-content p{ color: rgba(255,255,255,0.7); font-size: 1.05rem; font-weight: 400; }

.test-btn{
  background: var(--primary);
  color: white;
  padding: 16px 30px;
  font-size: 1.05rem;
  font-weight: 900;
  border-radius: 100px;
  box-shadow: 0 10px 20px rgba(0,209,91,0.3);
  transition: 0.2s;
  white-space: nowrap;
}
.test-btn:hover{ transform: scale(1.04); background: #00e063; }

.deco-circle{
  position:absolute;
  width: 300px; height: 300px;
  background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
  opacity: 0.2;
  filter: blur(40px);
  top: -100px; right: -50px;
}

@media (max-width: 740px){
  .test-banner{ flex-direction: column; align-items: flex-start; padding: 28px; }
  .test-content h2{ font-size: 1.6rem; }
}
</style>
