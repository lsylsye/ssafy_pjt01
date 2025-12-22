import { defineStore } from "pinia";
import { getUserProfile, toggleFollow } from "@/api/users";

export const useUserProfileStore = defineStore("userProfile", {
  state: () => ({
    profile: null,
    loading: false,
    error: "",
    toggling: false,
    toggleError: "",
  }),

  actions: {
    fetchProfile(userId) {
      this.loading = true;
      this.error = "";
      this.profile = null;

      getUserProfile(userId)
        .then((res) => {
          this.profile = res.data || null;
        })
        .catch((err) => {
          console.error("[프로필 조회 실패]", err.response?.status, err.response?.data || err.message);
          this.error = "프로필을 불러오지 못했습니다.";
        })
        .finally(() => {
          this.loading = false;
        });
    },

    toggleFollow(userId) {
      if (this.toggling) return;

      this.toggling = true;
      this.toggleError = "";

      toggleFollow(userId)
        .then((res) => {
          // ✅ 서버가 최신 상태 내려주면 그걸 우선 사용
          const data = res.data || {};

          if (this.profile) {
            if (typeof data.is_following !== "undefined") {
              this.profile.is_following = !!data.is_following;
            } else {
              // ✅ fallback: 서버가 is_following을 안주면 로컬 토글
              this.profile.is_following = !this.profile.is_following;
            }

            if (typeof data.followers_count !== "undefined") {
              this.profile.followers_count = Number(data.followers_count || 0);
            } else {
              // ✅ fallback: 서버가 followers_count 안주면 로컬로만 +/-
              const cur = Number(this.profile.followers_count || 0);
              this.profile.followers_count = this.profile.is_following ? cur + 1 : Math.max(0, cur - 1);
            }
          }
        })
        .catch((err) => {
          const status = err.response?.status;
          console.error("[팔로우 토글 실패]", status, err.response?.data || err.message);

          if (status === 401) {
            // ✅ 뷰에서 로그인 이동 처리할 수 있게 에러만 세팅
            this.toggleError = "로그인이 필요합니다.";
            return;
          }
          this.toggleError = "팔로우 처리에 실패했습니다.";
        })
        .finally(() => {
          this.toggling = false;
        });
    },
  },
});
