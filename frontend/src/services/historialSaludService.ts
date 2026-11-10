import type { RegistroSalud } from '../types/animal'

const historialMock: Record<number, RegistroSalud[]> = {
  1: [
    { id: 1, tipo: 'VACUNA', fecha: '2026-03-10', descripcion: 'Antirrábica', veterinario: 'Dra. Pérez' },
    { id: 2, tipo: 'CONSULTA', fecha: '2026-06-02', descripcion: 'Control de rutina, sin novedades', veterinario: 'Dra. Pérez' },
  ],
  2: [
    { id: 3, tipo: 'TRATAMIENTO', fecha: '2026-01-15', descripcion: 'Desparasitación', veterinario: 'Dr. Gómez' },
  ],
  3: [
    { id: 4, tipo: 'VACUNA', fecha: '2026-05-20', descripcion: 'Triple felina', veterinario: 'Dra. Pérez' },
  ],
  4: [
    { id: 5, tipo: 'VACUNA', fecha: '2026-02-01', descripcion: 'Antirrábica', veterinario: 'Dr. Gómez' },
    { id: 6, tipo: 'CONSULTA', fecha: '2026-04-18', descripcion: 'Chequeo dental', veterinario: 'Dr. Gómez' },
  ],
}

export function getHistorialSaludByAnimalId(animalId: number): RegistroSalud[] {
  return historialMock[animalId] ?? []
}