export type EstadoSolicitud = 'PENDIENTE' | 'APROBADA' | 'RECHAZADA' | 'CANCELADA'
export type TipoVivienda = 'Casa con patio' | 'Casa sin patio' | 'Departamento'

export interface SolicitudAdopcion {
  id: number
  animalId: number
  adoptanteId: number
  fechaSolicitud: string
  estado: EstadoSolicitud
  tipoVivienda: TipoVivienda
  tienePatio: boolean
  tieneOtrosAnimales: boolean
  experienciaPrevia: string
  motivo: string
  puntajeCompatibilidad?: number
}