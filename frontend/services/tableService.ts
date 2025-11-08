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
