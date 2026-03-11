"""Operaciones sobre archivos duplicados (papelera y restauración)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from send2trash import send2trash


@dataclass
class RemovedFile:
    """Representa un archivo enviado a la papelera."""

    original_path: str


class FileOperations:
    """Encapsula operaciones de eliminación segura."""

    def __init__(self) -> None:
        self._removed_files: list[RemovedFile] = []

    def mover_a_papelera(self, file_paths: list[str]) -> int:
        moved = 0
        for file_path in file_paths:
            path = Path(file_path)
            if path.exists() and path.is_file():
                send2trash(str(path))
                self._removed_files.append(RemovedFile(original_path=str(path)))
                moved += 1
        return moved

    @property
    def historial_eliminados(self) -> list[RemovedFile]:
        return list(self._removed_files)
