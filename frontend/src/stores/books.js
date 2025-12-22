import { defineStore } from "pinia";
import { getNewSpecial } from "@/api/books";

export const useBooksStore = defineStore("books", {
  state: () => ({
    newSpecial: [],
    newSpecialLoading: false,
    newSpecialError: "",
  }),

  actions: {
    fetchNewSpecial() {
      this.newSpecialLoading = true;
      this.newSpecialError = "";
      this.newSpecial = [];

      getNewSpecial()
        .then((res) => {
          const list = Array.isArray(res.data) ? res.data : [];
          this.newSpecial = list.slice(0, 5);
        })
        .catch((err) => {
          console.error("[new/special 실패]", err.response?.status, err.response?.data || err.message);
          this.newSpecialError = "주목할 만한 신간을 불러오지 못했습니다.";
        })
        .finally(() => {
          this.newSpecialLoading = false;
        });
    },
  },
});
