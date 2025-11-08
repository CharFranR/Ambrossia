import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import * as tablesService from "@/services/tablesService";

export const useTables = () => {
  return useQuery({
    queryKey: ["tables"],
    queryFn: tablesService.getTables,
  });
};

