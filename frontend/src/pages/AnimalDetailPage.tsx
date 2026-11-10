import { Link, useParams } from 'react-router-dom'
import { getAnimalById } from '../services/animalService'
import { getHistorialSaludByAnimalId } from '../services/historialSaludService'

export function AnimalDetailPage() {
  const { id } = useParams<{ id: string }>()
  const animal = getAnimalById(Number(id))

  if (!animal) {
    return (
      <main className="max-w-3xl mx-auto px-6 py-12 text-center">
        <p className="font-body text-ink">No encontramos ese animal.</p>
        <Link to="/catalogo" className="font-body text-primary-dark underline">
          Volver al catálogo
        </Link>
      </main>
    )
  }

  const historial = getHistorialSaludByAnimalId(animal.id)

  return (
    <main className="max-w-4xl mx-auto px-6 py-8">
      <Link to="/catalogo" className="font-body text-sm text-primary-dark mb-4 inline-block">
        ← Volver al catálogo
      </Link>

      <div className="grid md:grid-cols-2 gap-8">
        <img
          src={animal.fotoUrl}
          alt={animal.nombre}
          className="w-full h-72 object-cover rounded-2xl"
        />

        <div>
          <h1 className="font-heading font-bold text-3xl text-ink mb-1">{animal.nombre}</h1>
          <p className="font-body text-sm text-ink/70 mb-4">
            {animal.especie} · {animal.raza} · {animal.tamano} · {animal.edadAproximada} años
          </p>
          <p className="font-body text-sm text-ink/80 mb-6">{animal.descripcion}</p>

          <Link
            to={`/solicitudes/nueva/${animal.id}`}
            className="inline-block bg-accent text-white rounded-full px-5 py-2 font-body font-medium text-sm"
          >
            Quiero adoptar
          </Link>
        </div>
      </div>

      <section className="mt-10">
        <h2 className="font-heading font-bold text-xl text-ink mb-4">Historial de salud</h2>
        {historial.length === 0 ? (
          <p className="font-body text-sm text-ink/60">Todavía no hay registros sanitarios cargados.</p>
        ) : (
          <ul className="flex flex-col gap-3">
            {historial.map((r) => (
              <li key={r.id} className="bg-surface-muted rounded-xl p-4 flex justify-between items-start gap-4">
                <div>
                  <p className="font-body font-medium text-sm text-ink">{r.tipo} — {r.descripcion}</p>
                  {r.veterinario && (
                    <p className="font-body text-xs text-ink/60 mt-1">{r.veterinario}</p>
                  )}
                </div>
                <span className="font-body text-xs text-ink/60 whitespace-nowrap">{r.fecha}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  )
}