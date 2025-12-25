import { defineStore } from "pinia";
import { getBestsellers } from "@/api/books.api";
import { getReviews } from "@/api/review";

function normalizeBooks(data) {
  const list = Array.isArray(data) ? data : (data?.results || data?.items || []);
  return (list || []).map((b) => ({
    id: b.id || b.item_id || b.isbn13,
    isbn13: b.isbn13 || b.isbn || b.itemId,
    title: b.title || "",
    author: b.author || "",
    cover: b.cover || "",
    rank: b.best_rank || b.rank || null,
  }));
}

export const useHomeStore = defineStore("home", {
  state: () => ({
    bestsellers: [],
    loadingBestsellers: false,
    bestsellersError: "",
    latestReviews: [],
    loadingReviews: false,
  }),

  actions: {
    async fetchBestsellers() {
      this.loadingBestsellers = true;
      this.bestsellersError = "";
      try {
        const res = await getBestsellers();
        this.bestsellers = normalizeBooks(res.data);
      } catch (e) {
        this.bestsellers = [];
        this.bestsellersError = "베스트셀러를 불러오지 못했어요.";
      } finally {
        this.loadingBestsellers = false;
      }
    },

    async fetchLatestReviews() {
      this.loadingReviews = true;
      try {
        const res = await getReviews();
        // 최신순 정렬은 백엔드에서 해줄 수도 있지만 안전하게 체크
        const data = Array.isArray(res.data) ? res.data : [];
        // 날짜 내림차순 정렬 (최신순)
        const sorted = data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        this.latestReviews = sorted.slice(0, 6).map(r => ({
          id: r.id,
          user: r.user_nickname || "익명",
          time: r.created_at, // ReviewGrid에서 변환 필요
          bookTitle: r.book_title || "제목 없음",
          content: r.content || "",
          rating: r.rating,
          user_profile_image: r.user_profile_image,
        }));
      } catch (e) {
        console.error(e);
        this.latestReviews = [];
      } finally {
        this.loadingReviews = false;
      }
    }
  },
});
