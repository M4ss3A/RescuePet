import { createContext, useContext, useState, type ReactNode } from 'react'
import type { Usuario } from '../types/auth'
import { login as loginService } from '../services/authService'

interface AuthContextValue {
  usuario: Usuario | null
  isAuthenticated: boolean
  login: (email: string, password: string) => boolean
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null)

  const login = (email: string, password: string) => {
    const encontrado = loginService(email, password)
    if (!encontrado) return false
    setUsuario(encontrado)
    return true
  }

  const logout = () => setUsuario(null)

  return (
    <AuthContext.Provider value={{ usuario, isAuthenticated: usuario !== null, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth debe usarse dentro de un AuthProvider')
  return context
}