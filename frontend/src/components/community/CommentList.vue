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
.error {
  color: #dc2626;
  background: #fee2e2;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 12px 0;
}

.clist {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.citem {
  border: none;
  border-radius: 8px;
  padding: 14px;
  background: #f9f9f9;
  border-left: 3px solid #f0f0f0;
}

.cmeta {
  color: #999;
  font-size: 12px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.nick {
  font-weight: 600;
  color: var(--text-primary);
}

.ctext {
  margin: 10px 0 0;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.5;
  font-size: 13px;
  color: var(--text-primary);
}

.cactions {
  margin-top: 10px;
  display: flex;
  gap: 12px;
}

.linkbtn {
  border: none;
  background: none;
  color: var(--primary-color);
  cursor: pointer;
  padding: 0;
  font-weight: 500;
  font-size: 12px;
  transition: var(--transition);
}

.linkbtn:hover {
  color: var(--primary-dark);
}

.replybox {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.input {
  flex: 1;
  min-width: 150px;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 8px 10px;
  font-size: 12px;
  transition: var(--transition);
  background: #ffffff;
  color: var(--text-primary);
}

.input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.1);
}

.btn {
  border: 1px solid #ddd;
  background: #ffffff;
  border-radius: 6px;
  padding: 8px 12px;
  cursor: pointer;
  color: var(--text-primary);
  font-weight: 500;
  transition: var(--transition);
  font-size: 12px;
}

.btn:hover {
  border-color: var(--primary-color);
  background: #f5f5f5;
  color: var(--primary-color);
}

.rlist {
  list-style: none;
  padding: 0 0 0 18px;
  margin: 12px 0 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-left: 2px solid #f0f0f0;
}

.ritem {
  border: none;
  border-radius: 6px;
  padding: 12px;
  background: #ffffff;
  margin-left: 10px;
  border-left: 3px solid #f0f0f0;
}

.ritem:hover {
  border-left-color: var(--primary-color);
}
</style>
