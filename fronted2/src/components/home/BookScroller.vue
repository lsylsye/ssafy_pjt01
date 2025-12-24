<template>
  <section class="book-section">
    <div class="container">
      <div class="section-header">
        <h2>{{ title }}</h2>
        <button class="link-more" type="button" @click="$emit('more')">더보기</button>
      </div>

      <div class="book-scroller">
        <div v-if="loading" class="state">불러오는 중...</div>
        <div v-else-if="error" class="state err">{{ error }}</div>

        <div v-else class="row">
          <button
            v-for="b in books"
            :key="b.id || b.isbn13 || b.title"
            class="book-card"
            type="button"
            @click="$emit('select', b)"
          >
            <div class="cover-wrapper">
              <img v-if="b.cover" :src="b.cover" alt="" />
              <div v-else class="ph">Cover</div>
            </div>

            <div class="book-meta">
              <h3 :title="b.title">{{ b.title }}</h3>
              <p :title="b.author">{{ b.author }}</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: { type: String, default: "많은 사람들이 찾는 책 📖" },
  books: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: String, default: "" },
});
defineEmits(["more", "select"]);
</script>

<style scoped>
.book-section{ width:100%; }
.container{ max-width:1100px; margin:0 auto; padding:0 24px; width:100%; }

.section-header{
  display:flex;
  justify-content:space-between;
  align-items:flex-end;
  margin:60px 0 24px;
}
.section-header h2{ font-size:1.8rem; font-weight:900; letter-spacing:-0.5px; }
.link-more{ font-size:0.9rem; font-weight:900; color:var(--text-sub); }
.link-more:hover{ color:var(--primary); }

.book-scroller{
  overflow-x:auto;
  padding:10px 10px 40px 10px;
  scroll-behavior:smooth;
  scroll-snap-type:x mandatory;
  -webkit-overflow-scrolling:touch;
}
.book-scroller::-webkit-scrollbar{ height:10px; }
.book-scroller::-webkit-scrollbar-thumb{ background:rgba(0,0,0,0.12); border-radius:999px; }
.book-scroller::-webkit-scrollbar-track{ background:transparent; }

.row{
  display:flex;
  gap:24px;
  align-items:flex-start;
}

/* ✅ 핵심: 카드 폭 고정(제목 길이 상관없이 동일) */
.book-card{
  --card-w:180px;
  flex:0 0 var(--card-w);
  width:var(--card-w);

  scroll-snap-align:start;

  padding:0;
  border:0;
  background:none;

  cursor:pointer;
  transition:transform 0.25s;
  text-align:left;
}
.book-card:hover{ transform:translateY(-10px); }

.cover-wrapper{
  width:100%;
  height:260px;
  border-radius:var(--radius-md);
  background:#fff;
  box-shadow:0 8px 20px rgba(0,0,0,0.08);
  overflow:hidden;
  margin-bottom:16px;
  position:relative;
  display:flex;
  align-items:center;
  justify-content:center;
}
.cover-wrapper::after{
  content:"";
  position:absolute;
  inset:0;
  background:linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 50%);
  pointer-events:none;
}
.cover-wrapper img{ width:100%; height:100%; object-fit:cover; }
.ph{ font-weight:900; color:#94a3b8; }

.book-meta{ min-width:0; }
.book-meta h3{
  font-size:1.05rem;
  font-weight:900;
  margin-bottom:4px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.book-meta p{
  font-size:0.9rem;
  color:var(--text-sub);
  font-weight:400;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.state{ font-weight:800; color:#64748b; }
.err{ color:#ef4444; }

@media (max-width:560px){
  .container{ padding:0 16px; }
  .book-card{ --card-w:150px; }
  .cover-wrapper{ height:220px; }
  .row{ gap:16px; }
}
</style>
