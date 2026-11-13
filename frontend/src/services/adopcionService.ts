import type { Adopcion } from '../types/adopcion'

// NOTA: mock en memoria — los cambios se pierden al recargar la pagina.
// Se resuelve en el Hito 5, cuando esto pase a consultar la API 
const adopcionesMock: Adopcion[] = []
let nextId = 1

export function createAdopcion(solicitudId: number, fechaAdopcion: string): Adopcion {
  const nueva: Adopcion = { id: nextId++, solicitudId, fechaAdopcion, estado: 'EN_SEGUIMIENTO' }
  adopcionesMock.push(nueva)
  return nueva
}

export function getAdopcionBySolicitudId(solicitudId: number): Adopcion | undefined {
  return adopcionesMock.find((a) => a.solicitudId === solicitudId)
}