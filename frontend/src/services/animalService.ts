import type { Animal } from '../types/animal'

// NOTA: mock en memoria — los cambios (alta/edicion/baja) se pierden al recargar
// la pagina. Se resuelve en el Hito 5, cuando esto pase a consultar la API real.

const animalesMock: Animal[] = [
  { id: 1, nombre: 'Michi', especie: 'Gato', raza: 'Mestizo', edadAproximada: 2, tamano: 'Pequeño', descripcion: 'Tranquilo, le encanta dormir al sol.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/17A79C/white?text=Michi' },
  { id: 2, nombre: 'Coco', especie: 'Perro', raza: 'Mestizo', edadAproximada: 3, tamano: 'Grande', descripcion: 'Muy jugetón, ideal para casa con patio.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/0B6F68/white?text=Coco' },
  { id: 3, nombre: 'Lola', especie: 'Gato', raza: 'Siamés', edadAproximada: 1, tamano: 'Pequeño', descripcion: 'Curiosa y cariñosa, se lleva bien con niños.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/E2574C/white?text=Lola' },
  { id: 4, nombre: 'Low', especie: 'Perro', raza: 'Caniche', edadAproximada: 5, tamano: 'Mediano', descripcion: 'Tranquilo, ya convive bien con otros perros.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/17A79C/white?text=Low' },
  { id: 5, nombre: 'Bugs', especie: 'Otro', raza: 'Conejo', edadAproximada: 1, tamano: 'Pequeño', descripcion: 'Necesita un espacio tranquilo y mucho cariño.', estado: 'DISPONIBLE', fotoUrl: 'https://placehold.co/400x300/0B6F68/white?text=Bugs' },
  { id: 6, nombre: 'Toby', especie: 'Perro', raza: 'Labrador', edadAproximada: 4, tamano: 'Grande', descripcion: 'Activo, le encanta correr y jugar a la pelota.', estado: 'EN_PROCESO_ADOPCION', fotoUrl: 'https://placehold.co/400x300/E2574C/white?text=Toby' },
]

export function getAnimalesDisponibles(): Animal[] {
  return animalesMock.filter((a) => a.estado === 'DISPONIBLE')
}

export function getAnimalById(id: number): Animal | undefined {
  return animalesMock.find((a) => a.id === id)
}

export function getAllAnimales(): Animal[] {
  return animalesMock
}

let nextAnimalId = animalesMock.length + 1

export function createAnimal(data: Omit<Animal, 'id'>): Animal {
  const nuevo: Animal = { id: nextAnimalId++, ...data }
  animalesMock.push(nuevo)
  return nuevo
}

export function updateAnimal(id: number, data: Partial<Omit<Animal, 'id'>>): Animal | undefined {
  const animal = animalesMock.find((a) => a.id === id)
  if (!animal) return undefined
  Object.assign(animal, data)
  return animal
}

export function darDeBajaAnimal(id: number): void {
  updateAnimal(id, { estado: 'INACTIVO' })
}