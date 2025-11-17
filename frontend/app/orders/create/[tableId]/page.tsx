'use client';

import { useParams, useRouter } from 'next/navigation';
import { createOrder } from '@/hooks/api/useOrders';
import { useState, useRef } from 'react';
import { toast } from 'sonner';
import InteractiveMenu from '@/app/orders/components/InteractiveMenu';

export default function CreateOrderPage() {
  const router = useRouter();
  const params = useParams();
  const tableId = Array.isArray(params.tableId) ? params.tableId[0] : params.tableId;
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<any>(null);
  const [quantity, setQuantity] = useState(1);
  const [note, setNote] = useState('');
  const popupRef = useRef<HTMLDivElement>(null);

  const createOrderMutation = createOrder();

  const handleAddProduct = (product: any) => {
    setSelectedProduct(product);
    setQuantity(1);
    setNote('');
    setShowPopup(true);
  };

  const handleSendOrder = () => {
    if (!tableId || !selectedProduct) return;
    setIsSubmitting(true);
    createOrderMutation.mutate(
      {
        table: parseInt(tableId as string),
        product: selectedProduct.id,
        quantity,
        note,
        status: 'notCooking',
      },
      {
        onSuccess: () => {
          toast.success('Orden enviada a cocina');
          setIsSubmitting(false);
          setShowPopup(false);
          setSelectedProduct(null);
        },
        onError: () => {
          toast.error('Error al enviar la orden');
          setIsSubmitting(false);
        },
      }
    );
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

  if (!tableId) {
    return <div className="text-center py-10 text-lg text-gray-600">Mesa no seleccionada</div>;
  }

  return (
    <div className="relative flex flex-col gap-8">
      <h1 className="text-2xl font-bold mb-4">Menú Interactivo</h1>
      <InteractiveMenu onAdd={handleAddProduct} />
      {showPopup && (
        <div
          className="fixed inset-0 z-40 flex items-center justify-center bg-black/40"
          onClick={handleOverlayClick}
        >
          <div
            ref={popupRef}
            className="bg-white rounded-lg shadow-lg p-6 min-w-[320px] flex flex-col gap-4 animate-fade-in"
            onClick={e => e.stopPropagation()}
          >
            <div className="flex flex-col gap-2">
              <div className="font-semibold text-lg">{selectedProduct?.name}</div>
              <label className="text-sm font-medium">Cantidad</label>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  className="px-2 py-1 rounded bg-gray-200 hover:bg-gray-300 transition"
                  onClick={() => setQuantity(q => Math.max(1, q - 1))}
                  disabled={quantity <= 1}
                >
                  -
                </button>
                <span className="px-4">{quantity}</span>
                <button
                  type="button"
                  className="px-2 py-1 rounded bg-gray-200 hover:bg-gray-300 transition"
                  onClick={() => setQuantity(q => q + 1)}
                >
                  +
                </button>
              </div>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium">Notas</label>
              <textarea
                value={note}
                onChange={e => setNote(e.target.value)}
                className="border rounded px-2 py-1 min-h-[60px] resize-none"
                placeholder="Agregar notas para cocina (opcional)"
              />
            </div>
            <div className="flex gap-2 justify-end">
              <button
                type="button"
                className="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300 transition"
                onClick={handleCancelPopup}
                disabled={isSubmitting}
              >
                Cancelar
              </button>
              <button
                type="button"
                className="px-4 py-2 rounded bg-sky-600 text-white hover:bg-sky-700 transition"
                onClick={handleSendOrder}
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Enviando...' : 'Enviar a cocina'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}