import { useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createSeguimiento } from '../services/seguimientoService'

export function SeguimientoFormPage() {
  const { adopcionId } = useParams<{ adopcionId: string }>()
  const navigate = useNavigate()

  const [fecha, setFecha] = useState(new Date().toISOString().slice(0, 10))
  const [estadoGeneral, setEstadoGeneral] = useState('')
  const [resultado, setResultado] = useState('')
  const [observaciones, setObservaciones] = useState('')

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    createSeguimiento({
      adopcionId: Number(adopcionId),
      fecha,
      estadoGeneral,
      resultado,
      observaciones,
    })
    navigate('/rescatista/seguimientos')
  }

  return (
    <main className="max-w-xl mx-auto px-6 py-10">
      <h1 className="font-heading font-bold text-3xl text-ink mb-6">Nuevo control de seguimiento</h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Fecha</span>
          <input type="date" value={fecha} onChange={(e) => setFecha(e.target.value)} required
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Estado general del animal</span>
          <input value={estadoGeneral} onChange={(e) => setEstadoGeneral(e.target.value)} required minLength={15}
            placeholder="Ej: Saludable, adaptado y feliz"
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Resultado</span>
          <input value={resultado} onChange={(e) => setResultado(e.target.value)} required minLength={8}
            placeholder="Ej: Visita sin novedades, el animal se adaptó bien"
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Observaciones</span>
          <textarea value={observaciones} onChange={(e) => setObservaciones(e.target.value)} rows={3} required minLength={15}
            placeholder="Ej: El animal se mostró activo y contento, sin signos de estrés"
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" 
          />
        </label>

        <button type="submit"
          className="bg-primary text-white rounded-full px-5 py-2 font-body font-medium text-sm mt-2">
          Guardar control
        </button>
      </form>
    </main>
  )
}