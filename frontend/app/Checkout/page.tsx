"use client";

import { useState } from "react";
import BillList from "./components/BillList";
import BillDetail from "./components/BillDetail";
import type { Bill } from "@/types/models/bills";
import { Separator } from "@/components/ui/separator";
import CreateBillForm from "./components/CreateBillForm";

export default function CheckoutPage() {
  const [selected, setSelected] = useState<Bill | null>(null);

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Checkout</h1>
      <div className="flex flex-col lg:flex-row gap-8">
        <div className="flex-1">
          <h2 className="text-lg font-semibold mb-3">Facturas abiertas</h2>
          <CreateBillForm />
          <BillList onSelect={setSelected} selectedId={selected?.id ?? null} />
        </div>
        <Separator orientation="vertical" className="hidden lg:block" />
        <div className="w-full lg:w-80 xl:w-96">
          <h2 className="text-lg font-semibold mb-3">Detalle</h2>
          <BillDetail bill={selected} />
        </div>
      </div>
    </div>
  );
}
