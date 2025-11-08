import { MdTableRestaurant } from "react-icons/md";

export enum EstadoMesa {
  Libre,
  Ocupado,
  Reservado,
  Limpiando,
}

interface TablesCardProps {
  estado: EstadoMesa;
  numero: number;
}

function TablesCard({ estado, numero }: TablesCardProps) {
  let bgColor = "";
  let textColor = "";
  let text = "";

  switch (estado) {
    case EstadoMesa.Libre:
      bgColor = "bg-green-50 border border-3 border-green-500/50";
      textColor = "text-green-700";
      text = "Libre";
      break;
    case EstadoMesa.Ocupado:
      bgColor = "bg-red-50 border border-3 border-red-500/50";
      textColor = "text-red-700";
      text = "Ocupada";
      break;
    case EstadoMesa.Reservado:
      bgColor = "bg-gray-50 border border-3 border-gray-500/50";
      textColor = "text-gray-700";
      text = "Reservada";
      break;
    case EstadoMesa.Limpiando:
      bgColor = "bg-yellow-50 border border-3 border-yellow-500/50";
      textColor = "text-yellow-700";
      text = "Limpiando";
      break;
  }

  return (
    <button
      className={`${bgColor} ${textColor} flex flex-col items-center justify-center gap-2 p-5 rounded-xl w-40 h-40 hover:scale-105 hover:cursor-pointer transition-transform`}
    >
      <MdTableRestaurant className="text-5xl" />
      <span className="font-bold text-lg">Mesa {numero}</span>
      <span className="capitalize">{text}</span>
    </button>
  );
}

export default TablesCard;
