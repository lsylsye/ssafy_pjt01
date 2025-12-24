<template>
  <div class="sprout-icon-wrapper" aria-hidden="true">
    <div class="stem"></div>
    <div class="leaf left"></div>
    <div class="leaf right"></div>
  </div>
</template>

<style scoped>
.sprout-icon-wrapper{
  position:relative;width:24px;height:24px;
  animation: sprout-grow 0.8s cubic-bezier(0.175,0.885,0.32,1.275), sprout-float 3s ease-in-out infinite 0.8s;
  transform-origin: bottom center;
}
.stem{
  position:absolute;bottom:0;left:50%;transform:translateX(-50%);
  width:4px;height:16px;background:#00a84d;border-radius:4px;
}
.leaf{
  position:absolute;width:10px;height:10px;border-radius:50%;top:2px;
  box-shadow: inset -1px -1px 2px rgba(0,0,0,0.1);
}
.leaf.left{
  left:0;
  background: radial-gradient(circle at 30% 30%, #d1f7c4, #00d15b);
  border-radius:0 50% 50% 50%;
  transform: rotate(45deg);
}
.leaf.right{
  right:0;
  background: radial-gradient(circle at 70% 30%, #e8f5e9, #2ecc71);
  border-radius:50% 0 50% 50%;
  transform: rotate(-45deg);
}

@keyframes sprout-grow{from{transform:scale(0);opacity:0;}to{transform:scale(1);opacity:1;}}
@keyframes sprout-float{0%,100%{transform:translateY(0) rotate(0);}50%{transform:translateY(-3px) rotate(5deg);}}
</style>
