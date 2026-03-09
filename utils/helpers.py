"""Funciones auxiliares reutilizables."""

from __future__ import annotations

from pathlib import Path


def human_readable_size(size_in_bytes: int) -> str:
    """Convierte bytes a formato legible (KB, MB, GB...)."""
    size = float(size_in_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024.0 or unit == "TB":
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size_in_bytes} B"


def safe_name(path: str) -> str:
    """Retorna solo el nombre de archivo desde una ruta completa."""
    return Path(path).name
