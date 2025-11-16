"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import AreaDropdown from "./components/AreaDropdown";
import TableOptionsModal from "./components/TableOptionModal";
import TablesCard, { EstadoMesa } from "./components/TableCard";

import { Pencil } from "lucide-react";
import { Table } from "@/types/models";
import { useTables, useCreateTable } from "@/hooks/api/useTables";
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
  const {
    mutate: createTable,
    isPending: creating,
    data: lastCreated,
  } = useCreateTable() as any;
  const animateShuffle = useAnimateTables();

  const { takeOrder, closeBill, reserve } = useTableHandlers();
  useAnimateTables();

  // No cortar el render para poder mostrar botón de creación aunque falle fetch
  const loadingState = isLoading;
  const errorState = error as any;

  return (
    <div className="flex flex-col gap-5 text-center p-6">
      <h1 className="text-2xl font-bold">Mesas</h1>

      <div className="flex justify-between items-center">
        <AreaDropdown area={area} setArea={setArea} onAction={animateShuffle} />
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={animateShuffle}>
            Editar
            <Pencil className="h-4 w-4 ml-1" />
            <span className="sr-only">Editar</span>
          </Button>
          <Button
            size="sm"
            className="bg-sky-600 hover:bg-sky-700"
            disabled={creating}
            onClick={() => createTable()}
          >
            {creating ? "Creando..." : "Nueva mesa"}
          </Button>
        </div>
      </div>

      <div className="mt-4">
        {loadingState && (
          <div className="text-sm text-gray-500 mb-3">Cargando mesas...</div>
        )}
        {errorState && !loadingState && (
          <div className="text-sm text-red-500 mb-3">
            Error al cargar mesas: {errorState.message || "Network"}
          </div>
        )}
        {!loadingState && !errorState && tables?.length === 0 && (
          <div className="text-sm text-gray-500 mb-3">
            No hay mesas todavía. Crea la primera.
          </div>
        )}
        {lastCreated && (
          <div className="text-xs text-green-600 mb-2">
            Mesa creada ID {lastCreated.id}
          </div>
        )}
        <div className="flex flex-wrap justify-center gap-5">
          {tables?.map((table: Table) => (
            <div
              key={table.id}
              className="table-card"
              onClick={() => setSelectedTable(table)}
            >
              <TablesCard
                numero={table.id}
                estado={mapTableStatus(table.status)}
              />
            </div>
          ))}
        </div>
      </div>

      {selectedTable && (
        <TableOptionsModal
          table={selectedTable}
          open={!!selectedTable}
          onOpenChange={(open) => !open && setSelectedTable(null)}
          onTakeOrder={(id) => takeOrder(id)}
          onCloseBill={(id) => console.log("Cerrar cuenta mesa", id)}
          onReserve={(id) => console.log("Reservar mesa", id)}
        />
      )}
    </div>
  );
}
