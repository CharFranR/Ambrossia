"use client";

// Vista de cocina — componente cliente
// Este componente usa react-query (useOrders) y por eso debe ejecutarse en
// el cliente. Next.js en el directorio `app/` crea componentes server por
// defecto. La directiva "use client" arriba obliga a que este módulo se
// renderice en el cliente y así podemos invocar hooks como useQuery.
import OrderCard from "./OrderCard";
import { useOrders } from "@/hooks/api/useOrders";
import type { Order } from "@/types/models/orders";

export default function KitchenView() {
  const { data: orders, isLoading, isError } = useOrders();
  console.log("KitchenView orders:", orders);

  if (isLoading)
    return <div className="p-6 text-center">Cargando órdenes...</div>;
  if (isError)
    return (
      <div className="p-6 text-center text-red-500">
        Error al cargar órdenes
      </div>
    );

  const allOrders: Order[] = orders ?? [];

  // Filtrar órdenes relevantes para cocina (no-ready)
  const openOrders = allOrders.filter((o) => o.status !== "ready");

  // Agrupar órdenes por id de mesa
  const groups = new Map<number | string, Order[]>();
  openOrders.forEach((o) => {
    const tableId =
      typeof o.table === "number"
        ? o.table
        : (o.table && (o.table as any).id) ?? "-";
    const key = tableId ?? "-";
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(o);
  });

  const cards = Array.from(groups.entries()).map(
    ([tableId, ordersForTable]) => {
      // Agregar/combinar productos por id de producto
      const productMap = new Map<
        number | string,
        { productName: string; quantity: number; notes: string[] }
      >();
      
      ordersForTable.forEach((o) => {
        const pid =
          typeof o.product === "number"
            ? o.product
            : (o.product as any)?.id ?? "p" + Math.random();
        const pname =
          typeof o.product === "number"
            ? `Producto #${pid}`
            : (o.product as any)?.name ?? `Producto #${pid}`;
        const existing = productMap.get(pid);
        if (existing) {
          existing.quantity += o.quantity ?? 1;
          if (o.note) existing.notes.push(o.note);
        } else {
          productMap.set(pid, {
            productName: pname,
            quantity: o.quantity ?? 1,
            notes: o.note ? [o.note] : [],
          });
        }
      });

      const items = Array.from(productMap.values()).map((v) => ({
        productName: v.productName,
        quantity: v.quantity,
        note: v.notes.join(", "),
      }));

      // hora de creación más temprana entre las órdenes de la mesa
      const hora =
        ordersForTable.reduce(
          (acc, cur) => (acc.created_at < cur.created_at ? acc : cur),
          ordersForTable[0]
        )?.created_at ?? null;
      // no existe campo 'mesero' en el modelo Order; mostrar guion
      const mesero = "-";

      return (
        <div key={String(tableId)} className="shrink-0">
          <OrderCard
            table={tableId}
            waiter={mesero}
            time={hora}
            items={items}
          />
        </div>
      );
    }
  );

  return (
    <div className="p-4">
      {cards.length === 0 ? (
        <div className="text-center text-gray-500">
          No hay órdenes pendientes
        </div>
      ) : (
        <div className="flex flex-wrap gap-4 justify-center mt-6">{cards}</div>
      )}
    </div>
  );
}
