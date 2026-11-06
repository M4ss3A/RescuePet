import { useState, useMemo } from 'react'
import { getAnimalesDisponibles } from '../services/animalService'
import type { Especie, Tamano } from '../types/animal'

const especies: Especie[] = ['Perro', 'Gato', 'Otro']
const tamanos: Tamano[] = ['Pequeño', 'Mediano', 'Grande']

export function CatalogoPage() {
  const [especie, setEspecie] = useState<Especie | 'Todas'>('Todas')
  const [tamano, setTamano] = useState<Tamano | 'Todos'>('Todos')

  const animales = useMemo(() => {
    return getAnimalesDisponibles().filter((a) => {
      if (especie !== 'Todas' && a.especie !== especie) return false
      if (tamano !== 'Todos' && a.tamano !== tamano) return false
      return true
    })
  }, [especie, tamano])

  return (
    <main className="max-w-6xl mx-auto px-6 py-8">
      <h1 className="font-heading font-bold text-3xl text-ink mb-2">Animales en adopción</h1>
      <p className="font-body text-sm text-ink/70 mb-6">
        Conocé a los animales que están buscando una familia.
      </p>

      <div className="flex flex-wrap gap-3 mb-8">
        <select
          value={especie}
          onChange={(e) => setEspecie(e.target.value as Especie | 'Todas')}
          className="border border-surface-muted rounded-full px-4 py-2 font-body text-sm text-ink"
        >
          <option value="Todas">Todas las especies</option>
          {especies.map((e) => (
            <option key={e} value={e}>{e}</option>
          ))}
        </select>

        <select
          value={tamano}
          onChange={(e) => setTamano(e.target.value as Tamano | 'Todos')}
          className="border border-surface-muted rounded-full px-4 py-2 font-body text-sm text-ink"
        >
          <option value="Todos">Todos los tamaños</option>
          {tamanos.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
      </div>

      <p className="font-body text-sm text-ink/70">{animales.length} animales encontrados.</p>
    </main>
  )
}