from datetime import datetime, timezone


def ahora_utc() -> datetime:
    """Fecha y hora actual en UTC. El frontend la muestra en hora local."""
    return datetime.now(timezone.utc)