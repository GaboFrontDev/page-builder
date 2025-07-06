# Ejemplos de Uso - Landing Builder

## 1. Registro y Autenticación

### Registrar Usuario
```bash
curl -X POST http://localhost:3001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@ejemplo.com",
    "username": "juan",
    "password": "mipassword123"
  }'
```

### Iniciar Sesión
```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@ejemplo.com",
    "password": "mipassword123"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## 2. Crear Landing Page

### Crear Página
```bash
# Usar el token del login anterior
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST http://localhost:3001/api/pages/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Mi Empresa - Soluciones Innovadoras",
    "slug": "mi-empresa",
    "description": "Página principal de mi empresa",
    "config": {"theme": "modern"},
    "is_published": true
  }'
```

### Agregar Componente Header
```bash
curl -X POST "http://localhost:3001/api/components/?page_id=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "type": "header",
    "content": {
      "title": "Mi Empresa",
      "logo": "https://miempresa.com/logo.png",
      "menu_items": [
        {"text": "Inicio", "link": "/"},
        {"text": "Servicios", "link": "/servicios"},
        {"text": "Contacto", "link": "/contacto"}
      ]
    },
    "styles": {
      "backgroundColor": "#ffffff",
      "borderBottom": "1px solid #eee"
    },
    "position": 1,
    "is_visible": true
  }'
```

### Agregar Componente Hero
```bash
curl -X POST "http://localhost:3001/api/components/?page_id=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "type": "hero",
    "content": {
      "title": "Transformamos Ideas en Realidad",
      "subtitle": "Soluciones tecnológicas innovadoras para tu empresa",
      "cta_text": "Conocer Más",
      "cta_link": "/servicios",
      "image": "https://miempresa.com/hero-image.jpg"
    },
    "styles": {
      "minHeight": "80vh",
      "backgroundImage": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    "position": 2,
    "is_visible": true
  }'
```

### Agregar Sección de Contenido
```bash
curl -X POST "http://localhost:3001/api/components/?page_id=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "type": "text",
    "content": {
      "text": "<h2>Nuestros Servicios</h2><p>Ofrecemos desarrollo web, aplicaciones móviles y consultoría tecnológica.</p><ul><li>Desarrollo Frontend</li><li>Backend APIs</li><li>DevOps y Cloud</li></ul>",
      "alignment": "center"
    },
    "styles": {
      "padding": "80px 20px",
      "backgroundColor": "#f8f9fa"
    },
    "position": 3,
    "is_visible": true
  }'
```

### Agregar Footer
```bash
curl -X POST "http://localhost:3001/api/components/?page_id=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "type": "footer",
    "content": {
      "text": "© 2024 Mi Empresa. Todos los derechos reservados.",
      "links": [
        {"text": "Privacidad", "url": "/privacidad"},
        {"text": "Términos", "url": "/terminos"}
      ]
    },
    "styles": {
      "backgroundColor": "#333",
      "color": "#fff",
      "padding": "40px 20px"
    },
    "position": 4,
    "is_visible": true
  }'
```

## 3. Deployment

### Deployar la Página
```bash
curl -X POST http://localhost:3001/api/deploy/1 \
  -H "Authorization: Bearer $TOKEN"
```

Respuesta:
```json
{
  "message": "Deployment started",
  "page_id": 1,
  "slug": "mi-empresa",
  "url": "http://mi-empresa.localhost"
}
```

### Verificar Estado del Deployment
```bash
curl -X GET http://localhost:3001/api/deploy/status/mi-empresa
```

## 4. Gestión de Usuario

### Ver Perfil
```bash
curl -X GET http://localhost:3001/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Actualizar Username
```bash
curl -X PUT "http://localhost:3001/api/auth/me?username=nuevo_username" \
  -H "Authorization: Bearer $TOKEN"
```

### Cambiar Contraseña
```bash
curl -X POST "http://localhost:3001/api/auth/change-password?current_password=mipassword123&new_password=nueva_password456" \
  -H "Authorization: Bearer $TOKEN"
```

## 5. Workflow Completo con JavaScript

