import type { SolicitudAdopcion } from '../types/solicitudAdopcion'

// NOTA: mock en memoria — los cambios se pierden al recargar la pagina.
// Se resuelve en el Hito 5, cuando esto pase a consultar la API real.
const solicitudesMock: SolicitudAdopcion[] = []

let nextId = 1

export function createSolicitud(
  data: Omit<SolicitudAdopcion, 'id' | 'fechaSolicitud' | 'estado'>
): SolicitudAdopcion {
  const nueva: SolicitudAdopcion = {
    id: nextId++,
    fechaSolicitud: new Date().toISOString().slice(0, 10),
    estado: 'PENDIENTE',
    ...data,
  }
  solicitudesMock.push(nueva)
  return nueva
}

export function getSolicitudesByAdoptanteId(adoptanteId: number): SolicitudAdopcion[] {
  return solicitudesMock.filter((s) => s.adoptanteId === adoptanteId)
}