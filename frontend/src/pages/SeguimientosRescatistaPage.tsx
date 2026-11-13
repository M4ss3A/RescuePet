import { Link } from 'react-router-dom'
import { getAllAdopciones } from '../services/adopcionService'
import { getSolicitudById } from '../services/solicitudAdopcionService'
import { getAnimalById } from '../services/animalService'
import { getUsuarioById } from '../services/authService'
import { getSeguimientosByAdopcionId } from '../services/seguimientoService'

export function SeguimientosRescatistaPage() {
  const adopciones = getAllAdopciones()

  return (
    <main className="max-w-4xl mx-auto px-6 py-8">
      <h1 className="font-heading font-bold text-3xl text-ink mb-6">Seguimiento post-adopción</h1>

      {adopciones.length === 0 ? (
        <p className="font-body text-sm text-ink/70">Todavía no hay adopciones registradas.</p>
      ) : (
        <div className="flex flex-col gap-4">
          {adopciones.map((a) => {
            const solicitud = getSolicitudById(a.solicitudId)
            const animal = solicitud ? getAnimalById(solicitud.animalId) : undefined
            const adoptante = solicitud ? getUsuarioById(solicitud.adoptanteId) : undefined
            const seguimientos = getSeguimientosByAdopcionId(a.id)

            return (
              <div key={a.id} className="bg-surface-muted rounded-xl p-4">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-body font-medium text-sm text-ink">
                      {animal?.nombre ?? `Animal #${solicitud?.animalId}`} · {adoptante?.nombre ?? '—'}
                    </p>
                    <p className="font-body text-xs text-ink/60">
                      Adoptado el {a.fechaAdopcion} · {a.estado === 'EN_SEGUIMIENTO' ? 'En seguimiento' : 'Finalizada'}
                    </p>
                  </div>
                  <Link to={`/rescatista/adopciones/${a.id}/seguimiento/nuevo`}
                    className="font-body text-xs text-primary-dark underline">
                    + Agregar control
                  </Link>
                </div>

                {seguimientos.length > 0 && (
                  <ul className="mt-3 flex flex-col gap-2">
                    {seguimientos.map((s) => (
                      <li key={s.id} className="bg-white rounded-lg p-3">
                        <div className="flex items-center justify-between gap-2">
                            <p className="font-body text-xs text-ink">{s.fecha}</p>
                            {s.estadoGeneral && (
                            <span className="font-body text-xs font-medium px-2 py-0.5 rounded-full bg-surface-muted text-ink">
                                {s.estadoGeneral}
                            </span>
                            )}
                        </div>
                        <p className="font-body text-xs text-ink mt-1">{s.resultado ?? 'Sin resultado cargado'}</p>
                        {s.observaciones && (
                            <p className="font-body text-xs text-ink/60 mt-1">{s.observaciones}</p>
                        )}
                        </li>
                    ))}
                  </ul>
                )}
              </div>
            )
          })}
        </div>
      )}
    </main>
  )
}