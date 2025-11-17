"use client"

import InteractiveMenu from "@/app/orders/components/InteractiveMenu";
import { useState } from "react";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";

type OrderFormProps = {
  tableId: string;
  isSubmitting: boolean;
  onCreateOrder: () => void;
  onCancel: () => void;
  onAdd: (product: any) => void;
  category?: string;
  setCategory?: (cat: string) => void;
};

export function ProductCategorySelector({
  category,
  setCategory,
}: {
  category: string | undefined;
  setCategory: (cat: string) => void;
}) {
  return (
    <Select value={category} onValueChange={setCategory}>
      <SelectTrigger className="w-[185px]">
        <SelectValue placeholder="Seleccionar categoría" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Categorías</SelectLabel>
          <SelectItem value="all">Todas</SelectItem>
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
  onAdd,
  category,
  setCategory,
}: OrderFormProps) {
  return (
    <div className="w-full p-4">
      <h1 className="text-2xl font-bold mb-6 text-white">Toma de Orden - Mesa {tableId}</h1>
      <ProductCategorySelector category={category} setCategory={setCategory!} />
      <div>
        <InteractiveMenu onAdd={onAdd} category={category} />
      </div>
    </div>
  );
}