```javascript
class LandingBuilderClient {
  constructor(baseURL = 'http://localhost:3001') {
    this.baseURL = baseURL;
    this.token = null;
  }

  async register(email, username, password) {
    const response = await fetch(`${this.baseURL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, username, password })
    });
    return response.json();
  }

  async login(email, password) {
    const response = await fetch(`${this.baseURL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    this.token = data.access_token;
    return data;
  }

  async createPage(title, slug, description, theme = 'modern') {
    const response = await fetch(`${this.baseURL}/api/pages/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        title,
        slug,
        description,
        config: { theme },
        is_published: true
      })
    });
    return response.json();
  }

  async addComponent(pageId, type, content, styles = {}, position = 1) {
    const response = await fetch(`${this.baseURL}/api/components/?page_id=${pageId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        type,
        content,
        styles,
        position,
        is_visible: true
      })
    });
    return response.json();
  }

  async deployPage(pageId) {
    const response = await fetch(`${this.baseURL}/api/deploy/${pageId}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });
    return response.json();
  }

  async buildCompleteLandingPage() {
    // 1. Registrar usuario
    await this.register('demo@empresa.com', 'demo', 'demo123');
    
    // 2. Iniciar sesión
    await this.login('demo@empresa.com', 'demo123');
    
    // 3. Crear página
    const page = await this.createPage(
      'Demo Empresa',
      'demo-empresa',
      'Página de demostración',
      'modern'
    );
    
    // 4. Agregar componentes
    await this.addComponent(page.id, 'header', {
      title: 'Demo Empresa',
      menu_items: [
        { text: 'Inicio', link: '/' },
        { text: 'Servicios', link: '/servicios' }
      ]
    }, { backgroundColor: '#fff' }, 1);
    
    await this.addComponent(page.id, 'hero', {
      title: '¡Bienvenido a Demo Empresa!',
      subtitle: 'La mejor solución para tu negocio',
      cta_text: 'Comenzar',
      cta_link: '/contacto'
    }, {}, 2);
    
    await this.addComponent(page.id, 'text', {
      text: '<h2>Nuestros Servicios</h2><p>Ofrecemos las mejores soluciones del mercado.</p>',
      alignment: 'center'
    }, { padding: '60px 20px' }, 3);
    
    // 5. Deployar
    const deployment = await this.deployPage(page.id);
    
    console.log(`✅ Página creada y deployada en: ${deployment.url}`);
    return deployment;
  }
}

// Uso
const client = new LandingBuilderClient();
client.buildCompleteLandingPage();
```

## 6. Acceder al Sitio Generado

Una vez deployada la página, puedes acceder a ella de las siguientes formas:

### Opción 1: Con header Host (funciona inmediatamente)
```bash
curl -H "Host: mi-empresa.localhost" http://localhost/
```

### Opción 2: Configurar DNS local
Agregar a `/etc/hosts` (Linux/Mac) o `C:\Windows\System32\drivers\etc\hosts` (Windows):
```
127.0.0.1 mi-empresa.localhost
```

Luego visitar: http://mi-empresa.localhost

### Opción 3: Usar herramientas como ngrok
```bash
# Instalar ngrok y exponer puerto 80
ngrok http 80
# Usar la URL pública generada
```

## 7. Temas Disponibles

### Default Theme
```json
{"theme": "default"}
```
- Fondo blanco, texto negro
- Fuente sans-serif moderna
- Diseño limpio y minimalista

### Dark Theme
```json
{"theme": "dark"}
```
- Fondo oscuro (#1a1a1a)
- Texto blanco
- Ideal para sitios tecnológicos

### Modern Theme
```json
{"theme": "modern"}
```
- Gradientes modernos
- Efectos de transparencia
- Backdrop filters

### Minimal Theme
```json
{"theme": "minimal"}
```
- Tipografía serif (Georgia)
- Espacios amplios
- Enfoque en contenido

## 8. Tipos de Componentes

### Header
```json
{
  "type": "header",
  "content": {
    "title": "Mi Sitio",
    "logo": "https://ejemplo.com/logo.png",
    "menu_items": [...]
  }
}
```

### Hero
```json
{
  "type": "hero",
  "content": {
    "title": "Título Principal",
    "subtitle": "Subtítulo",
    "cta_text": "Botón",
    "cta_link": "/link",
    "image": "https://ejemplo.com/hero.jpg"
  }
}
```

### Text
```json
{
  "type": "text",
  "content": {
    "text": "<h2>HTML content</h2><p>Párrafo</p>",
    "alignment": "center"
  }
}
```

### Button
```json
{
  "type": "button",
  "content": {
    "text": "Click Me",
    "link": "/destino",
    "variant": "primary"
  }
}
```

### Image
```json
{
  "type": "image",
  "content": {
    "src": "https://ejemplo.com/imagen.jpg",
    "alt": "Descripción",
    "caption": "Pie de foto"
  }
}
```

### Footer
```json
{
  "type": "footer",
  "content": {
    "text": "© 2024 Mi Empresa",
    "links": [
      {"text": "Privacy", "url": "/privacy"}
    ]
  }
}
```