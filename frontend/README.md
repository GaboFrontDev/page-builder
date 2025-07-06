# Landing Builder Frontend

Frontend de React + TypeScript para el creador de landing pages.

## Características

- **React 18** con TypeScript
- **Tailwind CSS** para estilos
- **Playwright** para tests E2E
- **Drag & Drop** con @dnd-kit
- **React Router** para navegación
- **Context API** para estado global

## Scripts Disponibles

### Desarrollo
```bash
npm start          # Inicia servidor de desarrollo
npm run build      # Construye para producción
npm test           # Tests unitarios con Jest
```

### Testing E2E
```bash
npm run playwright:install    # Instala navegadores de Playwright
npm run test:e2e             # Ejecuta todos los tests E2E
npm run test:e2e:ui          # Ejecuta tests con interfaz visual
npm run test:e2e:headed      # Ejecuta tests con navegador visible
```

## Estructura de Tests

```
e2e/
├── auth.spec.ts              # Tests de autenticación
├── page-builder.spec.ts      # Tests del editor de páginas
├── deployment.spec.ts        # Tests de deployment
├── visual-regression.spec.ts # Tests de regresión visual
├── performance.spec.ts       # Tests de rendimiento
├── helpers/
│   ├── auth.ts              # Helper para autenticación
│   └── page-builder.ts      # Helper para page builder
├── global-setup.ts          # Setup global de tests
└── global-teardown.ts       # Cleanup global de tests
```

## Tests Implementados

### 🔐 **Tests de Autenticación**
- Registro de nuevos usuarios
- Login con credenciales válidas
- Validación de errores (email duplicado, contraseñas incorrectas)
- Logout y redirección
- Rutas protegidas
- Validación de formularios

### 🎨 **Tests del Page Builder**
- Creación de nuevas páginas
- Agregar/editar/eliminar componentes
- Drag & drop para reordenar
- Edición en tiempo real
- Cambio de temas
- Publicación de páginas
- Configuración de página
- Validación de campos

### 🚀 **Tests de Deployment**
- Deployment de páginas publicadas
- Validación de páginas no publicadas
- Vista de sitios desplegados
- Acceso a sitios generados
- Estado de deployment
- Gestión desde dashboard

### 📸 **Tests de Regresión Visual**
- Screenshots de todos los componentes
- Comparación visual entre temas
- Responsive design (móvil/desktop)
- Estados de error y formularios
- Componentes individuales

### ⚡ **Tests de Performance**
- Tiempo de carga de páginas
- Responsividad de drag & drop
- Edición en tiempo real
- Core Web Vitals
- Operaciones concurrentes
- Uso de memoria con muchos componentes

## Configuración de Tests

Los tests están configurados para:
- **Múltiples navegadores**: Chrome, Firefox, Safari, móviles
- **Paralelización** para mayor velocidad
- **Screenshots** automáticos en fallos
- **Videos** de tests fallidos
- **Trazas** para debugging
- **Setup/teardown** automático de servicios

## Ejecutar Tests

1. **Instalar dependencias:**
```bash
npm install
npm run playwright:install
```

2. **Ejecutar todos los tests:**
```bash
npm run test:e2e
```

3. **Ejecutar tests específicos:**
```bash
npx playwright test auth.spec.ts
npx playwright test page-builder.spec.ts --headed
```

4. **Ver reportes:**
```bash
npx playwright show-report
```

## Variables de Entorno

```bash
REACT_APP_API_URL=http://localhost:3001  # URL del backend
```

## Helpers de Testing

### AuthHelper
```typescript
const auth = new AuthHelper(page);
await auth.register(email, username, password);
await auth.login(email, password);
await auth.ensureLoggedIn();
```

### PageBuilderHelper
```typescript
const builder = new PageBuilderHelper(page);
await builder.createNewPage('Mi Página');
await builder.addComponent('Header');
await builder.editComponent('Header', 'título', 'Mi Sitio');
await builder.publishPage();
await builder.deployPage();
```

## CI/CD

Los tests están preparados para correr en CI con:
- Configuración específica para CI (`process.env.CI`)
- Reintentos automáticos en fallos
- Reportes en múltiples formatos (HTML, JSON)
- Screenshots y videos de fallos

## Debugging

Para debuggear tests:
```bash
npm run test:e2e:headed     # Ver navegador
npm run test:e2e:ui         # Interfaz visual interactiva
npx playwright test --debug # Modo debug paso a paso
```