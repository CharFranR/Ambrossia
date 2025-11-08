'use client';

import { useState } from "react";
import { Button } from "@/components/ui/button";
import AreaDropdown from "./AreaDropdown";
import { Pencil } from "lucide-react";
import { Table } from "@/types/models";
import { useTables } from "@/hooks/api/useTables";
import TablesCard, { EstadoMesa } from "./TablesCard";
import anime from "animejs";

const useAnimateTables = () => {
  return () => {
    anime({
      targets: ".table-card",
      translateX: anime.random(-20, 20),
      translateY: anime.random(-20, 20),
      easing: "easeInOutSine",
      duration: 400,
      direction: "alternate",
    });
  };
};

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
  const { data: tables, isLoading, error } = useTables();
  const animateShuffle = useAnimateTables();

  if (isLoading) return <div>Cargando mesas...</div>;
  if (error) return <div>Error al cargar mesas: {error.message}</div>;


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
          <div key={table.id} className="table-card">
            <TablesCard
              numero={table.id}
              estado={mapTableStatus(table.status)}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
