import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 8000,
  headers: {
    "x-api-key": "super-secret-owner-key", // MUST MATCH .env
  },
});

/* =========================
   DASHBOARD APIs (OWNER)
========================= */

export const getDashboardOverview = async () => {
  const res = await api.get("/owner/dashboard/overview");
  return res.data;
};

export const getLowViewArticles = async () => {
  const res = await api.get("/owner/dashboard/low-view");
  return res.data;
};

export const getTopArticles = async () => {
  const res = await api.get("/owner/dashboard/top-articles");
  return res.data;
};

export const getTrendingMemory = async () => {
  const res = await api.get("/owner/dashboard/trending-memory");
  return res.data;
};

export default api;
