import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'

const navLinks = [
  { to: '/catalogo', label: 'Catálogo' },
  { to: '/login', label: 'Iniciar sesión' },
]

export function Header() {
  const [open, setOpen] = useState(false)

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
            <NavLink
              key={link.to}
              to={link.to}
              onClick={() => setOpen(false)}
              className="font-body text-sm text-ink py-2"
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      )}
    </header>
  )
}