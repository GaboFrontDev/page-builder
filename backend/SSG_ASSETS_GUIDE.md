# Guía de Assets del SSG (Static Site Generator)

## Resumen del Problema

El sistema de generación de sitios estáticos no estaba copiando correctamente los assets compilados de Tailwind CSS desde `backend/ssg/dist/assets/` hacia los sitios generados en `generated-sites/`, lo que causaba que los estilos no se aplicaran correctamente.

## Arquitectura del Sistema

### 1. Estructura de Directorios

```
backend/
├── ssg/                          # Sistema de generación estática con React
│   ├── src/
│   │   ├── index.tsx            # Punto de entrada del SSG
│   │   ├── index.css            # Estilos base con Tailwind
│   │   └── Page.tsx             # Componente principal de página
│   ├── dist/                    # Assets compilados (generados por Vite)
│   │   └── assets/
│   │       ├── main.js          # JavaScript compilado
│   │       └── style.css        # CSS compilado con Tailwind
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.cjs
├── templates/                   # Sistema legacy de generación
│   └── assets/
│       ├── style.css           # CSS básico
│       └── test.css            # CSS de prueba
├── generator.py                 # Generador legacy (Jinja2)
├── ssg_generator.py            # Generador React SSG
└── routers/
    └── deployment.py           # Endpoints de deployment
```

### 2. Flujo de Generación

1. **Build del SSG**: `npm run build` en `backend/ssg/`
2. **Generación de HTML**: React SSG renderiza componentes a HTML
3. **Copia de Assets**: Los assets se copian desde `ssg/dist/assets/` a cada sitio generado

## Componentes Principales

### 1. ReactSSGGenerator (ssg_generator.py)

```python
class ReactSSGGenerator:
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or "/var/www/sites")
        self.ssg_dir = Path(__file__).parent / "ssg"
    
    def _copy_assets(self, target_dir: Path):
        """Copia assets desde ssg/dist/assets/ al directorio objetivo"""
        ssg_assets = self.ssg_dir / "dist" / "assets"
        if ssg_assets.exists():
            target_assets = target_dir / "assets"
            if target_assets.exists():
                shutil.rmtree(target_assets)
            shutil.copytree(ssg_assets, target_assets)
```

### 2. Configuración de Vite (vite.config.ts)

```typescript
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name].js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name].[ext]'
      }
    }
  }
})
```

### 3. Configuración de Tailwind (tailwind.config.cjs)

```javascript
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./templates/**/*.{js,ts,jsx,tsx}",
    "../shared/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: { /* colores personalizados */ }
      }
    }
  }
}
```

## Proceso de Deployment

### 1. Configuración del Generador

En `deployment.py`:

```python
# Seleccionar generador basado en variable de entorno
USE_REACT_SSG = os.getenv("USE_REACT_SSG", "true").lower() == "true"
if USE_REACT_SSG:
    generator = ReactSSGGenerator()
else:
    generator = SiteGenerator()  # Legacy
```

### 2. Flujo de Deployment

1. **Endpoint llamado**: `POST /api/deploy/{page_id}`
2. **Verificaciones**: Usuario autorizado, página publicada
3. **Tarea en background**: `deploy_page_task(page, db)`
4. **Generación**: `generator.deploy_page(page, db)`
5. **Copia de assets**: `generator._copy_assets(page_dir)`

## Scripts de Automatización

### build_ssg.py

Script para rebuildar el SSG y actualizar sitios existentes:

```bash
# Solo rebuild
python build_ssg.py

# Rebuild + actualizar sitios existentes
python build_ssg.py --update-sites
```

**Funcionalidades**:
- Ejecuta `npm run build` en el directorio SSG
- Verifica que los assets se generen correctamente
- Opcionalmente actualiza todos los sitios deployados
- Proporciona información detallada del proceso

## Comandos Útiles

### Desarrollo

```bash
# Entrar al directorio SSG
cd backend/ssg

# Instalar dependencias
npm install

# Build de desarrollo
npm run build

# Ver assets generados
ls -la dist/assets/

# Rebuild completo con actualización de sitios
python build_ssg.py --update-sites
```

### Troubleshooting

```bash
# Limpiar y reinstalar dependencias
rm -rf node_modules package-lock.json
npm install

# Verificar configuración de Tailwind
npx tailwindcss -i src/index.css -o dist/test.css --watch

# Verificar que los assets se copien correctamente
python -c "
from ssg_generator import ReactSSGGenerator
generator = ReactSSGGenerator()
generator._copy_assets(Path('test-output'))
"
```

## Solución del Problema

### Problema Identificado

1. **Assets desactualizados**: Los assets en `ssg/dist/` no se rebuildeaban automáticamente
2. **Dependencias rotas**: Faltaba `@rollup/rollup-darwin-arm64` en node_modules
3. **Proceso manual**: No había script automatizado para rebuild

### Solución Implementada

1. **Reinstalación de dependencias**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Rebuild de assets**:
   ```bash
   npm run build
   ```

3. **Script de automatización**: `build_ssg.py` para facilitar el proceso

4. **Actualización de sitios existentes**: Comando para actualizar assets en sitios ya deployados

### Verificación

```bash
# Verificar que el CSS contiene clases de Tailwind
grep -o "text-center\|bg-blue-600\|flex\|px-4" generated-sites/*/assets/style.css

# Verificar tamaño de assets
ls -la backend/ssg/dist/assets/
# style.css: ~12KB (compilado con Tailwind)
# main.js: ~83KB (React + SSR)
```

## Mantenimiento

### Actualización de Estilos

1. Modificar `backend/ssg/src/index.css`
2. Ejecutar `python build_ssg.py --update-sites`
3. Verificar que los sitios se actualicen correctamente

### Actualización de Componentes

1. Modificar componentes en `backend/ssg/src/`
2. Ejecutar `npm run build` en `backend/ssg/`
3. Los nuevos deployments usarán automáticamente los assets actualizados

### Monitoreo

- Verificar que `backend/ssg/dist/assets/` contenga los assets actualizados
- Comprobar que los sitios nuevos tengan los estilos correctos
- Usar `build_ssg.py` para mantener sitios existentes actualizados

## Conclusión

El sistema ahora funciona correctamente:

1. ✅ **Assets compilados**: Vite genera correctamente los assets de Tailwind
2. ✅ **Copia automática**: Los assets se copian a cada sitio generado
3. ✅ **Proceso automatizado**: Script `build_ssg.py` facilita el mantenimiento
4. ✅ **Sitios actualizados**: Los sitios existentes pueden actualizarse fácilmente

El flujo completo desde el build hasta la generación final funciona correctamente, asegurando que los estilos de Tailwind CSS se apliquen correctamente en todos los sitios generados.