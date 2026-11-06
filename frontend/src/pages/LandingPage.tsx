import { Link } from 'react-router-dom'

export function LandingPage() {
  return (
    <main>
      <div className="bg-gradient-to-br from-primary to-primary-dark rounded-2xl p-8 m-8 text-white">
        <p className="font-body text-xs opacity-85 mb-2">RescuePet · Adopción responsable</p>
        <h1 className="font-heading font-bold text-3xl mb-4">
          Dale un hogar, + amor + familia
        </h1>
        <p className="font-body text-sm max-w-md mb-6 opacity-90">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rescatamos,
          cuidamos y acompañamos el proceso de adopción responsable de animales.
        </p>
        <Link
          to="/catalogo"
          className="inline-block bg-white text-primary-dark rounded-full px-5 py-2 font-body font-medium text-sm"
        >
          Ver animales en adopción ↘
        </Link>
      </div>
    </main>
  )
}