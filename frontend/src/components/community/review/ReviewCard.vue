<template>
  <div class="card" @click="emit('open', review?.id)">
    <div class="left">
      <img
        v-if="hasCover"
        :src="review.cover"
        alt="cover"
        @error="onImgError"
      />
      <div v-else class="placeholder"></div>
    </div>

    <div class="right">
      <div class="book">
        <div class="title">{{ review?.book_title || "-" }}</div>
        <div class="meta">
          {{ review?.book_author || "-" }}
          <span class="dot">·</span>
          {{ review?.publisher || "-" }}
          <span class="dot">·</span>
          {{ formatDate(review?.created_at) }}
        </div>
      </div>

      <div class="content">{{ review?.content || "" }}</div>

      <div class="bottom">
        <div class="user">{{ review?.user_nickname || "-" }}</div>
        <div class="stats">
          <span>★ {{ review?.rating ?? "-" }}</span>
          <span>♥ {{ review?.like_count ?? 0 }}</span>
          <span>💬 {{ review?.comment_count ?? 0 }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";

const props = defineProps({
  review: {
    type: Object,
    required: true,
    default: () => ({}),
  },
});

const emit = defineEmits(["open"]);

const coverOk = ref(true);

const hasCover = computed(() => {
  return coverOk.value && !!props.review?.cover;
});

const onImgError = () => {
  coverOk.value = false;
};

const formatDate = (iso) => {
  if (!iso) return "-";
  return String(iso).split("T")[0] || "-";
};
</script>

<style scoped>
.card { display:flex; gap:12px; padding:12px; border:1px solid #eee; border-radius:10px; cursor:pointer; }
.left img { width:72px; height:100px; object-fit:cover; border-radius:6px; }
.placeholder { width:72px; height:100px; background:#f2f2f2; border-radius:6px; }
.right { flex:1; display:flex; flex-direction:column; gap:6px; min-width:0; }
.title { font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.meta { font-size:12px; color:#666; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.dot { margin: 0 6px; color:#bbb; }
.content { font-size:13px; color:#333; overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; }
.bottom { display:flex; justify-content:space-between; font-size:12px; color:#666; margin-top:auto; }
.stats { display:flex; gap:8px; }
</style>
