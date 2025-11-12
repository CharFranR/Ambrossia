'use client';

import { useState } from "react";
import { Button } from "@/components/ui/button";
import AreaDropdown from "./components/AreaDropdown";
import TableOptionsModal from "./components/TableOptionModal";
import TablesCard, { EstadoMesa } from "./components/TableCard";

import { Pencil } from "lucide-react";
import { Table } from "@/types/models";
import { useTables } from "@/hooks/api/useTables";
import { useAnimateTables, useTableHandlers } from "./hooks";



const mapTableStatus = (status: string): EstadoMesa => {
  switch (status) {
    case "available":
      return EstadoMesa.Libre;
    case "occupied":
      return EstadoMesa.Ocupado;
    case "reserved":
      return EstadoMesa.Reservado;
    case "in_cleaning":
      return EstadoMesa.Limpiando;
    default:
      return EstadoMesa.Libre;
  }
};

export default function TablesPage() {
  const [area, setArea] = useState("0");
  const [selectedTable, setSelectedTable] = useState<Table | null>(null);
  const { data: tables, isLoading, error } = useTables();
  const animateShuffle = useAnimateTables();

  const { takeOrder, closeBill, reserve } = useTableHandlers();
  useAnimateTables();

  if (isLoading) return <div className="flex justify-center mt-6"> <div className="p-6 text-center">Cargando mesas...</div></div>;
  if (error) return <div className="flex justify-center mt-6">Error al cargar mesas: {error.message}</div>;

  return (
    <div className="flex flex-col gap-5 text-center p-6">
      <h1 className="text-2xl font-bold">Mesas</h1>

      <div className="flex justify-between items-center">
        <AreaDropdown area={area} setArea={setArea} onAction={animateShuffle} />
        <Button variant="outline" size="sm" onClick={animateShuffle}>
          Editar
          <Pencil className="h-4 w-4 ml-1" />
          <span className="sr-only">Editar</span>
        </Button>
      </div>

      <div className="flex flex-wrap justify-center gap-5 mt-4">
      {tables?.map((table: Table) => (
        <div
          key={table.id}
          className="table-card"
          onClick={() => setSelectedTable(table)} // al click, se abre el modal
        >
          <TablesCard
            numero={table.id}
            estado={mapTableStatus(table.status)}
          />
        </div>
      ))}
    </div>

    {selectedTable && (
      <TableOptionsModal
        table={selectedTable}
        open={!!selectedTable}
        onOpenChange={(open) => !open && setSelectedTable(null)}
        onTakeOrder={(id) => takeOrder(id)}
        onCloseBill={(id) => console.log('Cerrar cuenta mesa', id)}
        onReserve={(id) => console.log('Reservar mesa', id)}
      />
    )}

    </div>
  );
}
