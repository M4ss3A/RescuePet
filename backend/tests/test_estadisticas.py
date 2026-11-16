from app.models.enums import RolNombre


def test_estadisticas_requieren_rol_rescatista_o_admin(cliente, crear_usuario):
    assert cliente.get("/api/v1/estadisticas").status_code == 401
    juan = crear_usuario("juan", RolNombre.ADOPTANTE)
    assert juan.get("/api/v1/estadisticas").status_code == 403


def test_estadisticas_cuentan_los_animales_por_estado(crear_usuario):
    ana = crear_usuario("ana", RolNombre.RESCATISTA)
    for nombre in ("Toby", "Coco"):
        ana.post("/api/v1/animales", json={"nombre": nombre, "especie": "Perro"})
    datos = ana.get("/api/v1/estadisticas").json()
    assert datos["resumen"]["totalAnimales"] == 2
    por_estado = {fila["estado"]: fila["cantidad"] for fila in datos["animalesPorEstado"]}
    assert por_estado["DISPONIBLE"] == 2
    assert por_estado["ADOPTADO"] == 0
