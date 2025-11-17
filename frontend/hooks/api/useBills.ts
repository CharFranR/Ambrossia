import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import * as billService from "@/services/billService";
import type { Bill } from "@/types/models/bills";

export const useOpenBills = () => {
  return useQuery<Bill[]>({
    queryKey: ["bills", "open"],
    queryFn: billService.getNotPayedBills,
  });
};

export const usePayedBills = () => {
  return useQuery<Bill[]>({
    queryKey: ["bills", "payed"],
    queryFn: billService.getPayedBills,
  });
};

export const useCreateBill = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      tableId,
      discountPercent,
    }: {
      tableId: number;
      discountPercent?: number;
    }) => billService.createBill(tableId, { discountPercent }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["bills", "open"] });
    },
  });
};

export const useUpdateBill = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      billId,
      IVAPercent,
      discountAmount,
    }: {
      billId: number;
      IVAPercent?: number;
      discountAmount?: number;
    }) => billService.updateBill(billId, { IVAPercent, discountAmount }),
    onSuccess: () => {
      qc.invalidateQueries();
    },
  });
};

export const useUpdateBillStatus = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      billId,
      status,
    }: {
      billId: number;
      status: "notPayed" | "payed";
    }) => billService.updateBillStatus(billId, status),
    onSuccess: () => {
      qc.invalidateQueries();
    },
  });
};
