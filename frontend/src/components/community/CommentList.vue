<template>
  <div>
    <p v-if="loading">댓글 불러오는 중...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <div v-else>
      <p v-if="!items || items.length === 0">댓글이 없습니다.</p>

      <ul v-else class="clist">
        <li v-for="c in items" :key="c.id" class="citem">
          <div class="cmeta">
            <span class="nick">{{ c.user_nickname }}</span>
            <span class="date">{{ formatDate(c.created_at) }}</span>
            <span class="count">좋아요 {{ c.like_count }}</span>
          </div>

          <p class="ctext">{{ c.content }}</p>

          <div class="cactions" v-if="actionsEnabled">
            <button class="linkbtn" @click="$emit('like', c.id)">좋아요</button>
            <button class="linkbtn" @click="$emit('remove', c.id)">삭제</button>
            <button class="linkbtn" @click="startReply(c.id)">답글</button>
          </div>

          <div v-if="replyingTo === c.id && actionsEnabled" class="replybox">
            <input v-model="replyText" class="input" placeholder="답글 입력" />
            <button class="btn" @click="submitReply(c.id)">등록</button>
            <button class="btn" @click="cancelReply">취소</button>
          </div>

          <ul v-if="c.replies && c.replies.length" class="rlist">
            <li v-for="r in c.replies" :key="r.id" class="ritem">
              <div class="cmeta">
                <span class="nick">{{ r.user_nickname }}</span>
                <span class="date">{{ formatDate(r.created_at) }}</span>
                <span class="count">좋아요 {{ r.like_count }}</span>
              </div>

              <p class="ctext">{{ r.content }}</p>

              <div class="cactions" v-if="actionsEnabled">
                <button class="linkbtn" @click="$emit('like', r.id)">좋아요</button>
                <button class="linkbtn" @click="$emit('remove', r.id)">삭제</button>
              </div>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: String, default: "" },
  actionsEnabled: { type: Boolean, default: false }, // 로그인 상태
});

const emit = defineEmits(["reply", "like", "remove"]);

const replyingTo = ref(null);
const replyText = ref("");

const formatDate = (iso) => (typeof iso === "string" ? iso.slice(0, 10) : "");

const startReply = (id) => {
  replyingTo.value = id;
  replyText.value = "";
};

const cancelReply = () => {
  replyingTo.value = null;
  replyText.value = "";
};

const submitReply = (parentId) => {
  const v = replyText.value.trim();
  if (!v) return;
  emit("reply", { parentId, content: v });
  cancelReply();
};
</script>

<style scoped>
.error { color: #d33; }

.clist { list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:12px; }
.citem { border:1px solid #eee; border-radius:12px; padding:10px 12px; }
.cmeta { color:#666; font-size:13px; display:flex; gap:10px; flex-wrap:wrap; }
.nick { font-weight:700; color:#333; }
.ctext { margin:6px 0 0; white-space:pre-wrap; }

.cactions { margin-top:8px; display:flex; gap:10px; }
.linkbtn { border:none; background:none; color:#1a73e8; cursor:pointer; padding:0; }

.replybox { display:flex; gap:8px; margin-top:8px; }
.input { flex:1; border:1px solid #ddd; border-radius:10px; padding:8px 10px; }
.btn { border:1px solid #ddd; background:white; border-radius:10px; padding:8px 12px; cursor:pointer; }

.rlist { list-style:none; padding:0; margin:10px 0 0 18px; display:flex; flex-direction:column; gap:10px; }
.ritem { border:1px dashed #e6e6e6; border-radius:12px; padding:10px 12px; background:#fcfcfc; }
</style>
