import api from "@/api/axios";

export const getMyGrass = (params = {}) => {
    return api.get("grass/me/", { params });
};

export const getMyLevel = () => {
    return api.get("grass/level/me/");
};
