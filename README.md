# Proyecto de gestión de gimnasio

Proyecto académico organizado en carpetas separadas para backend y frontend.

## Estructura

```text
proyecto/
├── Programacion_de _Software_2026_2---backend/
│   ├── src/           # API FastAPI, modelos, CRUD y lógica del programa
│   ├── tests/         # Pruebas automatizadas
│   ├── requirements.txt
│   └── README.md      # Instalación, ejecución y detalles del backend
├── Programacion_de _Software_2026_2---frontend/
│   └── README.md      # Carpeta preparada para el frontend
└── explicacion_examen02.mp4
```

El backend está implementado en Python con FastAPI y SQLAlchemy. El frontend todavía no tiene código; su carpeta queda lista para agregarlo después.

## Ejecutar el backend

Abre PowerShell desde la raíz del proyecto y ejecuta:

```powershell
Set-Location "Programacion_de _Software_2026_2---backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload
```

La documentación interactiva de la API estará en <http://127.0.0.1:8000/docs>. Consulta el [README del backend](./Programacion_de%20_Software_2026_2---backend/README.md) para migraciones, datos de prueba y demostración CRUD.
