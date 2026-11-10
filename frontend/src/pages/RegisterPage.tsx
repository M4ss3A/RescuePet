import { useState, type FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { register } from '../services/authService'
import type { Rol } from '../types/auth'

const rolesDisponibles: { value: Rol; label: string }[] = [
  { value: 'ADOPTANTE', label: 'Adoptante' },
  { value: 'RESCATISTA', label: 'Rescatista / Protectora' },
  { value: 'HOGAR_TRANSITO', label: 'Hogar de tránsito' },
]

export function RegisterPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [nombre, setNombre] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rol, setRol] = useState<Rol>('ADOPTANTE')

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    register(nombre, email, password, rol)
    login(email, password)
    navigate('/')
  }

  return (
    <main className="max-w-md mx-auto px-6 py-12">
      <h1 className="font-heading font-bold text-3xl text-ink mb-6">Crear cuenta</h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Nombre</span>
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm"
          />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Email</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm"
          />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Contraseña</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm"
          />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-body text-sm text-ink">Soy</span>
          <select
            value={rol}
            onChange={(e) => setRol(e.target.value as Rol)}
            className="border border-surface-muted rounded-lg px-3 py-2 font-body text-sm"
          >
            {rolesDisponibles.map((r) => (
              <option key={r.value} value={r.value}>{r.label}</option>
            ))}
          </select>
        </label>

        <button
          type="submit"
          className="bg-primary text-white rounded-full px-5 py-2 font-body font-medium text-sm mt-2"
        >
          Crear cuenta
        </button>
      </form>

      <p className="font-body text-sm text-ink/70 mt-4">
        ¿Ya tenés cuenta? <Link to="/login" className="text-primary-dark underline">Iniciá sesión</Link>
      </p>
    </main>
  )
}