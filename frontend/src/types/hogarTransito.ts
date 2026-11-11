export interface HogarTransito {
  id: number
  responsableId: number
  direccion: string
  capacidad: number
  disponible: boolean
  observaciones?: string
}

export interface AsignacionTransito {
  id: number
  animalId: number
  hogarTransitoId: number
  fechaIngreso: string
  fechaSalida?: string
  observaciones?: string
}