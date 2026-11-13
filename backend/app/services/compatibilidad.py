"""Cálculo del puntaje de compatibilidad entre un adoptante y un animal (de 0 a 100).

Criterios y puntos máximos:
- Vivienda según el tamaño del animal ......... 40
- Patio ....................................... 10
- Experiencia previa con animales ............. 20
- Otros animales en el hogar .................. 10
- Motivo explicado con detalle ................ 20
"""

from decimal import Decimal

from app.models.enums import Tamano, TipoVivienda


PUNTOS_VIVIENDA: dict[Tamano | None, dict[TipoVivienda, int]] = {
    Tamano.GRANDE: {
        TipoVivienda.CASA_CON_PATIO: 40,
        TipoVivienda.CASA_SIN_PATIO: 20,
        TipoVivienda.DEPARTAMENTO: 5,
    },
    Tamano.MEDIANO: {
        TipoVivienda.CASA_CON_PATIO: 40,
        TipoVivienda.CASA_SIN_PATIO: 30,
        TipoVivienda.DEPARTAMENTO: 20,
    },
    Tamano.PEQUENO: {
        TipoVivienda.CASA_CON_PATIO: 40,
        TipoVivienda.CASA_SIN_PATIO: 40,
        TipoVivienda.DEPARTAMENTO: 35,
    },
}


def calcular_puntaje(
    tamano: Tamano | None,
    tipo_vivienda: TipoVivienda,
    tiene_patio: bool,
    experiencia_previa: str | None,
    tiene_otros_animales: bool,
    motivo: str,
) -> Decimal:
    puntaje = PUNTOS_VIVIENDA[tamano or Tamano.MEDIANO][tipo_vivienda]

    if tiene_patio:
        puntaje += 10

    if experiencia_previa and experiencia_previa.strip():
        puntaje += 20

    puntaje += 5 if tiene_otros_animales else 10

    largo_motivo = len(motivo.strip())
    if largo_motivo >= 100:
        puntaje += 20
    elif largo_motivo >= 30:
        puntaje += 10

    return Decimal(puntaje)