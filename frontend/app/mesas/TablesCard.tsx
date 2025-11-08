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
  let text = "";

  switch (estado) {
    case EstadoMesa.Libre:
      bgColor = "bg-green-500";
      text = "Libre";
      break;
    case EstadoMesa.Ocupado:
      bgColor = "bg-red-500";
      text = "Ocupada";
      break;
    case EstadoMesa.Reservado:
      bgColor = "bg-gray-500";
      text = "Reservada";
      break;
    case EstadoMesa.Limpiando:
      bgColor = "bg-yellow-500";
      text = "Limpiando";
      break;
  }

  return (
    <button
      className={`${bgColor} text-white flex flex-col items-center justify-center gap-2 p-5 rounded-xl w-40 h-40 hover:scale-105 transition-transform`}
    >
      <MdTableRestaurant className="text-5xl" />
      <span className="font-bold text-lg">Mesa {numero}</span>
      <span className="capitalize">{text}</span>
    </button>
  );
}

export default TablesCard;
