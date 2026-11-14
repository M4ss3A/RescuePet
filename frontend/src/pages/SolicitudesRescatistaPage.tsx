import { useState } from 'react'
import { getAllSolicitudes, updateSolicitudEstado } from '../services/solicitudAdopcionService'
import { getAnimalById, updateAnimal } from '../services/animalService'
import { getUsuarioById } from '../services/authService'
import { createAdopcion } from '../services/adopcionService'
import { finalizarAsignacion } from '../services/hogarTransitoService'

export function SolicitudesRescatistaPage() {
  const [, forceUpdate] = useState(0)
  const solicitudes = getAllSolicitudes()

  function handleAprobar(solicitudId: number, animalId: number) {
    updateSolicitudEstado(solicitudId, 'APROBADA')
    createAdopcion(solicitudId, new Date().toISOString().slice(0, 10))
    updateAnimal(animalId, { estado: 'ADOPTADO' })
    finalizarAsignacion(animalId, new Date().toISOString().slice(0, 10))
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
              <div key={s.id} className="bg-surface-muted rounded-xl p-4">
                <div className="flex items-center justify-between gap-4">
                  <p className="font-body font-medium text-sm text-ink">
                    {animal?.nombre ?? `Animal #${s.animalId}`} · {adoptante?.nombre ?? `Usuario #${s.adoptanteId}`}
                  </p>
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

                <dl className="mt-3 grid grid-cols-2 gap-x-4 gap-y-2">
                  <div>
                    <dt className="font-body text-xs text-ink/50">Tipo de vivienda</dt>
                    <dd className="font-body text-xs text-ink">{s.tipoVivienda}</dd>
                  </div>
                  <div>
                    <dt className="font-body text-xs text-ink/50">Fecha de solicitud</dt>
                    <dd className="font-body text-xs text-ink">{s.fechaSolicitud}</dd>
                  </div>
                  <div>
                    <dt className="font-body text-xs text-ink/50">¿Tiene patio?</dt>
                    <dd className="font-body text-xs text-ink">{s.tienePatio ? 'Sí' : 'No'}</dd>
                  </div>
                  <div>
                    <dt className="font-body text-xs text-ink/50">¿Tiene otros animales?</dt>
                    <dd className="font-body text-xs text-ink">{s.tieneOtrosAnimales ? 'Sí' : 'No'}</dd>
                  </div>
                  <div className="col-span-2">
                    <dt className="font-body text-xs text-ink/50">Experiencia previa</dt>
                    <dd className="font-body text-xs text-ink">{s.experienciaPrevia || '—'}</dd>
                  </div>
                  <div className="col-span-2">
                    <dt className="font-body text-xs text-ink/50">Motivo</dt>
                    <dd className="font-body text-xs text-ink">{s.motivo}</dd>
                  </div>
                </dl>
              </div>
            )
          })}
        </div>
      )}
    </main>
  )
}