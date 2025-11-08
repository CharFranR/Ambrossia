export type TableStatus =
  | "available"
  | "occupied"
  | "reserved"
  | "in_cleaning";

export interface Table {
  id: number;
  status: TableStatus;
}