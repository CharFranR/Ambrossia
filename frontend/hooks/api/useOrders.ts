import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import * as orderService from "@/services/orderService";

export const useOrders = () => {
  return useQuery({
    queryKey: ["orders"],
    queryFn: orderService.getOrders,
  });
};

export const createOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: orderService.createOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orders"] });
    },
  });
};
