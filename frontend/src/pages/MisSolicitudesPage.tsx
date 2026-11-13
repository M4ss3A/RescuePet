import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { getSolicitudesByAdoptanteId } from '../services/solicitudAdopcionService'
import { getAnimalById } from '../services/animalService'

export function MisSolicitudesPage() {
  const { usuario } = useAuth()
  const solicitudes = getSolicitudesByAdoptanteId(usuario?.id ?? 0)

  return (
    <main className="max-w-3xl mx-auto px-6 py-8">
      <h1 className="font-heading font-bold text-3xl text-ink mb-6">Mis solicitudes</h1>

      {solicitudes.length === 0 ? (
        <p className="font-body text-sm text-ink/70">
          Todavía no enviaste ninguna solicitud. Mirá el{' '}
          <Link to="/catalogo" className="text-primary-dark underline">catálogo</Link> para empezar.
        </p>
      ) : (
        <div className="flex flex-col gap-3">
          {solicitudes.map((s) => {
            const animal = getAnimalById(s.animalId)
            return (
              <div key={s.id} className="bg-surface-muted rounded-xl p-4 flex items-center justify-between gap-4">
                <div>
                  <p className="font-body font-medium text-sm text-ink">{animal?.nombre ?? `Animal #${s.animalId}`}</p>
                  <p className="font-body text-xs text-ink/60">Enviada el {s.fechaSolicitud}</p>
                </div>
                <span className="font-body text-xs font-medium px-3 py-1 rounded-full bg-white text-ink">
                  {s.estado}
                </span>
              </div>
            )
          })}
        </div>
      )}
    </main>
  )
}