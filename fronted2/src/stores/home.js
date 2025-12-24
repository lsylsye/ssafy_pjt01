import { defineStore } from "pinia";
import { getBestsellers } from "@/api/books.api";

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
  },
});
