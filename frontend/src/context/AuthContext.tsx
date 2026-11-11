import { createContext, useContext, useState, type ReactNode } from 'react'
import type { Usuario } from '../types/auth'
import { login as loginService } from '../services/authService'

const STORAGE_KEY = 'rescuepet_usuario'

interface AuthContextValue {
  usuario: Usuario | null
  isAuthenticated: boolean
  login: (email: string, password: string) => boolean
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

function cargarUsuarioGuardado(): Usuario | null {
  const guardado = sessionStorage.getItem(STORAGE_KEY)
  return guardado ? JSON.parse(guardado) : null
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(cargarUsuarioGuardado)

  const login = (email: string, password: string) => {
    const encontrado = loginService(email, password)
    if (!encontrado) return false
    setUsuario(encontrado)
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(encontrado))
    return true
  }

  const logout = () => {
    setUsuario(null)
    sessionStorage.removeItem(STORAGE_KEY)
  }

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