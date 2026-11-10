import { useState, type FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    const ok = login(email, password)
    if (!ok) {
      setError('Email o contraseña incorrectos.')
      return
    }
    navigate('/')
  }

  return (
    <main className="max-w-md mx-auto px-6 py-12">
      <h1 className="font-heading font-bold text-3xl text-ink mb-6">Iniciar sesión</h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
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

        {error && <p className="font-body text-sm text-accent">{error}</p>}

        <button
          type="submit"
          className="bg-primary text-white rounded-full px-5 py-2 font-body font-medium text-sm mt-2"
        >
          Ingresar
        </button>
      </form>

      <p className="font-body text-sm text-ink/70 mt-4">
        ¿No tenés cuenta? <Link to="/registro" className="text-primary-dark underline">Registrate</Link>
      </p>
    </main>
  )
}