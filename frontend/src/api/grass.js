import api from "@/api/axios";

export const getMyGrass = (params = {}) => {
  return api.get("/api/grass/me/", { params });
};