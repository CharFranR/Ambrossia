'use client';

import * as Dialog from '@radix-ui/react-dialog';
import { Button } from '@/components/ui/button';
import { Table } from '@/types/models';

interface TableOptionsModalProps {
  table: Table;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onTakeOrder: (tableId: number) => void;
  onCloseBill: (tableId: number) => void;
  onReserve?: (tableId: number) => void;
}

export default function TableOptionsModal({
  table,
  open,
  onOpenChange,
  onTakeOrder,
  onCloseBill,
  onReserve,
}: TableOptionsModalProps) {
  const { status } = table;

  const buttonClasses = {
    takeOrder: 'bg-green-600 hover:bg-green-700 text-white',
    closeBill: 'bg-red-600 hover:bg-red-700 text-white',
    reserve: 'bg-blue-600 hover:bg-blue-700 text-white',
    cancel: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
  };

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg shadow-lg w-80">
          <Dialog.Title className="text-lg font-bold mb-4 text-black">
            Mesa {table.id}
          </Dialog.Title>

          <div className="flex flex-col gap-3 justify-center">
            {(status === 'available' || status === 'reserved' || status === 'occupied') && (
              <Button className={buttonClasses.takeOrder} onClick={() => onTakeOrder(table.id)}>
                Tomar Orden
              </Button>
            )}

            {(status === 'occupied' || status === 'reserved') && (
              <Button className={buttonClasses.closeBill} onClick={() => onCloseBill(table.id)}>
                Cerrar Cuenta
              </Button>
            )}

            {status === 'available' && onReserve && (
              <Button className={buttonClasses.reserve} onClick={() => onReserve(table.id)}>
                Reservar Mesa
              </Button>
            )}
          </div>

          <Dialog.Close asChild>
            <Button className={`mt-4 w-full ${buttonClasses.cancel}`} onClick={() => onOpenChange(false)}>
              Cancelar
            </Button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
