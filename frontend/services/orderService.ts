import axios from "@/lib/axios"; // configuración base (baseURL, headers, etc.)
import { Order, OrderStatus} from "@/types/models";

export const getOrders = async (): Promise<Order[]> => {
  const res = await axios.get("/orders/");
  return res.data;
};

export const updateOrderStatus = async (id: number, status: OrderStatus) => {
  const res = await axios.patch(`/orders/${id}/status/`, { status });
  return res.data;
};

export const createOrder = async (orderData: Partial<Order>) => {
  const res = await axios.post("/orders/", orderData);
  return res.data;
};