import { getAllAnimales } from './animalService'
import { getAllHogares, getAsignacionesActivasByHogarId } from './hogarTransitoService'
import { getAllSolicitudes } from './solicitudAdopcionService'
import { getAllAdopciones } from './adopcionService'
import type { EstadoAnimal } from '../types/animal'

export interface ConteoPorEstado {
  estado: string
  cantidad: number
}

export function getAnimalesPorEstado(): ConteoPorEstado[] {
  const animales = getAllAnimales()
  const estados: EstadoAnimal[] = ['DISPONIBLE', 'EN_TRANSITO', 'EN_PROCESO_ADOPCION', 'ADOPTADO', 'INACTIVO']
  return estados.map((estado) => ({
    estado,
    cantidad: animales.filter((a) => a.estado === estado).length,
  }))
}

export function getSolicitudesPorEstado(): ConteoPorEstado[] {
  const solicitudes = getAllSolicitudes()
  const estados = ['PENDIENTE', 'APROBADA', 'RECHAZADA', 'CANCELADA']
  return estados.map((estado) => ({
    estado,
    cantidad: solicitudes.filter((s) => s.estado === estado).length,
  }))
}

export function getAdopcionesPorMes(): { mes: string; cantidad: number }[] {
  const adopciones = getAllAdopciones()
  const conteoPorMes: Record<string, number> = {}
  for (const a of adopciones) {
    const mes = a.fechaAdopcion.slice(0, 7)
    conteoPorMes[mes] = (conteoPorMes[mes] ?? 0) + 1
  }
  return Object.entries(conteoPorMes)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([mes, cantidad]) => ({ mes, cantidad }))
}

export function getResumenGeneral() {
  const animales = getAllAnimales()
  const hogares = getAllHogares()
  const animalesEnHogares = hogares.reduce(
    (acc, h) => acc + getAsignacionesActivasByHogarId(h.id).length,
    0
  )

  return {
    totalAnimales: animales.length,
    disponibles: animales.filter((a) => a.estado === 'DISPONIBLE').length,
    hogaresActivos: hogares.filter((h) => h.disponible).length,
    animalesEnHogares,
    totalAdopciones: getAllAdopciones().length,
  }
}