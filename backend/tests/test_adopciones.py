from datetime import date

import pytest

from app.core.uow import UnitOfWork
from app.models import Animal
from app.models.enums import Especie, RolNombre

SOLICITUD = {
    "tipoVivienda": "Casa con patio",
    "tienePatio": True,
    "tieneOtrosAnimales": False,
    "experienciaPrevia": "Tuve perros",
    "motivo": "Tenemos espacio y tiempo para cuidarlo.",
}


@pytest.fixture()
def escenario(crear_usuario):
    """Una rescatista con un animal publicado y dos adoptantes."""
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    juan = crear_usuario("juan", RolNombre.ADOPTANTE)
    sofi = crear_usuario("sofi", RolNombre.ADOPTANTE)
    animal_id = ana.post("/api/v1/animales", json={"nombre": "Toby", "especie": "Perro", "tamano": "Grande"}).json()["id"]
    publicacion = ana.post("/api/v1/publicaciones", json={"animalId": animal_id, "titulo": "Toby", "descripcion": "Busca familia"})
    assert publicacion.status_code == 201
    return {"ana": ana, "juan": juan, "sofi": sofi, "animal_id": animal_id, "publicacion_id": publicacion.json()["id"]}


def test_solicitud_calcula_el_puntaje(escenario):
    respuesta = escenario["juan"].post("/api/v1/solicitudes", json={**SOLICITUD, "animalId": escenario["animal_id"]})
    assert respuesta.status_code == 201
    assert float(respuesta.json()["puntajeCompatibilidad"]) > 0


def test_no_se_puede_solicitar_el_animal_propio(escenario):
    respuesta = escenario["ana"].post("/api/v1/solicitudes", json={**SOLICITUD, "animalId": escenario["animal_id"]})
    assert respuesta.status_code == 400


def test_solicitud_duplicada_da_409(escenario):
    juan = escenario["juan"]
    datos = {**SOLICITUD, "animalId": escenario["animal_id"]}
    juan.post("/api/v1/solicitudes", json=datos)
    assert juan.post("/api/v1/solicitudes", json=datos).status_code == 409


def test_no_se_puede_solicitar_un_animal_no_publicado(escenario):
    otro_id = escenario["ana"].post("/api/v1/animales", json={"nombre": "Mora", "especie": "Gato"}).json()["id"]
    respuesta = escenario["juan"].post("/api/v1/solicitudes", json={**SOLICITUD, "animalId": otro_id})
    assert respuesta.status_code == 400


def test_aprobar_concreta_la_adopcion_en_una_sola_transaccion(escenario):
    ana, juan, sofi = escenario["ana"], escenario["juan"], escenario["sofi"]
    datos = {**SOLICITUD, "animalId": escenario["animal_id"]}
    id_juan = juan.post("/api/v1/solicitudes", json=datos).json()["id"]
    id_sofi = sofi.post("/api/v1/solicitudes", json=datos).json()["id"]

    respuesta = ana.post(f"/api/v1/solicitudes/{id_juan}/aprobar")
    assert respuesta.status_code == 201
    adopcion = respuesta.json()
    assert adopcion["estado"] == "EN_SEGUIMIENTO"

    # Todos los efectos del caso de uso quedaron aplicados
    assert juan.get(f"/api/v1/solicitudes/{id_juan}").json()["estado"] == "APROBADA"
    assert sofi.get(f"/api/v1/solicitudes/{id_sofi}").json()["estado"] == "RECHAZADA"
    assert ana.get(f"/api/v1/animales/{escenario['animal_id']}").json()["estado"] == "ADOPTADO"
    assert ana.get(f"/api/v1/publicaciones/{escenario['publicacion_id']}").json()["estado"] == "FINALIZADA"
    assert juan.get("/api/v1/adopciones").json()[0]["id"] == adopcion["id"]


def test_solo_el_autor_puede_aprobar(escenario, crear_usuario):
    bea = crear_usuario("bea", RolNombre.RESCATISTA)
    solicitud_id = escenario["juan"].post("/api/v1/solicitudes", json={**SOLICITUD, "animalId": escenario["animal_id"]}).json()["id"]
    assert bea.post(f"/api/v1/solicitudes/{solicitud_id}/aprobar").status_code == 403


def test_seguimiento_solo_lo_carga_el_responsable(escenario):
    ana, juan = escenario["ana"], escenario["juan"]
    solicitud_id = juan.post("/api/v1/solicitudes", json={**SOLICITUD, "animalId": escenario["animal_id"]}).json()["id"]
    adopcion_id = ana.post(f"/api/v1/solicitudes/{solicitud_id}/aprobar").json()["id"]
    hoy = {"fecha": date.today().isoformat(), "estadoGeneral": "Muy bien"}
    assert juan.post(f"/api/v1/adopciones/{adopcion_id}/seguimientos", json=hoy).status_code == 403
    assert ana.post(f"/api/v1/adopciones/{adopcion_id}/seguimientos", json=hoy).status_code == 201
    assert len(juan.get(f"/api/v1/adopciones/{adopcion_id}/seguimientos").json()) == 1


def test_unit_of_work_deshace_todo_si_hay_un_error(base_de_datos):
    """Si falla algo dentro del bloque `with`, no se guarda nada (rollback)."""
    with pytest.raises(RuntimeError):
        with UnitOfWork() as uow:
            uow.animales.agregar(Animal(nombre="Fantasma", especie=Especie.GATO))
            raise RuntimeError("falla a mitad del caso de uso")

    with UnitOfWork() as uow:
        assert all(animal.nombre != "Fantasma" for animal in uow.animales.listar())
