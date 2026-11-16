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

      <div className="grid md:grid-cols-2 rounded-2xl overflow-hidden mx-8 mb-8">
        <img
          src="https://images.unsplash.com/photo-1593991340674-c237fbb7e400?w=900&auto=format&fit=crop&q=80"
          alt="Perro rescatado esperando una familia en un refugio"
          className="w-full h-64 md:h-full object-cover"
        />
        <div className="bg-primary-dark p-8 flex flex-col justify-center">
          <p className="font-body text-xs text-white/80 mb-2">RescuePet · Nuestra misión</p>
          <h2 className="font-heading font-bold text-2xl md:text-3xl text-white mb-4">
            Ayudanos a crear un mundo donde ningún animal espere solo.
          </h2>
          <p className="font-body text-sm text-white/90 mb-6">
            Rescatamos, cuidamos y acompañamos cada adopción hasta el final. Cada hogar
            de tránsito y cada familia adoptante suman a esta red de cuidado responsable.
          </p>
          <Link
            to="/registro"
            className="inline-block self-start bg-accent text-white rounded-full px-5 py-2 font-body font-medium text-sm"
          >
            Sumate a la comunidad ↘
          </Link>
        </div>
      </div>
    </main>
  )
}