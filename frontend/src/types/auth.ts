export type Rol = 'ADMINISTRADOR' | 'RESCATISTA' | 'HOGAR_TRANSITO' | 'ADOPTANTE'

export interface Usuario {
  id: number
  nombre: string
  email: string
  roles: Rol[]
}