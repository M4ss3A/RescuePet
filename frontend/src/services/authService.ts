import type { Usuario, Rol } from '../types/auth'

const usuariosMock: (Usuario & { password: string })[] = [
  { id: 1, nombre: 'Ana Rescatista', email: 'rescatista@rescuepet.com', password: '1234', roles: ['RESCATISTA'] },
  { id: 2, nombre: 'Juan Adoptante', email: 'adoptante@rescuepet.com', password: '1234', roles: ['ADOPTANTE'] },
  { id: 3, nombre: 'María Admin', email: 'admin@rescuepet.com', password: '1234', roles: ['ADMINISTRADOR'] },
]

export function login(email: string, password: string): Usuario | null {
  const encontrado = usuariosMock.find((u) => u.email === email && u.password === password)
  if (!encontrado) return null
  const { password: _password, ...usuario } = encontrado
  return usuario
}

export function register(nombre: string, email: string, password: string, rol: Rol): Usuario {
  const nuevo: Usuario & { password: string } = {
    id: usuariosMock.length + 1,
    nombre,
    email,
    password,
    roles: [rol],
  }
  usuariosMock.push(nuevo)
  const { password: _password, ...usuario } = nuevo
  return usuario
}