import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

export const setAuthToken = (token: string) => {
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
};

export default api;
