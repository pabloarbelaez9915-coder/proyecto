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

> Estado de validación: rama de funcionalidad creada para preparación del flujo de integración feat -> dev -> qa -> prod.

## Autor

Proyecto desarrollado para la clase de programación.
