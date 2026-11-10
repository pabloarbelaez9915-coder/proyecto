# Frontend Angular — FORMA

Panel web en Angular para administrar las diez entidades de la API del gimnasio. Incluye un menú lateral retraíble, consulta por ID, filtros y operaciones CRUD desde una interfaz propia y adaptable a móviles.

## Requisitos

- Node.js 20.19 o superior y npm.
- API del backend ejecutándose en `http://127.0.0.1:8000`.

## Instalar y ejecutar

Desde PowerShell, en esta carpeta:

```powershell
npm install
npm start
```

Abre <http://localhost:4200>. Para la demostración, mantén también el backend activo. El frontend consume `http://127.0.0.1:8000/api/v1`; la documentación de la API está en <http://127.0.0.1:8000/docs>.

## Módulos

Usuarios, membresías, sedes, clientes, entrenadores, clases, rutinas, equipos, asistencias y pagos. Cada módulo permite listar, consultar un registro por ID, crear, editar y eliminar. Las contraseñas no aparecen en las respuestas del backend; al editar, el campo se deja vacío para conservar la existente.

Las colecciones usan `GET /recurso/` y `POST /recurso/` con barra final; las operaciones por registro usan `/{id}`. Después de crear o editar, la tabla refleja el registro devuelto por la API; al eliminar, se quita de la tabla al confirmar la respuesta. Las referencias a otras entidades (`id_cliente`, `id_sede`, etc.) se ingresan como UUID. Para comprobar un registro por ID, usa el campo «Consulta directa» de la parte superior.

## Verificar la compilación

```powershell
npm run build
```
