"use client"

import InteractiveMenu from "@/app/orders/components/InteractiveMenu";
import { Table2, Utensils, SendHorizonal, StickyNote } from "lucide-react";
import {   Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue } from "@/components/ui/select";

type OrderFormProps = {
  tableId: string;
  isSubmitting: boolean;
  onCreateOrder: () => void;
  onCancel: () => void;
};

type OrderFormProducts = {
    id: number;
  name: string;
  price: number;
  notes?: string;
  quantity: number;
};

export function ProductCategorySelector() {
  return (
<Select>
      <SelectTrigger className="w-[185px]">
        <SelectValue placeholder="Seleccionar categoría" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Categorías</SelectLabel>
          <SelectItem value="appetizers">Aperitivos</SelectItem>
          <SelectItem value="main-dishes">Platos principales</SelectItem>
          <SelectItem value="desserts">Postres</SelectItem>
          <SelectItem value="drinks">Bebidas</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}

export function OrderForm({
  tableId,
  isSubmitting,
  onCreateOrder,
  onCancel,
}: OrderFormProps) {
  return (
    <div className="w-full p-4">
        <h1 className="text-2xl font-bold mb-6 text-white">Toma de Orden - Mesa {tableId}</h1>
        <ProductCategorySelector />
        <div>
          <InteractiveMenu />
        </div>
    </div>
  );
}
