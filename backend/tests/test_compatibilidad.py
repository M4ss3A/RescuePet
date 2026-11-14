from app.models.enums import Tamano, TipoVivienda
from app.services.compatibilidad import calcular_puntaje

MOTIVO_LARGO = "x" * 100


def test_puntaje_maximo_es_100():
    puntaje = calcular_puntaje(
        tamano=Tamano.GRANDE,
        tipo_vivienda=TipoVivienda.CASA_CON_PATIO,
        tiene_patio=True,
        experiencia_previa="Tuve perros",
        tiene_otros_animales=False,
        motivo=MOTIVO_LARGO,
    )
    assert puntaje == 100


def test_perro_grande_en_departamento_puntua_bajo():
    puntaje = calcular_puntaje(
        tamano=Tamano.GRANDE,
        tipo_vivienda=TipoVivienda.DEPARTAMENTO,
        tiene_patio=False,
        experiencia_previa=None,
        tiene_otros_animales=True,
        motivo="corto",
    )
    assert puntaje == 10 


def test_animal_pequeno_se_adapta_a_departamento():
    grande = calcular_puntaje(Tamano.GRANDE, TipoVivienda.DEPARTAMENTO, False, None, False, "corto")
    pequeno = calcular_puntaje(Tamano.PEQUENO, TipoVivienda.DEPARTAMENTO, False, None, False, "corto")
    assert pequeno > grande


def test_experiencia_vacia_no_suma():
    con_espacios = calcular_puntaje(Tamano.MEDIANO, TipoVivienda.CASA_SIN_PATIO, False, "   ", False, "corto")
    sin_experiencia = calcular_puntaje(Tamano.MEDIANO, TipoVivienda.CASA_SIN_PATIO, False, None, False, "corto")
    assert con_espacios == sin_experiencia
