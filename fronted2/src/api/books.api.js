import api from "./axios";

export const getBestsellers = () => api.get("/books/bestsellers/", { auth: false });
export const searchBooks = (q) => api.get(`books/search/?q=${encodeURIComponent(q)}`, { auth: false });
