import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

// CartaOrden: componente visual que muestra la orden de una mesa.
// Recibe props con la mesa, posible mesero, hora y lista de items.
// Conserva el diseño original pero ahora renderiza datos dinámicos.

type Item = {
  productName: string;
  quantity: number;
  note?: string | null;
};

interface CartaOrdenProps {
  mesa: number | string;
  mesero?: string | null;
  hora?: string | null;
  items: Item[];
}

function formatTime(dateString?: string | null) {
  if (!dateString) return "--:--";
  try {
    const d = new Date(dateString);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch (e) {
    return dateString;
  }
}

export default function CartaOrden({
  mesa,
  mesero,
  hora,
  items,
}: CartaOrdenProps) {
  return (
    <Card className="w-64 border border-gray-700 shadow-black bg-gray-800 py-0 rounded-xl">
      <CardHeader className="bg-sky-100 py-2 px-3 rounded-t-xl">
        <CardTitle className="text-base font-semibold text-gray-900">
          Mesa {mesa}
        </CardTitle>

        <div className="text-sm text-gray-500 flex justify-between">
          <span className="text-gray-700">{formatTime(hora)}</span>
          <p>{mesero ?? "-"}</p>
        </div>
      </CardHeader>

      <CardContent className="px-3 pb-7">
        {items.map((it, idx) => (
          <div key={idx} className={idx === 0 ? "" : "mt-3"}>
            <div className="flex justify-between items-center">
              <span className="font-medium">
                {it.quantity} {it.productName}
              </span>
            </div>
            {it.note ? (
              <div className="ml-4 text-sm text-amber-100">
                <p>{it.note}</p>
              </div>
            ) : null}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
