import api from "./axios";

export const getNewSpecial = () => {
  return api.get("/api/books/new/special/", { auth: false });
};
