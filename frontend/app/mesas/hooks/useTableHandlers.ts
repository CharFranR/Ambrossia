// useTableHandlers.ts
import { useRouter } from "next/navigation";

export const useTableHandlers = () => {
  const router = useRouter();

  const takeOrder = (tableId: number) => {
    // Ruta dinámica
    router.push(`/orders/create/${tableId}`);
  };

  const closeBill = (tableId: number) => {
    router.push(`/bills/${tableId}`);
  };

  const reserve = (tableId: number) => {
    router.push(`/tables/${tableId}/reserve`);
  };

  return { takeOrder, closeBill, reserve };
};
