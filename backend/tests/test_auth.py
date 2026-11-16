from app.models.enums import RolNombre

REGISTRO = {
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@test.com",
    "password": "Juan1234!",
    "rol": "ADOPTANTE",
}


def test_registro_devuelve_usuario_sin_contrasena(cliente):
    respuesta = cliente.post("/api/v1/auth/register", json=REGISTRO)
    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["roles"] == ["ADOPTANTE"]
    assert "password" not in datos and "contrasenaHash" not in datos


def test_registro_con_email_repetido_da_409(cliente):
    cliente.post("/api/v1/auth/register", json=REGISTRO)
    assert cliente.post("/api/v1/auth/register", json=REGISTRO).status_code == 409


def test_no_se_puede_registrar_como_administrador(cliente):
    respuesta = cliente.post("/api/v1/auth/register", json={**REGISTRO, "rol": "ADMINISTRADOR"})
    assert respuesta.status_code == 422


def test_login_con_contrasena_incorrecta_da_401(cliente):
    cliente.post("/api/v1/auth/register", json=REGISTRO)
    respuesta = cliente.post("/api/v1/auth/token", data={"username": REGISTRO["email"], "password": "otra"})
    assert respuesta.status_code == 401


def test_login_guarda_el_token_en_cookie_httponly(cliente):
    cliente.post("/api/v1/auth/register", json=REGISTRO)
    respuesta = cliente.post("/api/v1/auth/token", data={"username": REGISTRO["email"], "password": REGISTRO["password"]})
    assert respuesta.status_code == 200
    assert "httponly" in respuesta.headers["set-cookie"].lower()
    assert cliente.get("/api/v1/auth/me").json()["email"] == REGISTRO["email"]


def test_me_sin_cookie_da_401(cliente):
    assert cliente.get("/api/v1/auth/me").status_code == 401


def test_encabezado_authorization_no_se_acepta(crear_usuario):
    juan = crear_usuario("juan", RolNombre.ADOPTANTE)
    token = juan.cookies["access_token"]
    juan.cookies.clear()
    respuesta = juan.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert respuesta.status_code == 401


def test_usuario_comun_en_ruta_de_admin_da_403(crear_usuario):
    juan = crear_usuario("juan", RolNombre.ADOPTANTE)
    assert juan.get("/api/v1/admin/usuarios").status_code == 403


def test_usuario_desactivado_pierde_el_acceso(crear_usuario):
    admin = crear_usuario("admin", RolNombre.ADMINISTRADOR)
    juan = crear_usuario("juan", RolNombre.ADOPTANTE)
    juan_id = juan.get("/api/v1/auth/me").json()["id"]
    assert admin.post(f"/api/v1/admin/usuarios/{juan_id}/desactivar").status_code == 200
    assert juan.get("/api/v1/auth/me").status_code == 400


def test_logout_cierra_la_sesion(crear_usuario):
    juan = crear_usuario("juan", RolNombre.ADOPTANTE)
    juan.post("/api/v1/auth/logout")
    assert juan.get("/api/v1/auth/me").status_code == 401
