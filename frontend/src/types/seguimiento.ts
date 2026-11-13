export interface Seguimiento {
  id: number
  adopcionId: number
  fecha: string
  observaciones?: string
  estadoGeneral?: string
  resultado?: string
}