import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import * as tablesService from "@/services/tableService";

export const useTables = () => {
  return useQuery({
    queryKey: ["tables"],
    queryFn: tablesService.getTables,
  });
};

export const useCreateTable = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: tablesService.createTable,
    onSuccess: (newTable) => {
      // Optimistic merge: insertar nueva mesa al cache antes del refetch
      qc.setQueryData(["tables"], (old: any) => {
        if (!old) return [newTable];
        // evitar duplicado por refetch posterior
        if (old.find((t: any) => t.id === newTable.id)) return old;
        return [...old, newTable];
      });
      // Disparar refetch para sincronizar
      qc.invalidateQueries({ queryKey: ["tables"] });
    },
    onError: (err) => {
      console.error("createTable error", err);
    },
  });
};
