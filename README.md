# Proyecto Gym

Proyecto de clase para la gestión de un gimnasio en Python.

## Descripción

Este proyecto implementa un sistema básico de gestión para un gimnasio, con entidades como:

- Cliente
- Membresía
- Entrenador
- Sede
- Clase
- Rutina
- Equipo
- Asistencia
- Pago

La estructura está pensada para representar modelos y relaciones de negocio, con identificadores UUID, fechas de registro y edición, y campos nulos cuando corresponden.

## Estructura del proyecto

```text
proyecto/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── entities/
│       ├── __init__.py
│       ├── asistencia.py
│       ├── clase.py
│       ├── clientes.py
│       ├── entrenado.py
│       ├── equipo.py
│       ├── membresia.py
│       ├── pago.py
│       ├── rutina.py
│       ├── sede.py
│       └── ...
├── tests/
│   └── test_entidades.py
├── README.md
└── .gitignore
```

## Requisitos

- Python 3.10 o superior
- Git

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/pabloarbelaez9915-coder/proyecto.git
cd proyecto
```

2. Crea un entorno virtual (opcional, pero recomendado):

```bash
python -m venv venv
```

3. Activa el entorno virtual:

- Windows:

```bash
venv\Scripts\activate
```

- Linux/macOS:

```bash
source venv/bin/activate
```

4. Ejecuta la aplicación:

```bash
python src/main.py
```

## Uso

El proyecto cuenta con una interfaz por consola para:

- iniciar sesión
- crear usuario
- gestionar clientes
- gestionar membresías
- gestionar sedes
- gestionar clases y rutinas

## Entidades principales

### Cliente
- id_cliente: UUID
- primer_nombre
- segundo_nombre (nullable)
- primer_apellido
- segundo_apellido (nullable)
- correo
- telefono (nullable)
- clave
- id_membresia (FK, nullable)

### Membresía
- id_membresia: UUID
- nombre
- precio
- descripcion (nullable)
- fecha_inscripcion
- fecha_edicion (nullable)
- activo

### Entrenador
- id_entrenador: UUID
- primer_nombre
- segundo_nombre (nullable)
- primer_apellido
- segundo_apellido (nullable)
- correo
- telefono (nullable)
- clave
- id_sede (FK, nullable)

### Clase
- id_clase: UUID
- nombre
- descripcion (nullable)
- capacidad_maxima
- horario (nullable)
- nivel (nullable)
- id_entrenador (FK, nullable)
- id_sede (FK, nullable)

## Estado del proyecto

Este proyecto está en desarrollo académico y sirve como base para modelar un sistema de gestión deportiva con Python.

## Migración SQLAlchemy y Neon

La migración incluye modelos ORM para `clientes`, `membresias`, `entrenadores`, `sedes`, `clases`, `rutinas`, `equipos`, `asistencias` y `pagos`. Las relaciones y llaves foráneas están definidas en `src/models.py`. Los CRUD reciben una sesión SQLAlchemy y guardan cambios con `commit()`.

### Instalación

Desde la raíz del proyecto, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Base local, migración y seeders

SQLite se usa automáticamente si no existe `DATABASE_URL`. Para crear las tablas y cargar datos de prueba:

```powershell
python -m src.migrations
python -m src.seeders
python -m src.demo_crud
```

Los seeders son idempotentes: se pueden ejecutar varias veces sin duplicar los datos identificados por nombre o correo.

### Conexión con Neon

1. Copia `.env.example` como `.env`.
2. Pega la cadena de conexión de Neon en `DATABASE_URL`, conservando `sslmode=require`.
3. Carga la variable en la sesión de PowerShell (no la escribas en el repositorio):

```powershell
$env:DATABASE_URL = "postgresql+psycopg://USUARIO:CONTRASENA@HOST/BASE?sslmode=require"
python -m src.migrations
python -m src.seeders
```

En Neon se pueden comprobar los resultados con:

```sql
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' ORDER BY table_name;

SELECT id_membresia, nombre, precio FROM membresias;
SELECT id_cliente, correo, id_membresia FROM clientes;
```

### Demostración CRUD

`python -m src.demo_crud` muestra en consola `CREATE`, `READ`, `UPDATE` y `DELETE`. Para la sustentación, ejecuta el demo contra Neon, copia el UUID mostrado y verifica cada estado con consultas SQL en el panel de Neon. El script elimina el registro de demostración al final.

### Flujo de ramas solicitado

```text
dev -> feat/examen-sqlalchemy
feat/examen-sqlalchemy -> dev
feat/examen-sqlalchemy -> qa
feat/examen-sqlalchemy -> prod
```

La rama `feat/examen-sqlalchemy` debe ser la misma fuente de los tres Pull Requests. No se deben subir `.env`, contraseñas ni cadenas de conexión reales.

### Guion breve del video

1. Mostrar la rama `feat` y el código de `src/models.py`.
2. Ejecutar `src.migrations` y mostrar las tablas creadas en Neon.
3. Ejecutar `src.seeders` y consultar las nueve tablas en Neon.
4. Ejecutar `src.demo_crud` y pausar después de cada operación.
5. Confirmar en Neon el registro creado, actualizado y eliminado.
6. Mostrar los tres Pull Requests hacia `dev`, `qa` y `prod`.

## Autor

Proyecto desarrollado para la clase de programación.
"Cambio de validaci�n QA" 
"Validaci�n de QA - cambio de sincronizaci�n" 
