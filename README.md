# DuplicateFileCleaner Desktop

Aplicación de escritorio en **Python + PyQt5** para detectar y gestionar archivos duplicados de forma segura.

## Objetivo

Este proyecto escanea una carpeta, calcula el hash de cada archivo y agrupa los que son idénticos por contenido. Después, permite seleccionar duplicados y enviarlos a la papelera del sistema (sin borrado permanente directo).

## Características principales

- Escaneo recursivo de carpetas.
- Detección de duplicados por **SHA-256** (no por nombre).
- Barra de progreso durante el escaneo.
- Ejecución del escaneo en hilo separado para evitar congelar la interfaz.
- Tabla de resultados con hash, nombre y ruta completa.
- Eliminación segura mediante `send2trash`.

## Estructura del proyecto

```text
.
├── main.py
├── core/
│   ├── file_scanner.py
│   └── file_operations.py
├── ui/
│   └── main_window.py
├── utils/
│   └── helpers.py
└── requirements.txt
```

## Requisitos

- Python 3.10+
- Dependencias del sistema para PyQt5 (según SO)

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Flujo de uso

1. Selecciona una carpeta.
2. Haz clic en **Escanear**.
3. Revisa los duplicados encontrados en la tabla.
4. Selecciona filas y usa **Enviar seleccionados a papelera**.

## Notas técnicas

- `FileScanner` evita enlaces simbólicos para reducir ciclos y resultados inesperados.
- El cálculo de hash se realiza en bloques (`chunk_size`) para soportar archivos grandes.
- La UI desacopla lógica de negocio (`core/`) de visualización (`ui/`).

## Mejoras futuras sugeridas

- Estrategias de selección automática (mantener más nuevo/más antiguo).
- Filtros por extensión o tamaño mínimo.
- Exportación de reporte a CSV/JSON.
- Tests unitarios para escaneo, hashing y eliminación.

## Licencia

Define aquí tu licencia (por ejemplo MIT).
