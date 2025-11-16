"use client";

import type { Bill } from "@/types/models/bills";
import { useUpdateBill, useUpdateBillStatus } from "@/hooks/api/useBills";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface BillDetailProps {
  bill: Bill | null;
}

export default function BillDetail({ bill }: BillDetailProps) {
  const { mutate: updateBill } = useUpdateBill();
  const { mutate: updateStatus } = useUpdateBillStatus();

  const [ivaPercent, setIvaPercent] = useState<number>(15);
  const [discountPercent, setDiscountPercent] = useState<number>(0);

  if (!bill)
    return (
      <div className="text-gray-500 text-sm">
        Selecciona una factura para ver detalles.
      </div>
    );

  const subtotal = bill.amount;
  const iva = bill.IVA ?? 0;
  const discount = bill.discount ?? 0;
  const total = bill.total ?? 0;

  return (
    <Card className="border shadow-sm">
      <CardHeader className="py-2">
        <CardTitle className="text-base">Factura #{bill.id}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
          <span className="text-gray-600">Subtotal:</span>
          <span className="text-right">{subtotal.toFixed(2)}</span>
          <span className="text-gray-600">IVA:</span>
          <span className="text-right">{iva.toFixed(2)}</span>
          <span className="text-gray-600">Descuento:</span>
          <span className="text-right">{discount.toFixed(2)}</span>
          <span className="font-semibold">Total:</span>
          <span className="text-right font-semibold">{total.toFixed(2)}</span>
          <span className="text-gray-600">Estado:</span>
          <span className="text-right uppercase text-xs tracking-wide">
            {bill.status}
          </span>
        </div>

        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <label className="text-xs text-gray-600">IVA %</label>
            <input
              type="number"
              value={ivaPercent}
              onChange={(e) => setIvaPercent(Number(e.target.value))}
              className="w-20 rounded border px-2 py-1 text-sm bg-background"
            />
            <label className="text-xs text-gray-600">Desc %</label>
            <input
              type="number"
              value={discountPercent}
              onChange={(e) => setDiscountPercent(Number(e.target.value))}
              className="w-20 rounded border px-2 py-1 text-sm bg-background"
            />
            <Button
              size="sm"
              variant="outline"
              onClick={() => {
                // For now we only change IVA using updateBill (discount there expects amount, not %)
                updateBill({
                  billId: bill.id,
                  IVAPercent: ivaPercent,
                  discountAmount: (discountPercent / 100) * subtotal,
                });
              }}
            >
              Actualizar
            </Button>
          </div>
          <Button
            size="sm"
            className="bg-sky-600 hover:bg-sky-700"
            onClick={() => updateStatus({ billId: bill.id, status: "payed" })}
            disabled={bill.status === "payed"}
          >
            {bill.status === "payed" ? "Pagada" : "Marcar como pagada"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
