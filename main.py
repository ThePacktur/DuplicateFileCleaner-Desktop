"""Punto de entrada de DuplicateFileCleaner Desktop."""

from __future__ import annotations

import logging
import sys

from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow


def configure_logging() -> None:
    """Configura un logger simple para depuración local."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def main() -> int:
    """Inicializa la aplicación Qt y ejecuta el loop principal."""
    configure_logging()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
