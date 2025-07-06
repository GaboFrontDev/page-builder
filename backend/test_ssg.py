#!/usr/bin/env python3
"""
Test script for the new React SSG system
"""

import json
import sys
from pathlib import Path
from ssg_generator import ReactSSGGenerator

def test_ssg_system():
    """Test the React SSG system with sample data"""
    
    # Sample page data that would normally come from the database
    sample_page_data = {
        "id": 1,
        "title": "Test Page - React SSG",
        "description": "Una página de prueba generada con React SSG",
        "slug": "test-react-ssg",
        "subdomain": "testsite",
        "config": {
            "theme": "modern"
        },
        "components": [
            {
                "id": 1,
                "type": "header",
                "content": {
                    "title": "Mi Sitio Web",
                    "logo": "",
                    "menu_items": [
                        {"text": "Inicio", "link": "#"},
                        {"text": "Servicios", "link": "#servicios"},
                        {"text": "Contacto", "link": "#contacto"}
                    ]
                },
                "styles": {},
                "position": 0,
                "is_visible": True
            },
            {
                "id": 2,
                "type": "hero",
                "content": {
                    "title": "Bienvenido a nuestro sitio",
                    "subtitle": "Creamos experiencias digitales increíbles con React SSG",
                    "cta_text": "Conoce más",
                    "cta_link": "#servicios"
                },
                "styles": {},
                "position": 1,
                "is_visible": True
            },
            {
                "id": 3,
                "type": "text",
                "content": {
                    "text": "<h2>Nuestros Servicios</h2><p>Ofrecemos soluciones modernas para tu negocio:</p><ul><li>Desarrollo web con React</li><li>Generación estática de sitios (SSG)</li><li>Optimización para motores de búsqueda</li></ul>",
                    "alignment": "center"
                },
                "styles": {"padding": "60px 20px"},
                "position": 2,
                "is_visible": True
            },
            {
                "id": 4,
                "type": "button",
                "content": {
                    "text": "Contáctanos",
                    "link": "#contacto",
                    "variant": "primary"
                },
                "styles": {},
                "position": 3,
                "is_visible": True
            },
            {
                "id": 5,
                "type": "footer",
                "content": {
                    "text": "© 2024 Mi Sitio Web. Todos los derechos reservados.",
                    "links": [
                        {"text": "Política de Privacidad", "url": "#"},
                        {"text": "Términos de Uso", "url": "#"}
                    ]
                },
                "styles": {},
                "position": 4,
                "is_visible": True
            }
        ]
    }
    
    print("🚀 Probando el sistema React SSG...")
    
    # Initialize the generator
    generator = ReactSSGGenerator("/tmp/test_ssg_output")
    
    try:
        # Test the Node.js rendering
        print("📦 Generando HTML con React SSG...")
        html_content = generator._render_with_node(sample_page_data)
        
        print("✅ HTML generado exitosamente!")
        print(f"📄 Longitud del HTML: {len(html_content)} caracteres")
        
        # Save the result to a file for inspection
        output_file = Path("/tmp/test_react_ssg_output.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 HTML guardado en: {output_file}")
        
        # Show a preview of the generated HTML
        print("\n📋 Vista previa del HTML generado:")
        print("=" * 50)
        preview_lines = html_content.split('\n')[:20]
        for line in preview_lines:
            print(line)
        if len(html_content.split('\n')) > 20:
            print("... (contenido truncado)")
        print("=" * 50)
        
        # Check if the HTML contains expected elements
        checks = [
            ("DOCTYPE html", "Declaración DOCTYPE"),
            ("Mi Sitio Web", "Título del header"),
            ("Bienvenido a nuestro sitio", "Título del hero"),
            ("Nuestros Servicios", "Sección de servicios"),
            ("Contáctanos", "Botón de contacto"),
            ("Todos los derechos reservados", "Footer")
        ]
        
        print("\n🔍 Verificando contenido:")
        all_passed = True
        for check_text, description in checks:
            if check_text in html_content:
                print(f"✅ {description}: encontrado")
            else:
                print(f"❌ {description}: NO encontrado")
                all_passed = False
        
        if all_passed:
            print("\n🎉 ¡Todas las verificaciones pasaron! El sistema React SSG funciona correctamente.")
        else:
            print("\n⚠️  Algunas verificaciones fallaron. Revisa el HTML generado.")
            
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ssg_system()
    sys.exit(0 if success else 1)