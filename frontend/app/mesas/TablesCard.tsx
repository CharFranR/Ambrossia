export enum EstadoMesa {
  Libre,
  Ocupado,
  Reservado,
}

interface TablesCardProps {
  estado: EstadoMesa;
  numero: number;
}

function TablesCard({ estado, numero }: TablesCardProps) {
  let backgroundColor = "";
  let text = "";

  switch (estado) {
    case EstadoMesa.Libre:
      backgroundColor = "green";
      text = "Libre";
      break;
    case EstadoMesa.Ocupado:
      backgroundColor = "red";
      text = "Ocupada";
      break;
    case EstadoMesa.Reservado:
      backgroundColor = "gray";
      text = "Reservada";
      break;
  }

  return (
    <>
      <button
        style={{
          backgroundColor,
          color: "white",
          fontSize: "20px",
          padding: "20px",
          border: "none",
          borderRadius: "10px",
          width: "200px",
          height: "200px",
          cursor: "pointer",
        }}
      >
        <span> Mesa {numero} </span>
        <br />
        <span>{text}</span>
      </button>
    </>
  );
}

export default TablesCard;
