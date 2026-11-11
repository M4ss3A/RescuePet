import { Link } from 'react-router-dom'
import { getAllHogares, getAsignacionesActivasByHogarId } from '../services/hogarTransitoService'
import { getAnimalById } from '../services/animalService'

export function HogaresTransitoPage() {
  const hogares = getAllHogares()

  return (
    <main className="max-w-5xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-heading font-bold text-3xl text-ink">Hogares de tránsito</h1>
        <Link to="/rescatista/hogares/nuevo"
          className="bg-accent text-white rounded-full px-4 py-2 font-body font-medium text-sm">
          + Registrar hogar
        </Link>
      </div>

      <div className="flex flex-col gap-3">
        {hogares.map((h) => {
          const asignaciones = getAsignacionesActivasByHogarId(h.id)
          return (
            <div key={h.id} className="bg-surface-muted rounded-xl p-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="font-body font-medium text-sm text-ink">{h.direccion}</p>
                  <p className="font-body text-xs text-ink/60">
                    {asignaciones.length}/{h.capacidad} ocupados · {h.disponible ? 'Disponible' : 'No disponible'}
                  </p>
                </div>
                <Link to={`/rescatista/hogares/${h.id}/editar`} className="font-body text-xs text-primary-dark underline">
                  Editar
                </Link>
              </div>

              {asignaciones.length > 0 && (
                <ul className="mt-3 flex flex-wrap gap-2">
                  {asignaciones.map((a) => {
                    const animal = getAnimalById(a.animalId)
                    return (
                      <li key={a.id} className="font-body text-xs bg-white rounded-full px-3 py-1 text-ink">
                        {animal?.nombre ?? `Animal #${a.animalId}`}
                      </li>
                    )
                  })}
                </ul>
              )}
            </div>
          )
        })}
      </div>
    </main>
  )
}