from app.models.enums import RolNombre

MICHI = {"nombre": "Michi", "especie": "Gato", "edadAproximada": 2, "fotoUrl": "https://f/michi.png"}


def test_catalogo_es_publico(cliente):
    assert cliente.get("/api/v1/animales").status_code == 200


def test_crear_animal_sin_login_da_401(cliente):
    assert cliente.post("/api/v1/animales", json=MICHI).status_code == 401


def test_adoptante_no_puede_crear_animales(crear_usuario):
    juan = crear_usuario("juan", RolNombre.ADOPTANTE)
    assert juan.post("/api/v1/animales", json=MICHI).status_code == 403


def test_rescatista_crea_animal_y_la_respuesta_esta_en_camelcase(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    respuesta = ana.post("/api/v1/animales", json=MICHI)
    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["edadAproximada"] == 2
    assert datos["fotoUrl"] == MICHI["fotoUrl"]
    assert datos["estado"] == "DISPONIBLE"


def test_especie_invalida_da_422(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    assert ana.post("/api/v1/animales", json={**MICHI, "especie": "Dinosaurio"}).status_code == 422


def test_baja_logica_pasa_a_inactivo(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    animal_id = ana.post("/api/v1/animales", json=MICHI).json()["id"]
    assert ana.delete(f"/api/v1/animales/{animal_id}").status_code == 204
    assert ana.get(f"/api/v1/animales/{animal_id}").json()["estado"] == "INACTIVO"


def test_animal_inexistente_da_404(cliente):
    assert cliente.get("/api/v1/animales/999").status_code == 404
