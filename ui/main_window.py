"""Ventana principal de DuplicateFileCleaner."""

from __future__ import annotations

import logging
import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.file_operations import FileOperations
from core.file_scanner import DuplicateMap, FileScanner
from utils.helpers import safe_name

LOGGER = logging.getLogger(__name__)


class ScanThread(QThread):
    """Hilo para evitar bloqueo de UI durante el escaneo."""

    progress_updated = pyqtSignal(int)
    scan_finished = pyqtSignal(dict)
    scan_failed = pyqtSignal(str)

    def __init__(self, folder_path: str) -> None:
        super().__init__()
        self.folder_path = folder_path

    def run(self) -> None:
        scanner = FileScanner()
        try:
            duplicates = scanner.encontrar_duplicados(
                self.folder_path, self.progress_updated.emit
            )
            self.scan_finished.emit(duplicates)
        except Exception as exc:  # noqa: BLE001 - manejo centralizado de errores de hilo
            LOGGER.exception("Error durante escaneo")
            self.scan_failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DuplicateFileCleaner Desktop")
        self.resize(900, 560)

        self.duplicates: DuplicateMap = {}
        self.scan_thread: ScanThread | None = None
        self.file_operations = FileOperations()

        self._build_ui()
        self._bind_events()

    def _build_ui(self) -> None:
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        path_layout = QHBoxLayout()
        self.line_edit_folder = QLineEdit()
        self.line_edit_folder.setPlaceholderText("Selecciona una carpeta para escanear")

        self.btn_select_folder = QPushButton("Seleccionar carpeta")
        self.btn_scan = QPushButton("Escanear")
        self.btn_delete = QPushButton("Enviar seleccionados a papelera")
        self.btn_delete.setEnabled(False)

        path_layout.addWidget(QLabel("Carpeta:"))
        path_layout.addWidget(self.line_edit_folder)
        path_layout.addWidget(self.btn_select_folder)
        path_layout.addWidget(self.btn_scan)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        self.results_table = QTableWidget(0, 3)
        self.results_table.setHorizontalHeaderLabels(["Hash", "Archivo", "Ruta completa"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setSelectionBehavior(self.results_table.SelectRows)
        self.results_table.setSelectionMode(self.results_table.MultiSelection)

        main_layout.addLayout(path_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.results_table)
        main_layout.addWidget(self.btn_delete)

    def _bind_events(self) -> None:
        self.btn_select_folder.clicked.connect(self.select_folder)
        self.btn_scan.clicked.connect(self.start_scan)
        self.btn_delete.clicked.connect(self.delete_selected)

    def select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if folder:
            self.line_edit_folder.setText(folder)

    def start_scan(self) -> None:
        folder_path = self.line_edit_folder.text().strip()
        if not folder_path or not os.path.isdir(folder_path):
            QMessageBox.warning(self, "Advertencia", "Selecciona una carpeta válida.")
            return

        self.progress_bar.setValue(0)
        self.btn_scan.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.results_table.setRowCount(0)

        self.scan_thread = ScanThread(folder_path)
        self.scan_thread.progress_updated.connect(self.progress_bar.setValue)
        self.scan_thread.scan_finished.connect(self.show_results)
        self.scan_thread.scan_failed.connect(self.show_scan_error)
        self.scan_thread.start()

    def show_scan_error(self, error_message: str) -> None:
        self.btn_scan.setEnabled(True)
        QMessageBox.critical(self, "Error de escaneo", error_message)

    def show_results(self, duplicates: DuplicateMap) -> None:
        self.duplicates = duplicates
        self.btn_scan.setEnabled(True)

        row = 0
        for duplicate_hash, file_paths in duplicates.items():
            for file_path in file_paths:
                self.results_table.insertRow(row)
                self.results_table.setItem(row, 0, QTableWidgetItem(duplicate_hash[:12]))
                self.results_table.setItem(row, 1, QTableWidgetItem(safe_name(file_path)))
                self.results_table.setItem(row, 2, QTableWidgetItem(file_path))
                row += 1

        self.btn_delete.setEnabled(row > 0)
        QMessageBox.information(
            self,
            "Escaneo finalizado",
            f"Se encontraron {sum(len(v) for v in duplicates.values())} archivos duplicados.",
        )

    def delete_selected(self) -> None:
        selected_items = self.results_table.selectionModel().selectedRows()
        if not selected_items:
            QMessageBox.information(self, "Información", "No hay filas seleccionadas.")
            return

        file_paths = [self.results_table.item(index.row(), 2).text() for index in selected_items]
        moved = self.file_operations.mover_a_papelera(file_paths)

        QMessageBox.information(
            self,
            "Eliminación completada",
            f"Se enviaron {moved} archivos a la papelera.",
        )
