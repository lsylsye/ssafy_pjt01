<template>
  <section>
    <div class="filters">
      <input v-model="q" class="input" placeholder="검색(제목+내용)" />
      <input v-model="prefix" class="input" placeholder="말머리(예: 잡담) - 선택" />
      <button class="btn" :disabled="loading" @click="search">검색</button>
    </div>

    <p v-if="loading">불러오는 중...</p>
    <p v-else-if="errorMsg" class="error">{{ errorMsg }}</p>

    <div v-else>
      <p v-if="posts.length === 0">게시글이 없습니다.</p>

      <ul v-else class="list">
        <FreePostCard
          v-for="p in posts"
          :key="p.id"
          :post="p"
          :to="`/community/${country}/free/${p.id}`"
        />
      </ul>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { storeToRefs } from "pinia";
import useCountry from "@/composables/useCountry";
import { useFreeStore } from "@/stores/community/free";
import FreePostCard from "@/components/community/free/FreePostCard.vue";

const { country } = useCountry();
const store = useFreeStore();
const { loading, errorMsg, posts } = storeToRefs(store);

const q = ref("");
const prefix = ref("");

const fetch = () => {
  store.fetchList(country.value, {
    q: q.value.trim() || undefined,
    prefix: prefix.value.trim() || undefined,
  });
};

const search = () => fetch();

onMounted(fetch);

watch(
  () => country.value,
  () => {
    q.value = "";
    prefix.value = "";
    fetch();
  }
);
</script>

<style scoped>
.filters { display:flex; gap:10px; margin-bottom:12px; align-items:center; }
.input { flex:1; padding:8px 10px; border:1px solid #ddd; border-radius:8px; }
.btn { border:1px solid #ddd; background:white; border-radius:8px; padding:8px 12px; cursor:pointer; }
.btn:hover { border-color:#1a73e8; color:#1a73e8; }
.error { color:#d33; }
.list { list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:12px; }
</style>
