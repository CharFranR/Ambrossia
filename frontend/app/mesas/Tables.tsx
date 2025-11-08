'use client';

import TablesCard, { EstadoMesa } from "./TablesCard";
import { Card } from "@/components/ui/card";
import { useTables } from "@/hooks/api/useTables";

// Función para mapear los estados de la API a tu enum EstadoMesa
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

export default function Tables() {
  const { data: tables, isLoading, error } = useTables();

  if (isLoading) return <div>Cargando mesas...</div>;
  if (error) return <div>Error al cargar mesas: {error.message}</div>;

  return (
    <div className="flex flex-wrap justify-center gap-5 p-10">
      {tables?.map((table) => (
        <Card key={table.id}>
          <TablesCard
            numero={table.id}
            estado={mapTableStatus(table.status)}
          />
        </Card>
      ))}
    </div>
  );
}
