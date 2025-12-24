import { defineStore } from "pinia";
import { getBestsellers, searchBooks } from "@/api/books.api";

export const useBooksStore = defineStore("books", {
  state: () => ({
    bestsellers: [],
    bestLoading: false,
    bestError: "",

    searchQ: "",
    searchLoading: false,
    searchError: "",
    searchResults: [],
  }),

  actions: {
    fetchBestsellers() {
      if (this.bestLoading) return;
      this.bestLoading = true;
      this.bestError = "";

      return getBestsellers()
        .then((res) => {
          this.bestsellers = res.data || [];
        })
        .catch((err) => {
          console.error("[bestsellers 실패]", err.response?.status, err.response?.data || err.message);
          this.bestError = "베스트셀러를 불러오지 못했습니다.";
        })
        .finally(() => {
          this.bestLoading = false;
        });
    },

    search(q) {
      const term = String(q || "").trim();
      this.searchQ = term;

      if (!term) {
        this.searchResults = [];
        this.searchError = "";
        this.searchLoading = false;
        return Promise.resolve();
      }

      this.searchLoading = true;
      this.searchError = "";

      return searchBooks(term)
        .then((res) => {
          // API 응답에서 items 배열 추출
          this.searchResults = res.data?.items || res.data || [];
        })
        .catch((err) => {
          console.error("[search 실패]", err.response?.status, err.response?.data || err.message);
          this.searchError = "검색에 실패했습니다.";
          this.searchResults = [];
        })
        .finally(() => {
          this.searchLoading = false;
        });
    },
  },
});
