import LineChart from "@/components/LineChart";


export default function AnalyticsPage() {
  return (
    <div>
      <h1 className="text-center font-bold text-2xl">Página de Analítica</h1>
      <p className="text-center">Aquí puedes ver las estadísticas y análisis de tu restaurante.</p>
      <div className="justify-center flex mt-6">
        <LineChart
        data={[1, 2, 3, 4, 5].map((i) => ({ name: `Día ${i}`, visits: Math.floor(Math.random() * 100), orders: Math.floor(Math.random() * 50) }))}
        xKey="name"
        lines={[
          { key: 'visits', label: 'Visitas', color: '#8884d8' },
          { key: 'orders', label: 'Órdenes', color: '#82ca9d' },
        ]}
      />
      </div>
      
    </div>
  );
}
