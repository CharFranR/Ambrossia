'use client';

import { useParams, useRouter } from 'next/navigation';
import { createOrder } from '@/hooks/api/useOrders';
import { useState, useRef } from 'react';
import { toast } from 'sonner';
import InteractiveMenu from '@/app/orders/components/InteractiveMenu';
import { ProductCategorySelector } from '@/app/orders/components/OrderForm';
import { Button } from '@/components/ui/button';

export default function CreateOrderPage() {
  const router = useRouter();
  const params = useParams();
  const tableId = Array.isArray(params.tableId) ? params.tableId[0] : params.tableId;
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<any>(null);
  const [quantity, setQuantity] = useState(1);
  const [note, setNote] = useState('');
  const [category, setCategory] = useState<string>('');
  const [orderItems, setOrderItems] = useState<any[]>([]);
  const [showSent, setShowSent] = useState(false);
  const popupRef = useRef<HTMLDivElement>(null);

  const createOrderMutation = createOrder();

  const handleAddProduct = (product: any) => {
    setSelectedProduct(product);
    setQuantity(1);
    setNote('');
    setShowPopup(true);
  };

  const handleAddToList = () => {
    if (!selectedProduct) return;
    setOrderItems([
      ...orderItems,
      {
        product: selectedProduct,
        quantity,
        note,
      },
    ]);
    setShowPopup(false);
    setSelectedProduct(null);
    setQuantity(1);
    setNote('');
  };

  const handleSendOrder = () => {
    if (!tableId || orderItems.length === 0) return;
    setIsSubmitting(true);

    Promise.all(
      orderItems.map(item =>
        createOrderMutation.mutateAsync({
          table: parseInt(tableId as string),
          product: item.product.id,
          quantity: item.quantity,
          note: item.note,
          status: 'notCooking',
        })
      )
    )
      .then(() => {
        setIsSubmitting(false);
        setOrderItems([]);
        setShowSent(true);
      })
      .catch(() => {
        toast.error('Error al enviar la orden');
        setIsSubmitting(false);
      });
  };

  const handleCancelPopup = () => {
    setShowPopup(false);
    setSelectedProduct(null);
    setQuantity(1);
    setNote('');
  };

  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (popupRef.current && !popupRef.current.contains(e.target as Node)) {
      handleCancelPopup();
    }
  };

  const handleContinue = () => {
    setShowSent(false);
  };

  if (!tableId) {
    return <div className="text-center py-10 text-lg text-gray-600">Mesa no seleccionada</div>;
  }

  return (
    <div className="relative flex flex-col gap-8">
      <h1 className="text-2xl font-bold mb-4 text-foreground">Toma de Orden - Mesa {tableId}</h1>
      <div className="flex flex-col md:flex-row gap-6">
        <div className="flex-1">
          <div className="mb-4">
            <ProductCategorySelector category={category} setCategory={setCategory} />
          </div>
          <InteractiveMenu onAdd={handleAddProduct} category={category} />
        </div>
        <div className="w-full md:w-96 bg-background rounded-xl shadow p-4 flex flex-col gap-4">
          <h2 className="text-lg font-semibold text-foreground">Orden actual</h2>
          {orderItems.length === 0 ? (
            <div className="text-gray-500 text-sm">No hay productos agregados.</div>
          ) : (
            <ul className="divide-y divide-muted">
              {orderItems.map((item, idx) => (
                <li key={idx} className="py-2 flex flex-col gap-1">
                  <span className="font-medium text-foreground">{item.product.name} x{item.quantity}</span>
                  {item.note && <span className="text-xs text-muted-foreground">Nota: {item.note}</span>}
                </li>
              ))}
            </ul>
          )}
          <Button
            className="w-full bg-sky-600 hover:bg-sky-700 text-white"
            onClick={handleSendOrder}
            disabled={isSubmitting || orderItems.length === 0}
          >
            {isSubmitting ? 'Enviando...' : 'Enviar a cocina'}
          </Button>
        </div>
      </div>
      {showPopup && (
        <div
          className="fixed inset-0 z-40 flex items-center justify-center bg-black/40"
          onClick={handleOverlayClick}
        >
          <div
            ref={popupRef}
            className="bg-background rounded-lg shadow-lg p-6 min-w-[320px] flex flex-col gap-4"
            onClick={e => e.stopPropagation()}
          >
            <div className="flex flex-col gap-2">
              <div className="font-semibold text-lg text-foreground">{selectedProduct?.name}</div>
              <label className="text-sm font-medium text-foreground">Cantidad</label>
              <div className="flex items-center gap-2">
                <Button
                  type="button"
                  variant="outline"
                  className="px-2 py-1"
                  onClick={() => setQuantity(q => Math.max(1, q - 1))}
                  disabled={quantity <= 1}
                >
                  -
                </Button>
                <span className="px-4">{quantity}</span>
                <Button
                  type="button"
                  variant="outline"
                  className="px-2 py-1"
                  onClick={() => setQuantity(q => q + 1)}
                >
                  +
                </Button>
              </div>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-foreground">Notas</label>
              <textarea
                value={note}
                onChange={e => setNote(e.target.value)}
                className="border rounded px-2 py-1 min-h-[60px] resize-none bg-background text-foreground"
                placeholder="Agregar notas para cocina (opcional)"
              />
            </div>
            <div className="flex gap-2 justify-end">
              <Button
                type="button"
                variant="outline"
                className="px-4 py-2"
                onClick={handleCancelPopup}
                disabled={isSubmitting}
              >
                Cancelar
              </Button>
              <Button
                type="button"
                className="px-4 py-2 bg-sky-600 text-white hover:bg-sky-700"
                onClick={handleAddToList}
                disabled={isSubmitting}
              >
                Agregar
              </Button>
            </div>
          </div>
        </div>
      )}
      {showSent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-background rounded-lg shadow-lg p-8 flex flex-col items-center gap-4">
            <span className="text-xl font-semibold text-foreground">¡Orden enviada a cocina!</span>
            <Button className="bg-sky-600 text-white hover:bg-sky-700" onClick={handleContinue}>
              Continuar
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}