import type { Rescate } from '../types/animal'

// NOTA: mock en memoria — los cambios (alta/edicion/baja) se pierden al recargar
// la pagina. Se resuelve en el Hito 5, cuando esto pase a consultar la API real.
const rescatesMock: Rescate[] = [
  { id: 1, animalId: 1, rescatistaId: 1, fechaRescate: '2026-02-01', ubicacion: 'Córdoba Capital', descripcion: 'Encontrado en la vía pública.' },
  { id: 2, animalId: 2, rescatistaId: 1, fechaRescate: '2026-03-15', ubicacion: 'Villa Allende', descripcion: 'Entregado por vecinos.' },
]

let nextId = rescatesMock.length + 1

export function getRescateByAnimalId(animalId: number): Rescate | undefined {
  return rescatesMock.find((r) => r.animalId === animalId)
}

export function createRescate(data: Omit<Rescate, 'id'>): Rescate {
  const nuevo: Rescate = { id: nextId++, ...data }
  rescatesMock.push(nuevo)
  return nuevo
}