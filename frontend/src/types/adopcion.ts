export type EstadoAdopcion = 'EN_SEGUIMIENTO' | 'FINALIZADA'

export interface Adopcion {
  id: number
  solicitudId: number
  fechaAdopcion: string
  estado: EstadoAdopcion
  observaciones?: string
}