import TablesCard, { EstadoMesa } from "./TablesCard";

function Tables() {
  return (
    <div
      style={{
        padding: "40px", // separación del borde del contenedor
        display: "flex",
        gap: "20px", // separación entre botones
        flexWrap: "wrap", // permite que se acomoden si no caben
        justifyContent: "center",
      }}
    >
      <TablesCard numero={1} estado={EstadoMesa.Libre} />
      <TablesCard numero={2} estado={EstadoMesa.Ocupado} />
      <TablesCard numero={3} estado={EstadoMesa.Reservado} />
      <TablesCard numero={4} estado={EstadoMesa.Libre} />
      <TablesCard numero={5} estado={EstadoMesa.Libre} />
      <TablesCard numero={6} estado={EstadoMesa.Libre} />
      <TablesCard numero={7} estado={EstadoMesa.Ocupado} />
    </div>
  );
}

export default Tables;
