"use client";

import { useState } from "react";
import { useCreateBill } from "@/hooks/api/useBills";
import { Button } from "@/components/ui/button";

export default function CreateBillForm() {
  const { mutate, isPending } = useCreateBill();
  const [tableId, setTableId] = useState<number | "">("");
  const [discountPercent, setDiscountPercent] = useState<number>(0);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (tableId === "" || isNaN(Number(tableId))) return;
        mutate({ tableId: Number(tableId), discountPercent });
      }}
      className="mb-4 flex flex-wrap items-end gap-3 bg-muted/40 p-3 rounded border"
    >
      <div className="flex flex-col">
        <label className="text-xs text-gray-600 mb-1">Table ID</label>
        <input
          type="number"
          value={tableId}
          onChange={(e) =>
            setTableId(e.target.value === "" ? "" : Number(e.target.value))
          }
          className="w-24 rounded border px-2 py-1 text-sm bg-background"
          placeholder="ID"
        />
      </div>
      <div className="flex flex-col">
        <label className="text-xs text-gray-600 mb-1">Discount %</label>
        <input
          type="number"
          value={discountPercent}
          onChange={(e) => setDiscountPercent(Number(e.target.value))}
          className="w-28 rounded border px-2 py-1 text-sm bg-background"
          placeholder="0"
        />
      </div>
      <Button
        type="submit"
        size="sm"
        disabled={isPending || tableId === ""}
        className="bg-sky-600 hover:bg-sky-700"
      >
        {isPending ? "Creando..." : "Crear factura"}
      </Button>
    </form>
  );
}
