import axiosRoot from "axios"; // separate instance because bills endpoints are not under /api
import baseAxios from "@/lib/axios"; // may be reused later if backend normalizes paths
import type { Bill } from "@/types/models/bills";

// Root-level axios (backend mounts bill routes at path '')
const rootAxios = axiosRoot.create({
  baseURL: process.env.NEXT_PUBLIC_API_ROOT || "http://localhost:8000",
  withCredentials: true,
});

// --- Helpers ---
function normalizeBill(raw: any): Bill {
  // Backend returns createdAt / closedAt; frontend type expects created_at / closed_at
  return {
    id: raw.id,
    status: raw.status,
    created_at: raw.createdAt ?? raw.created_at ?? "",
    closed_at: raw.closedAt ?? raw.closed_at ?? null,
    amount: raw.amount ?? 0,
    IVA: raw.IVA ?? null,
    discount: raw.discount ?? null,
    total: raw.total ?? null,
  };
}

// --- API Calls ---
export const getNotPayedBills = async (): Promise<Bill[]> => {
  const res = await rootAxios.get("/bills/getNotPayedBills/");
  return (res.data as any[]).map(normalizeBill);
};

export const getPayedBills = async (): Promise<Bill[]> => {
  const res = await rootAxios.get("/bills/getPayedBills/");
  return (res.data as any[]).map(normalizeBill);
};

export const createBill = async (
  tableId: number,
  params?: { discountPercent?: number }
) => {
  const body: any = {};
  if (params?.discountPercent) body.discount = params.discountPercent; // backend expects discount % in createBill
  const res = await rootAxios.post(`/bills/createBill/${tableId}/`, body);
  return {
    bill: normalizeBill(res.data.bill),
    orders: res.data.orders as Array<{
      product: string;
      price: number;
      quantity: number;
      amount: number;
    }>,
  };
};

export const updateBill = async (
  billId: number,
  params: { IVAPercent?: number; discountAmount?: number }
) => {
  // Backend updateBill expects IVA as % and discount as absolute amount (inconsistency vs createBill)
  const body: any = {};
  if (params.IVAPercent !== undefined) body.IVA = params.IVAPercent;
  if (params.discountAmount !== undefined)
    body.discount = params.discountAmount;
  const res = await rootAxios.put(`/bills/updateBill/${billId}/`, body);
  return normalizeBill(res.data);
};

export const updateBillStatus = async (
  billId: number,
  status: "notPayed" | "payed"
) => {
  const res = await rootAxios.put(`/bills/updateBillStatus/${billId}/`, {
    status,
  });
  return normalizeBill(res.data);
};
