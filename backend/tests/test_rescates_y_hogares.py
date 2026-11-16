from app.models.enums import RolNombre


def crear_animal(cliente, nombre="Toby"):
    return cliente.post("/api/v1/animales", json={"nombre": nombre, "especie": "Perro"}).json()["id"]


def test_el_rescatista_es_el_usuario_logueado(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    animal_id = crear_animal(ana)
    respuesta = ana.post(f"/api/v1/animales/{animal_id}/rescate", json={"fechaRescate": "2026-02-01", "ubicacion": "Córdoba"})
    assert respuesta.status_code == 201
    assert respuesta.json()["rescatistaId"] == ana.get("/api/v1/auth/me").json()["id"]


def test_un_animal_no_puede_tener_dos_rescates(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    animal_id = crear_animal(ana)
    datos = {"fechaRescate": "2026-02-01", "ubicacion": "Córdoba"}
    ana.post(f"/api/v1/animales/{animal_id}/rescate", json=datos)
    assert ana.post(f"/api/v1/animales/{animal_id}/rescate", json=datos).status_code == 409


def test_otro_rescatista_no_puede_editar_el_rescate(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    bea = crear_usuario("bea", RolNombre.RESCATISTA)
    animal_id = crear_animal(ana)
    ana.post(f"/api/v1/animales/{animal_id}/rescate", json={"fechaRescate": "2026-02-01", "ubicacion": "Córdoba"})
    assert bea.patch(f"/api/v1/animales/{animal_id}/rescate", json={"ubicacion": "X"}).status_code == 403


def test_registro_sanitario_con_fecha_futura_da_400(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    animal_id = crear_animal(ana)
    datos = {"tipo": "VACUNA", "fecha": "2099-01-01", "descripcion": "Antirrábica"}
    assert ana.post(f"/api/v1/animales/{animal_id}/registros-sanitarios", json=datos).status_code == 400


def test_asignar_y_egresar_cambia_el_estado_del_animal(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    laura = crear_usuario("laura", RolNombre.HOGAR_TRANSITO)
    animal_id = crear_animal(ana)
    hogar_id = laura.post("/api/v1/hogares-transito", json={"direccion": "Calle 1", "capacidad": 1}).json()["id"]

    asignacion = ana.post(
        f"/api/v1/hogares-transito/{hogar_id}/asignaciones", json={"animalId": animal_id, "fechaIngreso": "2026-03-01"}
    )
    assert asignacion.status_code == 201
    assert ana.get(f"/api/v1/animales/{animal_id}").json()["estado"] == "EN_TRANSITO"

    egreso = laura.patch(f"/api/v1/asignaciones-transito/{asignacion.json()['id']}/egreso", json={"fechaSalida": "2026-04-01"})
    assert egreso.status_code == 200
    assert ana.get(f"/api/v1/animales/{animal_id}").json()["estado"] == "DISPONIBLE"


def test_hogar_sin_lugar_no_acepta_mas_animales(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    laura = crear_usuario("laura", RolNombre.HOGAR_TRANSITO)
    hogar_id = laura.post("/api/v1/hogares-transito", json={"direccion": "Calle 1", "capacidad": 1}).json()["id"]
    for nombre, esperado in (("Toby", 201), ("Coco", 400)):
        animal_id = crear_animal(ana, nombre)
        respuesta = ana.post(
            f"/api/v1/hogares-transito/{hogar_id}/asignaciones", json={"animalId": animal_id, "fechaIngreso": "2026-03-01"}
        )
        assert respuesta.status_code == esperado


def test_otro_hogar_no_puede_editar_el_hogar(crear_usuario):
    laura = crear_usuario("laura", RolNombre.HOGAR_TRANSITO)
    mia = crear_usuario("mia", RolNombre.HOGAR_TRANSITO)
    hogar_id = laura.post("/api/v1/hogares-transito", json={"direccion": "Calle 1", "capacidad": 2}).json()["id"]
    assert mia.patch(f"/api/v1/hogares-transito/{hogar_id}", json={"capacidad": 5}).status_code == 403
