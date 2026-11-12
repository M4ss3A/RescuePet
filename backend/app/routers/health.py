from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Permite verificar que la API está funcionando."""
    return {"status": "ok"}