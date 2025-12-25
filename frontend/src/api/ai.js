import api from "./axios";

export const getBookTravelInfo = (country) => {
    return api.post("ai_curator/travel/", { country });
};
