import { Link } from 'react-router-dom'
import type { Animal } from '../types/animal'

export function AnimalCard({ animal }: { animal: Animal }) {
  return (
    <div className="bg-surface-muted rounded-2xl overflow-hidden flex flex-col">
      <img src={animal.fotoUrl} alt={animal.nombre} className="w-full h-44 object-cover" />
      <div className="p-4 flex flex-col flex-1">
        <h2 className="font-heading font-bold text-lg text-ink">{animal.nombre}</h2>
        <p className="font-body text-sm text-ink/70 mb-1">
          {animal.especie} · {animal.raza} · {animal.edadAproximada} años
        </p>
        <p className="font-body text-sm text-ink/60 mb-4 flex-1">{animal.descripcion}</p>
        <Link
          to={`/catalogo/${animal.id}`}
          className="self-start bg-accent text-white rounded-full px-4 py-2 font-body font-medium text-sm"
        >
          Ver ficha
        </Link>
      </div>
    </div>
  )
}