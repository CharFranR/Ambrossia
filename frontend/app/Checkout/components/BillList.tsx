"use client";

import { useOpenBills } from "@/hooks/api/useBills";
import type { Bill } from "@/types/models/bills";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface BillListProps {
  onSelect: (bill: Bill) => void;
  selectedId?: number | null;
}

export default function BillList({ onSelect, selectedId }: BillListProps) {
  const { data, isLoading, isError } = useOpenBills();

  if (isLoading)
    return <div className="text-center py-4">Cargando facturas...</div>;
  if (isError)
    return <div className="text-center py-4 text-red-500">Error al cargar</div>;

  const bills = data ?? [];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {bills.map((b) => (
        <Card
          key={b.id}
          className={`border shadow-sm transition hover:shadow-md cursor-pointer ${
            selectedId === b.id ? "ring-2 ring-sky-500" : ""
          }`}
          onClick={() => onSelect(b)}
        >
          <CardHeader className="py-2">
            <CardTitle className="text-sm font-semibold flex justify-between">
              <span>Bill #{b.id}</span>
              <span className="text-xs font-normal text-gray-500">
                {new Date(b.created_at).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span>Subtotal:</span>
              <span>{b.amount.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span>IVA:</span>
              <span>{(b.IVA ?? 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span>Desc:</span>
              <span>{(b.discount ?? 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between font-semibold">
              <span>Total:</span>
              <span>{(b.total ?? 0).toFixed(2)}</span>
            </div>
            <Button variant="outline" size="sm" className="mt-2 w-full">
              Seleccionar
            </Button>
          </CardContent>
        </Card>
      ))}
      {bills.length === 0 && (
        <div className="col-span-full text-center text-gray-500">
          No hay facturas abiertas
        </div>
      )}
    </div>
  );
}
