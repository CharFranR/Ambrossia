import type { Metadata } from "next";
import Sidebar from "@/components/Sidebar";
import { Providers } from "./providers";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ambrossia",
  description: "Sistema de gestión para restaurantes",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className="flex min-h-screen bg-background text-foreground">
        {/* 🔹 Envolvés todo dentro de Providers */}
        <Providers>
          {/* Sidebar fija */}
          <Sidebar />

          {/* Contenido principal */}
          <main className="flex-1 p-6">{children}</main>
        </Providers>
      </body>
    </html>
  );
}
