import { useState } from 'react'
import { Link } from 'react-router-dom'
import { getAllAnimales, darDeBajaAnimal } from '../services/animalService'

export function RescatistaDashboardPage() {
  const [, forceUpdate] = useState(0)
  const animales = getAllAnimales()

  function handleBaja(id: number) {
    darDeBajaAnimal(id)
    forceUpdate((n) => n + 1)
  }

  return (
    <main className="max-w-5xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-heading font-bold text-3xl text-ink">Panel del rescatista</h1>
        <div className="flex items-center gap-4">

          <Link to="/rescatista/hogares" className="font-body text-sm text-primary-dark underline">
            Hogares de tránsito
          </Link>

          <Link to="/rescatista/solicitudes" className="font-body text-sm text-primary-dark underline">
            Solicitudes
          </Link>
          
          <Link to="/rescatista/animales/nuevo"
            className="bg-accent text-white rounded-full px-4 py-2 font-body font-medium text-sm">
            + Registrar animal
          </Link>
          
        </div>
      </div>

      <div className="flex flex-col gap-2">
        {animales.map((a) => (
          <div key={a.id} className="bg-surface-muted rounded-xl p-4 flex items-center justify-between gap-4">
            <div>
              <p className="font-body font-medium text-sm text-ink">{a.nombre}</p>
              <p className="font-body text-xs text-ink/60">{a.especie} · {a.estado}</p>
            </div>
            <div className="flex gap-2">
              <Link to={`/rescatista/animales/${a.id}/editar`}
                className="font-body text-xs text-primary-dark underline">
                Editar
              </Link>
              {a.estado !== 'INACTIVO' && (
                <button onClick={() => handleBaja(a.id)} className="font-body text-xs text-accent">
                  Dar de baja
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </main>
  )
}