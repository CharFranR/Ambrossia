import axios from "axios";

const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  withCredentials: true,
});

axios.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status ?? "No Response";
    console.error("API Error:", status, error.message);
    return Promise.reject(error);
  }
);


export default instance;
