import { useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { createHogar, getHogarById, updateHogar } from '../services/hogarTransitoService'

export function HogarFormPage() {
  const { id } = useParams<{ id: string }>()
  const esEdicion = Boolean(id)
  const hogarExistente = esEdicion ? getHogarById(Number(id)) : undefined
  const { usuario } = useAuth()
  const navigate = useNavigate()

  const [direccion, setDireccion] = useState(hogarExistente?.direccion ?? '')
  const [capacidad, setCapacidad] = useState(hogarExistente?.capacidad ?? 1)
  const [disponible, setDisponible] = useState(hogarExistente?.disponible ?? true)
  const [observaciones, setObservaciones] = useState(hogarExistente?.observaciones ?? '')

  function handleSubmit(e: FormEvent) {
    e.preventDefault()

    if (esEdicion && hogarExistente) {
      updateHogar(hogarExistente.id, { direccion, capacidad, disponible, observaciones })
    } else {
      createHogar({ direccion, capacidad, disponible, observaciones, responsableId: usuario?.id ?? 0 })
    }

    navigate('/rescatista/hogares')
  }

  return (
    <main className="max-w-xl mx-auto px-6 py-10">
      <h1 className="font-heading font-bold text-3xl text-ink mb-6">
        {esEdicion ? 'Editar hogar de tránsito' : 'Registrar hogar de tránsito'}
      </h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Dirección</span>
          <input value={direccion} onChange={(e) => setDireccion(e.target.value)} required minLength={8} 
            placeholder="Ej: Calle Falsa 123, Ciudad, Provincia"
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Capacidad</span>
          <input type="number" min={1} value={capacidad} required
            onChange={(e) => setCapacidad(Number(e.target.value))} 
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <label className="flex items-center gap-2">
          <input type="checkbox" checked={disponible} onChange={(e) => setDisponible(e.target.checked)} />
          <span className="font-body text-sm text-ink">Disponible para recibir animales</span>
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Observaciones</span>
          <textarea value={observaciones} onChange={(e) => setObservaciones(e.target.value)} rows={3} required minLength={15}
            placeholder="Ej: Casa amplia, donde ya viven mascotas que se llevan bien con nuevos animales, familia responsable y comprometida"
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <button type="submit"
          className="bg-primary text-white rounded-full px-5 py-2 font-body font-medium text-sm mt-2">
          {esEdicion ? 'Guardar cambios' : 'Registrar hogar'}
        </button>
      </form>
    </main>
  )
}