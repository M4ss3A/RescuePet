import { useState } from 'react'
import type { Usuario } from '../types/auth'

// TODO (Hito 2): reemplazar por el estado real de autenticación (login/JWT)
export function useAuth() {
  const [usuario] = useState<Usuario | null>(null)
  return { usuario, isAuthenticated: usuario !== null }
}