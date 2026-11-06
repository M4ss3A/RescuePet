import type { Animal } from '../types/animal'

const animalesMock: Animal[] = [
  { id: 1, nombre: 'Michi', especie: 'Gato', raza: 'Mestizo', edadAproximada: 2, tamano: 'Pequeño', descripcion: 'Tranquilo, le encanta dormir al sol.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/17A79C/white?text=Michi' },
  { id: 2, nombre: 'Coco', especie: 'Perro', raza: 'Mestizo', edadAproximada: 3, tamano: 'Grande', descripcion: 'Muy jugetón, ideal para casa con patio.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/0B6F68/white?text=Rocky' },
  { id: 3, nombre: 'Luna', especie: 'Gato', raza: 'Siamés', edadAproximada: 1, tamano: 'Pequeño', descripcion: 'Curiosa y cariñosa, se lleva bien con niños.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/E2574C/white?text=Luna' },
  { id: 4, nombre: 'Low', especie: 'Perro', raza: 'Caniche', edadAproximada: 5, tamano: 'Mediano', descripcion: 'Tranquilo, ya convive bien con otros perros.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/17A79C/white?text=Toby' },
  { id: 5, nombre: 'Bugs', especie: 'Otro', raza: 'Conejo', edadAproximada: 1, tamano: 'Pequeño', descripcion: 'Necesita un espacio tranquilo y mucho cariño.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/0B6F68/white?text=Pelusa' },
  { id: 6, nombre: 'Toby', especie: 'Perro', raza: 'Labrador', edadAproximada: 4, tamano: 'Grande', descripcion: 'Activo, le encanta correr y jugar a la pelota.', estado: 'EN_PROCESO_ADOPCION', fotoUrl: 'https://placehold.co/400x300/E2574C/white?text=Max' },
]

export function getAnimalesDisponibles(): Animal[] {
  return animalesMock.filter((a) => a.estado === 'DISPONIBLE')
}