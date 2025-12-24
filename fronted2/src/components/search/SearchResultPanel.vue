<template>
  <teleport to="body">
    <div v-if="store.isOpen" class="panelWrap" @click.self="store.closePanel()">
      <div class="panel glass">
        <div class="head">
          <div class="title">검색 결과</div>
          <button class="close" @click="store.closePanel()">닫기</button>
        </div>

        <div v-if="store.loading" class="state">불러오는 중...</div>
        <div v-else-if="store.error" class="state err">{{ store.error }}</div>

        <div v-else class="list">
          <button
            class="item"
            v-for="b in store.items"
            :key="b.isbn13 || b.title"
            @click="$emit('select', b)"
          >
            <div class="cover">
              <img v-if="b.cover" :src="b.cover" alt="" />
              <div v-else class="ph">Cover</div>
            </div>
            <div class="meta">
              <div class="t">{{ b.title }}</div>
              <div class="a">{{ b.author }}</div>
            </div>
            <div class="cta">선택</div>
          </button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { useBookSearchStore } from "@/stores/bookSearch";
const store = useBookSearchStore();
defineEmits(["select"]);
</script>

<style scoped>
.panelWrap{
  position: fixed; inset: 0;
  z-index: 5000;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 86px 18px 18px;
  background: rgba(15, 23, 42, 0.18);
}

.glass{
  background: rgba(255,255,255,0.85);
  border: 1px solid rgba(255,255,255,0.5);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow: 0 24px 60px rgba(0,0,0,0.12);
  border-radius: 22px;
}

.panel{
  width: min(760px, 100%);
  overflow: hidden;
}

.head{
  display:flex; align-items:center; justify-content:space-between;
  padding: 16px 16px 10px;
}
.title{ font-weight: 900; letter-spacing: -0.4px; }
.close{ color: #6b7280; font-weight: 800; }
.close:hover{ color: var(--primary); }

.state{
  padding: 18px 16px 20px;
  color: #64748b;
  font-weight: 400;
}
.err{ color: #ef4444; }

.list{
  padding: 6px;
  display: grid;
  gap: 6px;
  max-height: min(520px, calc(100vh - 180px));
  overflow: auto;
}

.item{
  width:100%;
  display:flex; align-items:center; gap: 12px;
  padding: 10px 12px;
  border-radius: 16px;
  background: rgba(255,255,255,0.7);
  border: 1px solid rgba(0,0,0,0.04);
  transition: 0.15s;
  text-align: left;
}
.item:hover{
  background: white;
  transform: translateY(-1px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

.cover{
  width: 42px; height: 56px;
  border-radius: 12px;
  overflow: hidden;
  background: #f1f5f9;
  display:flex; align-items:center; justify-content:center;
  flex: 0 0 auto;
}
.cover img{ width:100%; height:100%; object-fit: cover; }
.ph{ font-size: 0.75rem; color:#94a3b8; font-weight:800; }

.meta{ flex: 1; min-width: 0; display:grid; gap: 2px; }
.t{
  font-weight: 900;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.a{
  color: #64748b;
  font-weight: 400;
  font-size: 0.9rem;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.cta{
  font-weight: 900;
  color: var(--primary);
}
</style>
