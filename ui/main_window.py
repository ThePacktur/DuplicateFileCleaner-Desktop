from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMassageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, pyqtSignal
from core.file_scanner import FileScanner
from core.file_operations import FileOperations
import os

class HiloEscaneo(QThread):
    # Define la sigla para enviar mensajes al hilo principal
    progreso_actualizado = pyqtSignal(int)
    escaneo_finalizado = pyqtSignal(dict)

    def __init__(self, ruta_carpeta):
        super().__init__()
        self.ruta_carpeta = ruta_carpeta
      
    def run(self):
        escaner = FileScanner()
        duplicados = escaner.encontrar_duplicados(self.ruta_carpeta, self.actualizar_proceso)
        self.escaneo_finalizado.emit(duplicados)

    def actualizar_procespo(self, progreso):
        self.progreso_actualizado.emit(progreso)
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'main_window.ui'), self)
        self.configurar_ui()
        self.duplicados = {}
        self.hilo_escaner = None

    def configurar_ui(self):
        self.btn_seleccionar_carpeta.clicked.connect(self.seleccionar_carpeta)
        self.btn_escanear.clicked.connect(self.iniciar_escaneo)
        self.btn_eliminar.clicked.connect(self.eliminar_seleccionados)
        self.btn_deshacer.clicked.connect(self.deshacer_eliminacion)
    def seleccionar_carpeta(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if carpeta:
            self.line_edit_carpeta.setText(carpeta)

    def iniciar_escaneo(self):
        ruta_carpeta = self.line_edit_carpeta.text()
        if not ruta_carpeta or not os.path.isdir(ruta_carpeta):
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione una carpeta válida")
            return

        self.barra_progreso.setValue(0)
        self.btn_escanear.setEnabled(False)
        
        self.hilo_escaner = HiloEscaneo(ruta_carpeta)
        self.hilo_escaner.progreso_actualizado.connect(self.actualizar_progreso)
        self.hilo_escaner.escaneo_finalizado.connect(self.mostrar_resultados)
        self.hilo_escaner.start()

    def actualizar_progreso(self, valor):
        self.barra_progreso.setValue(valor)

    def mostrar_resultados(self, duplicados):
        self.duplicados = duplicados
        self.btn_escanear.setEnabled(True)
        # Llenar la tabla con los resultados

    def eliminar_seleccionados(self):
        # Implementar lógica de eliminación usando FileOperations
        pass

    def deshacer_eliminacion(self):
        # Implementar funcionalidad de deshacer
        pass