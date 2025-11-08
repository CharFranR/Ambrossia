'use client';

import { useParams } from 'next/navigation';
import { createOrder } from '@/hooks/api/useOrders';

export default function CreateOrderPage() {
  const params = useParams();
  const tableId = params.tableId;

  if (!tableId) return <div>Mesa no seleccionada</div>;

  const createOrderMutation = createOrder();

  return (
    <div>
      <h1>Tomar Orden para la Mesa {tableId}</h1>
      <button
        onClick={() =>
          createOrderMutation.mutate({ table: parseInt(tableId as string) })
        }
      >
        Crear Orden
      </button>
    </div>
  );
}
