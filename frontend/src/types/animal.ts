export type Especie = 'Perro' | 'Gato' | 'Otro'
export type Tamano = 'Pequeño' | 'Mediano' | 'Grande'
export type EstadoAnimal = 'DISPONIBLE' | 'EN_TRANSITO' | 'EN_PROCESO_ADOPCION' | 'ADOPTADO'

export interface Animal {
  id: number
  nombre: string
  especie: Especie
  raza: string
  edadAproximada: number
  tamano: Tamano
  descripcion: string
  estado: EstadoAnimal
  fotoUrl: string
}

export interface RegistroSalud {
  id: number
  tipo: 'VACUNA' | 'TRATAMIENTO' | 'CONSULTA'
  fecha: string
  descripcion: string
  veterinario?: string
}