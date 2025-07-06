# Landing Builder

Servicio low-code para crear landing pages con subdominios dinámicos.

## Inicio rápido

```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down
```

## Servicios

- **Frontend Builder**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **MinIO Console**: http://localhost:9001
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Subdominios

Los sitios generados se sirven en:
- `cliente.localhost` (requerirá configuración de DNS local)

## Tests

Ejecutar tests del generador de sitios estáticos:
```bash
docker-compose exec backend make test-generator
```

Ejecutar todos los tests:
```bash
docker-compose exec backend make test-all
```

## Estructura

```
├── backend/          # API FastAPI + Generador de sitios
├── frontend/         # React Builder (en desarrollo)
├── nginx/            # Reverse proxy con subdominios
├── generated-sites/  # Sitios estáticos generados
├── test_*.py        # Suite completa de tests
└── docker-compose.yml
```

## Funcionalidades implementadas

✅ **API REST completa**
- Gestión de páginas y componentes
- Validación con Pydantic
- Base de datos PostgreSQL

✅ **Generador de sitios estáticos**
- Renderizado de componentes (hero, text, image, button, header, footer)
- Sistema de temas (default, dark, modern, minimal)
- Templates responsivos con Jinja2
- Deployment automático

✅ **Infraestructura**
- Docker Compose para desarrollo
- Nginx con subdominios dinámicos
- Volúmenes persistentes
- Background tasks

✅ **Autenticación y Autorización**
- Sistema JWT completo
- Registro y login de usuarios
- Protección de endpoints
- Gestión de perfiles de usuario
- Cambio de contraseñas

✅ **Tests completos**
- Tests unitarios del generador
- Tests de componentes
- Tests de templates y temas
- Tests de deployment
- Tests de integración
- Tests de autenticación completos

## API Endpoints

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener perfil actual
- `PUT /api/auth/me` - Actualizar perfil
- `POST /api/auth/change-password` - Cambiar contraseña
- `POST /api/auth/refresh-token` - Renovar token

### Páginas (requieren autenticación)
- `GET /api/pages/` - Listar páginas
- `POST /api/pages/` - Crear página 🔒
- `PUT /api/pages/{id}` - Actualizar página 🔒
- `DELETE /api/pages/{id}` - Eliminar página 🔒
- `POST /api/pages/{id}/publish` - Publicar página 🔒

### Deployment (requieren autenticación)
- `POST /api/deploy/{id}` - Deployar página 🔒
- `GET /api/deploy/status/{slug}` - Estado del deployment
- `DELETE /api/deploy/{id}` - Eliminar deployment 🔒

🔒 = Requiere autenticación