"use client";
import { LineChart as ReLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

export type LineChartProps = {
  /** Array de objetos con los datos a graficar */
  data: Array<Record<string, any>>;
  /** Clave del eje X (por defecto 'name') */
  xKey?: string;
  /** Líneas a mostrar: array de { key, color, label? } */
  lines: Array<{
    key: string;
    color?: string;
    label?: string;
    activeDot?: object;
  }>;
  /** Opciones de margen */
  margin?: { top?: number; right?: number; left?: number; bottom?: number };
  /** Estilo CSS */
  style?: React.CSSProperties;
  /** Altura máxima (px o %), por defecto '70vh' */
  maxHeight?: string | number;
  /** Mostrar leyenda */
  showLegend?: boolean;
};

export default function LineChart({
  data,
  xKey = 'name',
  lines,
  margin = { top: 5, right: 0, left: 0, bottom: 5 },
  style,
  maxHeight = '70vh',
  showLegend = true,
}: LineChartProps) {
  return (
    <div style={{ width: '100%', maxWidth: 700, height: '100%', maxHeight, aspectRatio: 1.618, ...style }}>
      <ReLineChart
        width={700}
        height={400}
        data={data}
        margin={margin}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={xKey} />
        <YAxis width="auto" />
        <Tooltip />
        {showLegend && <Legend />}
        {lines.map((line, idx) => (
          <Line
            key={line.key}
            type="monotone"
            dataKey={line.key}
            stroke={line.color || (idx === 0 ? '#8884d8' : '#82ca9d')}
            name={line.label || line.key}
            activeDot={line.activeDot}
          />
        ))}
      </ReLineChart>
    </div>
  );
}
