<template>
  <section class="test-section">
    <div class="container">
      <div class="test-banner" @click="$emit('start')">
        <div class="deco-circle"></div>
        <div class="test-content">
          <h2>내 독서 취향은 무슨 나무일까요?</h2>
          <p>간단한 테스트로 나만의 독서 DNA를 찾아보세요.</p>
        </div>
        <button class="test-btn">테스트 시작하기 ></button>
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
  /* Navy and Mint dynamic gradient */
  background: linear-gradient(-45deg, #191f28, #1a355e, #4fd1c5, #191f28);
  background-size: 200% 200%;
  animation: gradientBG 10s ease-in-out infinite;
  
  color: white;
  border-radius: 32px;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.3s ease;
  gap: 18px;
}
.test-banner:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 50px rgba(0,0,0,0.2);
}


@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
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
