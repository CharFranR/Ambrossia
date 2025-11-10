"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  Home,
  Settings,
  Table,
  Menu,
  BarChart,
  CookingPot,
} from "lucide-react";
import Link from "next/link";

export default function Sidebar() {
  const [open, setOpen] = useState(true);

  return (
    <div
      className={`h-screen bg-background border-r transition-all duration-300 ${
        open ? "w-64" : "w-16"
      } flex flex-col`}
    >
      {/* Header */}
      <div className="flex items-center p-4">
        {open && <span className="font-bold text-lg mr-auto">Ambrossia</span>}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setOpen(!open)}
          aria-label="Toggle sidebar"
          className={open ? "ml-auto" : "mx-auto"}
        >
          <Menu size={20} />
        </Button>
      </div>

      <Separator />

      {/* Links */}
      <nav className="flex-1 mt-4 space-y-2">
        <Link
          href="/"
          className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-muted transition-colors"
        >
          <Home size={18} />
          {open && <span>Inicio</span>}
        </Link>
        <Link
          href="/mesas"
          className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-muted transition-colors"
        >
          <Table size={18} />
          {open && <span>Mesas</span>}
        </Link>

        <Link
          href="/cocina"
          className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-muted transition-colors"
        >
          <CookingPot size={18} />
          {open && <span>Cocina</span>}
        </Link>

        <Link
          href="/analytics"
          className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-muted transition-colors"
        >
          <BarChart size={18} />
          {open && <span>Analítica</span>}
        </Link>
        <Link
          href="/settings"
          className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-muted transition-colors"
        >
          <Settings size={18} />
          {open && <span>Configuración</span>}
        </Link>
      </nav>
    </div>
  );
}
