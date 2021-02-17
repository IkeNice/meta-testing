import axios from "axios";

const app_id = "appbssvSnF3Oq5dgI";
const app_key = "key2opSCUNgWPJ6x0";

const apiClient = axios.create({
  baseURL: "https://api.airtable.com/v0/" + app_id,
  withCreditans: false,
  headers: {
    Authorization: "Bearer " + app_key,
    Accept: "application/json",
    "Content-Type": "application/json"
  }
});

export default {
  getAllProfiles() {
    return apiClient.get("/Psychotherapists");
  },
  getProfile(id) {
    return apiClient.get("/Psychotherapists/" + id);
  }
};
