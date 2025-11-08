import { Bill } from "./bills";
import { Product } from "./products";
import { Table } from "./tables";

export type OrderStatus = "notCooking" | "cooking" | "ready";

export interface Order {
  id: number;
  table: Table | number | null;  // depende si DRF devuelve el objeto o solo el ID
  product: Product | number;
  quantity: number;
  bill: Bill | number | null;
  status: OrderStatus;
  created_at: string;
  closed_at: string | null;
  note: string;
}