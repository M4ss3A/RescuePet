import { useState } from 'react'
import { Link } from 'react-router-dom'
import { getAllHogares, getAsignacionesActivasByHogarId, createAsignacion } from '../services/hogarTransitoService'
import { getAllAnimales, getAnimalById } from '../services/animalService'

export function HogaresTransitoPage() {
  const [, forceUpdate] = useState(0)
  const [seleccion, setSeleccion] = useState<Record<number, string>>({})
  const hogares = getAllHogares()
  const animalesEnTransito = getAllAnimales().filter((a) => a.estado === 'EN_TRANSITO')

  function animalesDisponibles() {
    const idsAsignados = new Set(
      hogares.flatMap((h) => getAsignacionesActivasByHogarId(h.id).map((a) => a.animalId))
    )
    return animalesEnTransito.filter((a) => !idsAsignados.has(a.id))
  }

  function handleAsignar(hogarId: number) {
    const animalId = Number(seleccion[hogarId])
    if (!animalId) return
    createAsignacion({
      animalId,
      hogarTransitoId: hogarId,
      fechaIngreso: new Date().toISOString().slice(0, 10),
    })
    setSeleccion((prev) => ({ ...prev, [hogarId]: '' }))
    forceUpdate((n) => n + 1)
  }

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
          const disponibles = animalesDisponibles()
          const hayLugar = asignaciones.length < h.capacidad

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

              {hayLugar && disponibles.length > 0 && (
                <div className="mt-3 flex items-center gap-2">
                  <select
                    value={seleccion[h.id] ?? ''}
                    onChange={(e) => setSeleccion((prev) => ({ ...prev, [h.id]: e.target.value }))}
                    className="border border-surface-muted rounded-lg px-2 py-1 font-body text-xs bg-white"
                  >
                    <option value="">Asignar animal en tránsito...</option>
                    {disponibles.map((a) => (
                      <option key={a.id} value={a.id}>{a.nombre}</option>
                    ))}
                  </select>
                  <button onClick={() => handleAsignar(h.id)} className="font-body text-xs text-primary-dark underline">
                    Asignar
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </main>
  )
}