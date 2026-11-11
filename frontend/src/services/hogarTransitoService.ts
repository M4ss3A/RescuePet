import type { HogarTransito, AsignacionTransito } from '../types/hogarTransito'

// NOTA: mock en memoria — los cambios se pierden al recargar la pagina.
// Se resuelve en el Hito 5, cuando esto pase a consultar la API real.
const hogaresMock: HogarTransito[] = [
  { id: 1, responsableId: 1, direccion: 'Barrio Alta Córdoba', capacidad: 3, disponible: true, observaciones: 'Acepta perros y gatos.' },
  { id: 2, responsableId: 1, direccion: 'Barrio Nueva Córdoba', capacidad: 2, disponible: false, observaciones: 'Solo gatos.' },
]

const asignacionesMock: AsignacionTransito[] = [
  { id: 1, animalId: 2, hogarTransitoId: 1, fechaIngreso: '2026-03-16' },
]

let nextHogarId = hogaresMock.length + 1

export function getAllHogares(): HogarTransito[] {
  return hogaresMock
}

export function getHogarById(id: number): HogarTransito | undefined {
  return hogaresMock.find((h) => h.id === id)
}

export function createHogar(data: Omit<HogarTransito, 'id'>): HogarTransito {
  const nuevo: HogarTransito = { id: nextHogarId++, ...data }
  hogaresMock.push(nuevo)
  return nuevo
}

export function updateHogar(id: number, data: Partial<Omit<HogarTransito, 'id'>>): HogarTransito | undefined {
  const hogar = hogaresMock.find((h) => h.id === id)
  if (!hogar) return undefined
  Object.assign(hogar, data)
  return hogar
}

export function getAsignacionesActivasByHogarId(hogarId: number): AsignacionTransito[] {
  return asignacionesMock.filter((a) => a.hogarTransitoId === hogarId && !a.fechaSalida)
}