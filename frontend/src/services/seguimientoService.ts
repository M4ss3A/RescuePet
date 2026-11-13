import type { Seguimiento } from '../types/seguimiento'

// NOTA: mock en memoria — los cambios se pierden al recargar la pagina.
// Se resuelve en el Hito 5, cuando esto pase a consultar la API real.
const seguimientosMock: Seguimiento[] = []
let nextId = 1

export function createSeguimiento(data: Omit<Seguimiento, 'id'>): Seguimiento {
  const nuevo: Seguimiento = { id: nextId++, ...data }
  seguimientosMock.push(nuevo)
  return nuevo
}

export function getSeguimientosByAdopcionId(adopcionId: number): Seguimiento[] {
  return seguimientosMock.filter((s) => s.adopcionId === adopcionId)
}