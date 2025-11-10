import TablesCard, { EstadoMesa } from "./TablesCard";
import { Card } from "@/components/ui/card";
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
      <Card variant="outline">
        <TablesCard numero={1} estado={EstadoMesa.Libre} />
      </Card>
      <Card variant="outline">
        <TablesCard numero={2} estado={EstadoMesa.Ocupado} />
      </Card>
      <Card variant="outline">
        <TablesCard numero={3} estado={EstadoMesa.Reservado} />
      </Card>
      <Card variant="outline">
        <TablesCard numero={4} estado={EstadoMesa.Libre} />
      </Card>
      <Card variant="outline">
        <TablesCard numero={5} estado={EstadoMesa.Libre} />
      </Card>
      <Card variant="outline">
        <TablesCard numero={6} estado={EstadoMesa.Libre} />
      </Card>
      <Card variant="outline">
        <TablesCard numero={7} estado={EstadoMesa.Ocupado} />
      </Card>
    </div>
  );
}

export default Tables;
