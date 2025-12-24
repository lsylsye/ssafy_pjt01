import { defineStore } from "pinia";
import { searchBooks } from "@/api/books.api";

function normalizeBooks(data) {
  const list = Array.isArray(data) ? data : (data?.items || data?.results || []);
  return (list || []).map((b) => ({
    isbn13: b.isbn13 || b.isbn || b.itemId || b.id,
    title: b.title || "",
    author: b.author || "",
    cover: b.cover || b.cover_url || "",
    publisher: b.publisher || "",
    pubDate: b.pub_date || b.pubDate || "",
  }));
}

export const useBookSearchStore = defineStore("bookSearch", {
  state: () => ({
    q: "",
    items: [],
    loading: false,
    error: "",
    isOpen: false,
    _t: 0,
  }),

  actions: {
    setQuery(v) {
      this.q = v;
      if (!v) {
        this.items = [];
        this.error = "";
        this.isOpen = false;
      }
    },

    async searchNow(q) {
      const query = (q ?? this.q).trim();
      if (query.length < 2) {
        this.items = [];
        this.error = "";
        this.isOpen = false;
        return;
      }

      this.loading = true;
      this.error = "";
      this.isOpen = true;

      try {
        const res = await searchBooks(query);
        this.items = normalizeBooks(res.data);
        if (this.items.length === 0) this.error = "검색 결과가 없어요.";
      } catch (e) {
        this.items = [];
        this.error = "검색에 실패했어요.";
      } finally {
        this.loading = false;
      }
    },

    // 입력 중 자동 검색(디바운스)
    debouncedSearch(q) {
      const query = (q ?? this.q).trim();
      clearTimeout(this._t);
      if (query.length < 2) return;
      this._t = setTimeout(() => {
        this.searchNow(query);
      }, 250);
    },

    closePanel() {
      this.isOpen = false;
    },
  },
});
