import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

type OrderFormProps = {
  tableId: string;
  isSubmitting: boolean;
  onCreateOrder: () => void;
  onCancel: () => void;
};

export function OrderForm({
  tableId,
  isSubmitting,
  onCreateOrder,
  onCancel,
}: OrderFormProps) {
  return (
    <div className="w-full p-4">
      <div className="max-w-md mx-auto bg-black p-6 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-white">Tomar Orden - Mesa {tableId}</h1>
        
        <div className="flex flex-col gap-4">
          <div className="flex justify-end gap-4 pt-4">
            <Button variant="outline" onClick={onCancel}>
              Cancelar
            </Button>
            <Button onClick={onCreateOrder} disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Creando...
                </>
              ) : (
                "Crear Orden"
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
