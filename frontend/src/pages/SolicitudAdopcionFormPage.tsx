import { useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { getAnimalById } from '../services/animalService'
import { createSolicitud } from '../services/solicitudAdopcionService'
import type { TipoVivienda } from '../types/solicitudAdopcion'

const tiposVivienda: TipoVivienda[] = ['Casa con patio', 'Casa sin patio', 'Departamento']

export function SolicitudAdopcionFormPage() {
  const { animalId } = useParams<{ animalId: string }>()
  const animal = getAnimalById(Number(animalId))
  const { usuario } = useAuth()
  const navigate = useNavigate()

  const [tipoVivienda, setTipoVivienda] = useState<TipoVivienda>('Casa con patio')
  const [tienePatio, setTienePatio] = useState(false)
  const [tieneOtrosAnimales, setTieneOtrosAnimales] = useState(false)
  const [experienciaPrevia, setExperienciaPrevia] = useState('')
  const [motivo, setMotivo] = useState('')

  if (!animal) {
    return (
      <main className="max-w-xl mx-auto px-6 py-12 text-center">
        <p className="font-body text-ink">No encontramos ese animal.</p>
      </main>
    )
  }

  const solicitudAnimalId = animal.id

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    createSolicitud({
      animalId: solicitudAnimalId,
      adoptanteId: usuario?.id ?? 0,
      tipoVivienda,
      tienePatio,
      tieneOtrosAnimales,
      experienciaPrevia,
      motivo,
    })
    navigate('/mis-solicitudes')
  }

  return (
    <main className="max-w-xl mx-auto px-6 py-10">
      <h1 className="font-heading font-bold text-3xl text-ink mb-2">Solicitud de adopción</h1>
      <p className="font-body text-sm text-ink/70 mb-6">Para {animal.nombre} · {animal.especie}</p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Tipo de vivienda</span>
          <select value={tipoVivienda} onChange={(e) => setTipoVivienda(e.target.value as TipoVivienda)}
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm">
            {tiposVivienda.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>

        <label className="flex items-center gap-2">
          <input type="checkbox" checked={tienePatio} onChange={(e) => setTienePatio(e.target.checked)} />
          <span className="font-body text-sm text-ink">Tengo patio</span>
        </label>

        <label className="flex items-center gap-2">
          <input type="checkbox" checked={tieneOtrosAnimales} onChange={(e) => setTieneOtrosAnimales(e.target.checked)} />
          <span className="font-body text-sm text-ink">Tengo otros animales</span>
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Experiencia previa con animales</span>
          <textarea value={experienciaPrevia} onChange={(e) => setExperienciaPrevia(e.target.value)} rows={3} required minLength={5}
            placeholder="Ej: Tuve un perro durante 8 años, sé de cuidados básicos y rutina de paseos."
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">¿Por qué querés adoptar a {animal.nombre}?</span>
          <textarea value={motivo} onChange={(e) => setMotivo(e.target.value)} required minLength={20} rows={3}
            placeholder="Ej: Me interesa adoptar a este animal porque..."
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <button type="submit"
          className="bg-accent text-white rounded-full px-5 py-2 font-body font-medium text-sm mt-2">
          Enviar solicitud
        </button>
      </form>
    </main>
  )
}