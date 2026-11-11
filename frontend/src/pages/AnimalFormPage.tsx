import { useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { createAnimal, getAnimalById, updateAnimal } from '../services/animalService'
import { createRescate, getRescateByAnimalId } from '../services/rescateService'
import type { Especie, Tamano, EstadoAnimal } from '../types/animal'

const especies: Especie[] = ['Perro', 'Gato', 'Otro']
const tamanos: Tamano[] = ['Pequeño', 'Mediano', 'Grande']
const estados: EstadoAnimal[] = ['EN_TRANSITO', 'DISPONIBLE', 'EN_PROCESO_ADOPCION', 'ADOPTADO', 'INACTIVO']

export function AnimalFormPage() {
  const { id } = useParams<{ id: string }>()
  const esEdicion = Boolean(id)
  const animalExistente = esEdicion ? getAnimalById(Number(id)) : undefined
  const rescateExistente = esEdicion ? getRescateByAnimalId(Number(id)) : undefined
  const { usuario } = useAuth()
  const navigate = useNavigate()

  const [nombre, setNombre] = useState(animalExistente?.nombre ?? '')
  const [especie, setEspecie] = useState<Especie>(animalExistente?.especie ?? 'Perro')
  const [raza, setRaza] = useState(animalExistente?.raza ?? '')
  const [edadAproximada, setEdadAproximada] = useState(animalExistente?.edadAproximada ?? 1)
  const [tamano, setTamano] = useState<Tamano>(animalExistente?.tamano ?? 'Mediano')
  const [descripcion, setDescripcion] = useState(animalExistente?.descripcion ?? '')
  const [ubicacion, setUbicacion] = useState(rescateExistente?.ubicacion ?? '')
  const [fechaRescate, setFechaRescate] = useState(rescateExistente?.fechaRescate ?? '')
  const [estado, setEstado] = useState<EstadoAnimal>(animalExistente?.estado ?? 'EN_TRANSITO')

  function handleSubmit(e: FormEvent) {
    e.preventDefault()

    if (esEdicion && animalExistente) {
  updateAnimal(animalExistente.id, { nombre, especie, raza, edadAproximada, tamano, descripcion, estado })
    } else {
      const nuevo = createAnimal({
        nombre, especie, raza, edadAproximada, tamano, descripcion,
        estado: 'EN_TRANSITO',
        fotoUrl: `https://placehold.co/400x300/17A79C/white?text=${encodeURIComponent(nombre)}`,
      })
      createRescate({
        animalId: nuevo.id,
        rescatistaId: usuario?.id ?? 0,
        ubicacion,
        fechaRescate,
      })
    }

    navigate('/rescatista')
  }

  return (
    <main className="max-w-xl mx-auto px-6 py-10">
      <h1 className="font-heading font-bold text-3xl text-ink mb-6">
        {esEdicion ? 'Editar animal' : 'Registrar animal rescatado'}
      </h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Nombre</span>
          <input value={nombre} onChange={(e) => setNombre(e.target.value)} required
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <div className="flex gap-4">
          <label className="flex flex-col gap-1 flex-1">
            <span className="font-body text-sm text-ink">Especie</span>
            <select value={especie} onChange={(e) => setEspecie(e.target.value as Especie)}
              className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm">
              {especies.map((e) => <option key={e} value={e}>{e}</option>)}
            </select>
          </label>

          <label className="flex flex-col gap-1 flex-1">
            <span className="font-body text-sm text-ink">Tamaño</span>
            <select value={tamano} onChange={(e) => setTamano(e.target.value as Tamano)}
              className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm">
              {tamanos.map((t) => <option key={t} value={t}>{t}</option>)}
            </select>
          </label>
        </div>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Raza</span>
          <input value={raza} onChange={(e) => setRaza(e.target.value)}
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Edad aproximada (años)</span>
          <input type="number" min={0} value={edadAproximada}
            onChange={(e) => setEdadAproximada(Number(e.target.value))}
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Descripción</span>
          <textarea value={descripcion} onChange={(e) => setDescripcion(e.target.value)} rows={3}
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
        </label>

        {!esEdicion && (
          <>
            <label className="flex flex-col gap-1">
              <span className="font-body text-sm text-ink">Ubicación del rescate</span>
              <input value={ubicacion} onChange={(e) => setUbicacion(e.target.value)} required
                className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
            </label>

            <label className="flex flex-col gap-1">
              <span className="font-body text-sm text-ink">Fecha del rescate</span>
              <input type="date" value={fechaRescate} onChange={(e) => setFechaRescate(e.target.value)} required
                className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm" />
            </label>
          </>
        )}

        {esEdicion && (
            <label className="flex flex-col gap-1">
                <span className="font-body text-sm text-ink">Estado</span>
                <select value={estado} onChange={(e) => setEstado(e.target.value as EstadoAnimal)}
                className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm">
                {estados.map((e) => <option key={e} value={e}>{e}</option>)}
                </select>
            </label>
        )}

        <button type="submit"
          className="bg-primary text-white rounded-full px-5 py-2 font-body font-medium text-sm mt-2">
          {esEdicion ? 'Guardar cambios' : 'Registrar animal'}
        </button>
      </form>
    </main>
  )
}