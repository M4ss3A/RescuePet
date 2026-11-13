import { useState } from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export function Header() {
  const [open, setOpen] = useState(false)
  const { usuario, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  const navLinks = [
    { to: '/catalogo', label: 'Catálogo' },
    ...(usuario?.roles.includes('RESCATISTA') ? [{ to: '/rescatista', label: 'Panel rescatista' }] : []),
    ...(usuario?.roles.includes('ADOPTANTE') ? [{ to: '/mis-solicitudes', label: 'Mis solicitudes' }] : []),
  ]

  function handleLogout() {
    logout()
    setOpen(false)
    navigate('/')
  }

  return (
    <header className="bg-white border-b border-surface-muted">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="font-heading font-bold text-xl text-primary-dark">
          RescuePet
        </Link>

        <nav className="hidden md:flex items-center gap-6">
          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `font-body text-sm ${isActive ? 'text-primary-dark font-medium' : 'text-ink'}`
              }
            >
              {link.label}
            </NavLink>
          ))}

          {isAuthenticated ? (
            <>
              <span className="font-body text-sm text-ink/70">Hola, {usuario?.nombre}</span>
              <button onClick={handleLogout} className="font-body text-sm text-accent">
                Cerrar sesión
              </button>
            </>
          ) : (
            <NavLink to="/login" className="font-body text-sm text-ink">
              Iniciar sesión
            </NavLink>
          )}
        </nav>

        <button
          className="md:hidden font-body text-sm text-ink"
          onClick={() => setOpen(!open)}
          aria-label="Abrir menú"
        >
          {open ? '✕' : '☰'}
        </button>
      </div>

      {open && (
        <nav className="md:hidden flex flex-col gap-1 px-6 pb-4">
          {navLinks.map((link) => (
            <NavLink key={link.to} to={link.to} onClick={() => setOpen(false)} className="font-body text-sm text-ink py-2">
              {link.label}
            </NavLink>
          ))}
          {isAuthenticated ? (
            <>
              <span className="font-body text-sm text-ink/70 py-2">Hola, {usuario?.nombre}</span>
              <button onClick={handleLogout} className="font-body text-sm text-accent text-left py-2">
                Cerrar sesión
              </button>
            </>
          ) : (
            <NavLink to="/login" onClick={() => setOpen(false)} className="font-body text-sm text-ink py-2">
              Iniciar sesión
            </NavLink>
          )}
        </nav>
      )}
    </header>
  )
}