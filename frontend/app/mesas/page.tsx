'use client';

import {motion} from "framer-motion";
import {useState} from 'react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger , DropdownMenuItem} from "@radix-ui/react-dropdown-menu";
import { Card, CardTitle, CardDescription} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import anime from 'animejs';
import { Pencil } from "lucide-react";

type TableStatus = "libre"| "ocupada" | "reservada"; 

interface Table {
  name: string;
  id: number;
  status: TableStatus;
}

export default function TablesPage() {
  const [area, setArea] = useState("0");
  const tables: Table[] = [
    { name: "Mesa 1", id: 1, status: "libre" },
    { name: "Mesa 2", id: 2, status: "ocupada" },
    { name: "Mesa 3", id: 3, status: "reservada" },
    { name: "Mesa 4", id: 4, status: "libre" },
    { name: "Mesa 5", id: 5, status: "libre" },
    { name: "Mesa 6", id: 6, status: "libre" },
    { name: "Mesa 7", id: 7, status: "ocupada" },
    { name: "Mesa 8", id: 8, status: "reservada"},
    { name: "Mesa 9", id: 9, status: "libre"},
    { name: "Mesa 10", id: 10, status: "ocupada"},
    { name: "Mesa 11", id: 11, status: "reservada"},
    { name: "Mesa 12", id: 12, status: "libre"},
    { name: "Mesa 13", id: 13, status: "ocupada"},
    { name: "Mesa 14", id: 14, status: "reservada"},
    { name: "Mesa 15", id: 15, status: "libre"},
    { name: "Mesa 16", id: 16, status: "ocupada"},
    { name: "Mesa 17", id: 17, status: "reservada"},
    { name: "Mesa 18", id: 18, status: "libre"},
    { name: "Mesa 19", id: 19, status: "ocupada"},
    { name: "Mesa 20", id: 20, status: "reservada"},
    
  ];

  const getColor = (status: TableStatus) => {
    switch (status) {
      case "libre":
        return "bg-green-500";
      case "ocupada":
        return "bg-red-500";
      case "reservada":
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
        <DropdownMenuContent className="z-50 rounded-md shadow-lg p-2">
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
      {tables.map((table) => (
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
            <CardTitle className="text-lg text-center">{table.name}</CardTitle>
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
