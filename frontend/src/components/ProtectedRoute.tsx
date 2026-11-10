import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import type { Rol } from '../types/auth'

interface Props {
  allowedRoles?: Rol[]
}

export function ProtectedRoute({ allowedRoles }: Props) {
  const { usuario, isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (allowedRoles && !allowedRoles.some((r) => usuario?.roles.includes(r))) {
    return <Navigate to="/" replace />
  }

  return <Outlet />
}