import axios from "axios";

const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  withCredentials: true,
});

instance.interceptors.response.use(
  (response) => response,
  (error) => {
    // Manejo global de errores (401, 403, etc.)
    console.error("API Error:", error.response?.status, error.message);
    return Promise.reject(error);
  }
);

export default instance;
