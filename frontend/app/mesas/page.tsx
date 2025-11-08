'use client';

import {motion} from "framer-motion";
import {useState} from 'react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger , DropdownMenuItem} from "@radix-ui/react-dropdown-menu";
import { Card, CardTitle, CardDescription} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import anime from 'animejs';
import { Pencil } from "lucide-react";
import { Table, TableStatus } from "@/types/models";
import { useTables } from "@/hooks/api/useTables";

export default function TablesPage() {
  const [area, setArea] = useState("0");
  const { data: tables, isLoading, error } = useTables();

  if (isLoading) {
    return <div>Cargando tablas...</div>;
  }

  if (error) {
    return <div>Error al cargar tablas: {error.message}</div>;
  }

  const getColor = (status: TableStatus) => {
    switch (status) {
      case "available":
        return "bg-green-500";
      case "occupied":
        return "bg-red-500";
      case "reserved":
        return "bg-gray-500";
    }
  };

  const animateShuffle = (area: string) => {
    anime({
      targets : ".table-card",
      translateX: anime.random(-20, 20),
      translateY: anime.random(-20, 20),
      easing: "easeInOutSine",
      duration: 400,
      direction: "alternate",
    });
  };

  return (
    <div className="flex flex-col gap-5 justify-between text-center">
      <h1 className="text-2xl font-bold">Mesas</h1>
      <div className = "flex justify-between">
      <div className="flex justify-start">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" size="lg" onClick={() => animateShuffle(area)}>
            Área: {area}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel>
            <Button variant="item" size="lg" onClick={() => setArea("1")}>
              Área: 1
            </Button>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuLabel>
            <Button variant="item" size="lg" onClick={() => setArea("2")}>
              Área: 2
            </Button>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuLabel>
            <Button variant="item" size="lg" onClick={() => setArea("3")}>
              Área: 3
            </Button>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuLabel>
            <Button variant="item" size="lg" onClick={() => setArea("4")}>
              Área: 4
            </Button>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuLabel>
            <Button variant="item" size="lg" onClick={() => setArea("5")}>
              Área: 5
            </Button>
          </DropdownMenuLabel>
        </DropdownMenuContent>
      </DropdownMenu>
      </div>
      <div className="flex justify-end">
      <Button variant="outline" size="sm" onClick={() => animateShuffle(area)}>
        Editar
        <Pencil className="h-4 w-4" />
        <span className="sr-only">Editar</span>
      </Button>
      </div>
      </div>
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      {tables?.map((table) => (
        <motion.div
          key={table.id}
          className={`table-card ${getColor(table.status)} rounded-xl`}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          whileHover={{ scale: 1.05 }}
          transition={{ duration: 0.3 }}
          onClick={() => animateShuffle(area)}
        >
          <Card className="h-full p-6 text-white shadow-md">
            <CardTitle className="text-lg text-center">{table.id}</CardTitle>
            <CardDescription className="text-center capitalize">
              {table.status}
            </CardDescription>
          </Card>
        </motion.div>
      ))}
    </div>
  </div>
  );
}
