import { useState } from 'react'
import { getAllSolicitudes, updateSolicitudEstado } from '../services/solicitudAdopcionService'
import { getAnimalById, updateAnimal } from '../services/animalService'
import { getUsuarioById } from '../services/authService'
import { createAdopcion } from '../services/adopcionService'

export function SolicitudesRescatistaPage() {
  const [, forceUpdate] = useState(0)
  const solicitudes = getAllSolicitudes()

  function handleAprobar(solicitudId: number, animalId: number) {
    updateSolicitudEstado(solicitudId, 'APROBADA')
    createAdopcion(solicitudId, new Date().toISOString().slice(0, 10))
    updateAnimal(animalId, { estado: 'ADOPTADO' })
    forceUpdate((n) => n + 1)
  }

  function handleRechazar(solicitudId: number) {
    updateSolicitudEstado(solicitudId, 'RECHAZADA')
    forceUpdate((n) => n + 1)
  }

  return (
    <main className="max-w-4xl mx-auto px-6 py-8">
      <h1 className="font-heading font-bold text-3xl text-ink mb-6">Solicitudes de adopción</h1>

      {solicitudes.length === 0 ? (
        <p className="font-body text-sm text-ink/70">Todavía no hay solicitudes.</p>
      ) : (
        <div className="flex flex-col gap-3">
          {solicitudes.map((s) => {
            const animal = getAnimalById(s.animalId)
            const adoptante = getUsuarioById(s.adoptanteId)
            return (
              <div key={s.id} className="bg-surface-muted rounded-xl p-4 flex items-center justify-between gap-4">
                <div>
                  <p className="font-body font-medium text-sm text-ink">
                    {animal?.nombre ?? `Animal #${s.animalId}`} · {adoptante?.nombre ?? `Usuario #${s.adoptanteId}`}
                  </p>
                  <p className="font-body text-xs text-ink/60">{s.tipoVivienda} · {s.motivo}</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-body text-xs font-medium px-3 py-1 rounded-full bg-white text-ink">
                    {s.estado}
                  </span>
                  {s.estado === 'PENDIENTE' && (
                    <>
                      <button onClick={() => handleAprobar(s.id, s.animalId)}
                        className="font-body text-xs text-primary-dark underline">
                        Aprobar
                      </button>
                      <button onClick={() => handleRechazar(s.id)}
                        className="font-body text-xs text-accent">
                        Rechazar
                      </button>
                    </>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </main>
  )
}