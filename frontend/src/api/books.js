import api from "@/api/axios";

export const getNewSpecial = () => {
  return api.get("/api/books/new/special/", { auth: false });
};
