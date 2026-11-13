import { Link, useParams } from 'react-router-dom'
import { getAdopcionBySolicitudId } from '../services/adopcionService'
import { getSolicitudById } from '../services/solicitudAdopcionService'
import { getAnimalById } from '../services/animalService'

export function AdopcionConfirmacionPage() {
  const { solicitudId } = useParams<{ solicitudId: string }>()
  const adopcion = getAdopcionBySolicitudId(Number(solicitudId))
  const solicitud = getSolicitudById(Number(solicitudId))
  const animal = solicitud ? getAnimalById(solicitud.animalId) : undefined

  if (!adopcion || !solicitud || !animal) {
    return (
      <main className="max-w-xl mx-auto px-6 py-12 text-center">
        <p className="font-body text-ink">Todavía no hay una adopción registrada para esta solicitud.</p>
        <Link to="/mis-solicitudes" className="font-body text-primary-dark underline">Volver a mis solicitudes</Link>
      </main>
    )
  }

  return (
    <main className="max-w-xl mx-auto px-6 py-12 text-center">
      <div className="bg-gradient-to-br from-primary to-primary-dark rounded-2xl p-8 text-white">
        <p className="font-body text-xs opacity-85 mb-2">¡Felicitaciones!</p>
        <h1 className="font-heading font-bold text-3xl mb-2">Adoptaste a {animal.nombre}</h1>
        <p className="font-body text-sm opacity-90">Fecha de adopción: {adopcion.fechaAdopcion}</p>
      </div>
      <p className="font-body text-sm text-ink/70 mt-6">
        Estado: {adopcion.estado === 'EN_SEGUIMIENTO' ? 'En seguimiento' : 'Finalizada'}
      </p>
      <Link to="/mis-solicitudes" className="font-body text-sm text-primary-dark underline mt-4 inline-block">
        Volver a mis solicitudes
      </Link>
    </main>
  )
}