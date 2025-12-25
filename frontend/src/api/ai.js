import api from "./axios";

export const getBookTravelInfo = (country) => {
    return api.post("ai_curator/travel/", { country });
};

export const getSupportedCountries = () => {
    return api.get("ai_curator/travel/countries/");
};
