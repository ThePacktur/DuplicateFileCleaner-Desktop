"""Escaneo de archivos duplicados basado en hash SHA-256."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Callable, DefaultDict
import hashlib

ProgressCallback = Callable[[int], None]
DuplicateMap = dict[str, list[str]]


class FileScanner:
    """Busca archivos duplicados dentro de una carpeta."""

    def __init__(self, chunk_size: int = 1024 * 1024) -> None:
        self.chunk_size = chunk_size

    def encontrar_duplicados(
        self,
        ruta_carpeta: str,
        progress_callback: ProgressCallback | None = None,
    ) -> DuplicateMap:
        """Retorna un mapa hash -> rutas para entradas con más de un archivo."""
        base_path = Path(ruta_carpeta)
        if not base_path.exists() or not base_path.is_dir():
            raise ValueError(f"Ruta inválida para escaneo: {ruta_carpeta}")

        archivos = [
            path
            for path in base_path.rglob("*")
            if path.is_file() and not path.is_symlink()
        ]

        total = len(archivos)
        por_hash: DefaultDict[str, list[str]] = defaultdict(list)

        for index, file_path in enumerate(archivos, start=1):
            file_hash = self._calcular_hash(file_path)
            por_hash[file_hash].append(str(file_path))

            if progress_callback is not None:
                progress = int((index / max(total, 1)) * 100)
                progress_callback(progress)

        return {h: files for h, files in por_hash.items() if len(files) > 1}

    def _calcular_hash(self, ruta_archivo: Path) -> str:
        hasher = hashlib.sha256()
        with ruta_archivo.open("rb") as file_handle:
            while True:
                bloque = file_handle.read(self.chunk_size)
                if not bloque:
                    break
                hasher.update(bloque)
        return hasher.hexdigest()
