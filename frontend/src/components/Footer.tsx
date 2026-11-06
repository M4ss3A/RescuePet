export function Footer() {
  return (
    <footer className="bg-ink text-white">
      <div className="max-w-6xl mx-auto px-6 py-8 font-body text-sm flex flex-col md:flex-row items-center justify-between gap-2">
        <p>© {new Date().getFullYear()} RescuePet. Todos los derechos reservados.</p>
        <p className="opacity-75">Trabajo Final Integrador — TUPaD UTN</p>
      </div>
    </footer>
  )
}