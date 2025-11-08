export type BillStatus = "notPayed" | "payed";

export interface Bill {
  id: number;
  status: BillStatus;
  created_at: string;   // ISO date string (ej. "2025-11-08T15:32:00Z")
  closed_at: string | null;
  amount: number;       // subtotal o monto base
  IVA: number | null;   // puede venir null según tu modelo
  discount: number | null;
  total: number | null;
}