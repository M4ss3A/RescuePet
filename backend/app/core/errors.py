from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ErrorDeDominio(Exception):
    """Error de una regla de negocio. Los services lo lanzan sin saber nada de HTTP."""

    status_code = 400

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class NoEncontrado(ErrorDeDominio):
    status_code = 404


class Conflicto(ErrorDeDominio):
    status_code = 409


class ReglaDeNegocio(ErrorDeDominio):
    status_code = 400


def registrar_manejadores(app: FastAPI) -> None:
    """Traduce los errores de dominio a respuestas HTTP en un único lugar."""

    @app.exception_handler(ErrorDeDominio)
    async def manejar_error_de_dominio(_: Request, error: ErrorDeDominio) -> JSONResponse:
        return JSONResponse(status_code=error.status_code, content={"detail": error.mensaje})
