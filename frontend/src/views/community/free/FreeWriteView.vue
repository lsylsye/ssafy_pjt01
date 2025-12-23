<template>
  <section>
    <h2>자유게시판 글쓰기</h2>

    <p v-if="loading">처리 중...</p>
    <p v-else-if="errorMsg" class="error">{{ errorMsg }}</p>

    <FreePostForm
      :disabled="loading"
      submit-text="등록"
      :error-msg="errorMsg"
      :show-prefix="true"
      @submit="submit"
    />
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import useCountry from "@/composables/useCountry";
import { useAuthStore } from "@/stores/auth";
import { useFreeStore } from "@/stores/community/free";
import FreePostForm from "@/components/community/free/FreePostForm.vue";

const router = useRouter();
const { country } = useCountry();

const auth = useAuthStore();
const store = useFreeStore();

const loading = ref(false);
const errorMsg = ref("");

const submit = (payload) => {
  if (!auth.isLoggedIn) {
    router.push("/login");
    return;
  }

  const body = {
    title: payload.title,
    content: payload.content,
    prefix_name: payload.prefix_name ?? null,
  };

  loading.value = true;
  errorMsg.value = "";

  store
    .createPost(country.value, body) // ✅ 내부에서 country 소문자 처리(api에서 처리)
    .then((data) => {
      const id = data?.id;
      router.push(id ? `/community/${country.value}/free/${id}` : `/community/${country.value}/free`);
    })
    .catch(() => {
      errorMsg.value = "글 작성에 실패했습니다.";
    })
    .finally(() => {
      loading.value = false;
    });
};
</script>

<style scoped>
section {
  padding: 24px;
  min-height: auto;
  max-width: 900px;
  margin: 0 auto;
  background: #ffffff;
}

h2 {
  margin: 0 0 20px;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.error {
  color: #dc2626;
  background: #fee2e2;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 12px 0;
}
</style>
