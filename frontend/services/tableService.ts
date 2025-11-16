import axios from "@/lib/axios"; // configuración base (baseURL, headers, etc.)
import { Table, TableStatus } from "@/types/models";

export const getTables = async (): Promise<Table[]> => {
  const res = await axios.get("/tables/");
  return res.data;
};

export const updateTableStatus = async (id: number, status: TableStatus) => {
  const res = await axios.patch(`/tables/${id}/status/`, { status });
  return res.data;
};

export const createTable = async (): Promise<Table> => {
  // Backend create ignores body and sets default status
  try {
    const res = await axios.post("/tables/", {});
    return res.data;
  } catch (err: any) {
    const status = err?.response?.status;
    console.error("POST /api/tables/ failed", status, err?.message);
    // Fallback con fetch sin credentials para aislar causa (CSRF/CORS)
    try {
      const url =
        (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api") +
        "/tables/";
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "{}",
        credentials: "omit",
      });
      if (!resp.ok) {
        console.error("Fallback fetch POST /api/tables/ status", resp.status);
        throw err;
      }
      const data = await resp.json();
      return data as Table;
    } catch (fallbackErr) {
      throw err; // re-lanzamos error original
    }
  }
};
