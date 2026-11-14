import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line,
} from 'recharts'
import { getAnimalesPorEstado, getSolicitudesPorEstado, getAdopcionesPorMes, getResumenGeneral } from '../services/statsService'

const coloresEstado: Record<string, string> = {
  DISPONIBLE: '#17A79C',
  EN_TRANSITO: '#0B6F68',
  EN_PROCESO_ADOPCION: '#E2574C',
  ADOPTADO: '#16302E',
  INACTIVO: '#9CA3AF',
  PENDIENTE: '#17A79C',
  APROBADA: '#0B6F68',
  RECHAZADA: '#E2574C',
  CANCELADA: '#9CA3AF',
}

const etiquetasEstado: Record<string, string> = {
  DISPONIBLE: 'Disponible',
  EN_TRANSITO: 'En tránsito',
  EN_PROCESO_ADOPCION: 'En proceso',
  ADOPTADO: 'Adoptado',
  INACTIVO: 'Inactivo',
  PENDIENTE: 'Pendiente',
  APROBADA: 'Aprobada',
  RECHAZADA: 'Rechazada',
  CANCELADA: 'Cancelada',
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-surface-muted rounded-xl p-4 text-center">
      <p className="font-heading font-bold text-2xl text-primary-dark">{value}</p>
      <p className="font-body text-xs text-ink/60">{label}</p>
    </div>
  )
}

export function EstadisticasPage() {
  const resumen = getResumenGeneral()
  const animalesPorEstado = getAnimalesPorEstado()
  const solicitudesPorEstado = getSolicitudesPorEstado()
  const adopcionesPorMes = getAdopcionesPorMes()

  return (
    <main className="max-w-5xl mx-auto px-6 py-8">
      <h1 className="font-heading font-bold text-3xl text-ink mb-6">Panel de estadísticas</h1>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
        <StatCard label="Animales" value={resumen.totalAnimales} />
        <StatCard label="Disponibles" value={resumen.disponibles} />
        <StatCard label="Hogares activos" value={resumen.hogaresActivos} />
        <StatCard label="En hogares" value={resumen.animalesEnHogares} />
        <StatCard label="Adopciones" value={resumen.totalAdopciones} />
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <div className="bg-surface-muted rounded-2xl p-4">
          <h2 className="font-heading font-bold text-lg text-ink mb-4">Animales por estado</h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={animalesPorEstado} margin={{ bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E6E7E4" />
              <XAxis
                dataKey="estado"
                tick={{ fontSize: 10 }}
                interval={0}
                angle={-20}
                textAnchor="end"
                tickFormatter={(value) => etiquetasEstado[value] ?? value}
              />
              <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
              <Tooltip labelFormatter={(value) => typeof value === 'string' ? etiquetasEstado[value] ?? value : value }/>
              <Bar dataKey="cantidad">
                {animalesPorEstado.map((entry) => (
                  <Cell key={entry.estado} fill={coloresEstado[entry.estado]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-surface-muted rounded-2xl p-4">
          <h2 className="font-heading font-bold text-lg text-ink mb-4">Solicitudes por estado</h2>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={solicitudesPorEstado} dataKey="cantidad" nameKey="estado" outerRadius={75}>
                {solicitudesPorEstado.map((entry) => (
                  <Cell key={entry.estado} fill={coloresEstado[entry.estado]} />
                ))}
              </Pie>
              <Tooltip formatter={(value, _name, item) => [value, etiquetasEstado[item.payload.estado] ?? item.payload.estado]} />
              <Legend formatter={(value) => etiquetasEstado[value] ?? value} wrapperStyle={{ fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-surface-muted rounded-2xl p-4">
        <h2 className="font-heading font-bold text-lg text-ink mb-4">Adopciones por mes</h2>
        {adopcionesPorMes.length === 0 ? (
            <p className="font-body text-sm text-ink/70">Todavía no hay adopciones registradas.</p>
        ) : (
            <div className="relative pl-8">
            <span
                className="absolute left-0 top-1/2 font-body text-xs text-ink/60 whitespace-nowrap"
                style={{ transform: 'translate(-30%, -50%) rotate(-90deg)' }}
            >
                Cantidad de adopciones
            </span>
            <ResponsiveContainer width="100%" height={260}>
                <LineChart data={adopcionesPorMes} margin={{ top: 5, right: 20, left: 0, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E6E7E4" />
                <XAxis
                    dataKey="mes"
                    tick={{ fontSize: 11 }}
                    label={{ value: 'Fecha', position: 'insideBottom', offset: -10, fontSize: 12 }}
                />
                <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Line type="monotone" dataKey="cantidad" stroke="#17A79C" strokeWidth={2} />
                </LineChart>
            </ResponsiveContainer>
            </div>
        )}
        </div>
    </main>
  )
}