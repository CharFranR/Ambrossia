'use client';

import { useParams, useRouter } from 'next/navigation';
import { createOrder } from '@/hooks/api/useOrders';
import { useState } from 'react';
import { toast } from 'sonner';
import { OrderForm } from '@/app/orders/components/OrderForm';

export default function CreateOrderPage() {
  const router = useRouter();
  const params = useParams();
  const tableId = Array.isArray(params.tableId) ? params.tableId[0] : params.tableId;
  const [isSubmitting, setIsSubmitting] = useState(false);

  const createOrderMutation = createOrder();

  const handleCreateOrder = () => {
    if (!tableId) return;
    
    setIsSubmitting(true);
    createOrderMutation.mutate({ 
      table: parseInt(tableId as string),
      status: 'notCooking',
    });
  };

  if (!tableId) {
    return <div>Mesa no seleccionada</div>;
  }

  return (
    <OrderForm 
      tableId={tableId}
      isSubmitting={isSubmitting}
      onCreateOrder={handleCreateOrder}
      onCancel={() => router.push('/tables')}
    />
  );
}