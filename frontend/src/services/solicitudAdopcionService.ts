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

export function getAllSolicitudes(): SolicitudAdopcion[] {
  return solicitudesMock
}

export function getSolicitudById(id: number): SolicitudAdopcion | undefined {
  return solicitudesMock.find((s) => s.id === id)
}

export function updateSolicitudEstado(
  id: number,
  estado: SolicitudAdopcion['estado']
): SolicitudAdopcion | undefined {
  const solicitud = solicitudesMock.find((s) => s.id === id)
  if (!solicitud) return undefined
  solicitud.estado = estado
  return solicitud
}