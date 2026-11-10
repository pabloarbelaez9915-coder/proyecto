# FORMA — Gestión de gimnasio

Frontend Angular para administrar los módulos del gimnasio mediante la API local del proyecto.

**Repositorio de entrega:** [pabloarbelaez9915-coder/proyecto](https://github.com/pabloarbelaez9915-coder/proyecto)

## 1. Cómo ejecutar el proyecto en local

Se necesitan dos terminales de PowerShell abiertas al mismo tiempo: una para el backend y otra para el frontend. Ejecuta los comandos desde la raíz del repositorio.

### Terminal 1: API

El entorno virtual está en la raíz del repositorio. Si todavía no existe, créalo primero con `python -m venv .venv`.

```powershell
.\.venv\Scripts\Activate.ps1
Set-Location ".\Programacion_de _Software_2026_2---backend"
python -m pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload
```

La instalación de dependencias solo hace falta la primera vez o cuando cambien los requisitos.

### Terminal 2: frontend

```powershell
Set-Location ".\Programacion_de _Software_2026_2---frontend"
npm install
npm start
```

La instalación con `npm install` solo hace falta la primera vez o cuando cambien las dependencias. Abre [http://localhost:4200](http://localhost:4200). Mantén las dos terminales abiertas mientras usas el sistema.

## 2. URL del backend

La aplicación consume la API REST en **[http://127.0.0.1:8000/api/v1](http://127.0.0.1:8000/api/v1)**. Su documentación interactiva está en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## 3. Video del punto 6

[Ver o descargar el video de la entrega](./explicacion_examen02.mp4).

[Ver el video del parcial](./Video_Parcial%234.mp4)
