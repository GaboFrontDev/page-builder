#!/usr/bin/env python3
"""
Script para ejecutar tests del generador de sitios estáticos
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr:
                print("STDERR:", result.stderr)
            if result.stdout:
                print("STDOUT:", result.stdout)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Ejecutando Tests del Generador de Sitios Estáticos")
    
    # Cambiar al directorio del backend
    os.chdir('/app')
    
    tests = [
        # Tests del generador básico
        ("python -m pytest test_generator.py::TestSiteGenerator::test_dict_to_css -v", 
         "Test conversión CSS"),
        
        ("python -m pytest test_generator.py::TestSiteGenerator::test_generate_hero_component -v", 
         "Test componente Hero"),
        
        ("python -m pytest test_generator.py::TestSiteGenerator::test_generate_text_component -v", 
         "Test componente Texto"),
        
        ("python -m pytest test_generator.py::TestSiteGenerator::test_generate_button_component -v", 
         "Test componente Botón"),
        
        ("python -m pytest test_generator.py::TestSiteGenerator::test_generate_page -v", 
         "Test generación de página completa"),
        
        ("python -m pytest test_generator.py::TestSiteGenerator::test_deploy_page -v", 
         "Test deployment de página"),
        
        # Tests de componentes específicos
        ("python -m pytest test_generator.py::TestComponentRendering::test_hero_without_optional_fields -v", 
         "Test Hero sin campos opcionales"),
        
        ("python -m pytest test_generator.py::TestComponentRendering::test_button_variants -v", 
         "Test variantes de botón"),
        
        # Tests de manejo de errores
        ("python -m pytest test_generator.py::TestErrorHandling::test_component_with_missing_content -v", 
         "Test manejo de errores"),
        
        # Tests de templates
        ("python -m pytest test_templates.py::TestThemeSystem::test_default_theme -v", 
         "Test tema por defecto"),
        
        ("python -m pytest test_templates.py::TestThemeSystem::test_modern_theme -v", 
         "Test tema moderno"),
        
        ("python -m pytest test_templates.py::TestResponsiveDesign::test_responsive_css_included -v", 
         "Test diseño responsivo"),
    ]
    
    passed = 0
    failed = 0
    
    for cmd, description in tests:
        if run_command(cmd, description):
            passed += 1
        else:
            failed += 1
    
    # Resumen final
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN DE TESTS")
    print(f"{'='*60}")
    print(f"✅ Tests pasados: {passed}")
    print(f"❌ Tests fallados: {failed}")
    print(f"📝 Total: {passed + failed}")
    
    if failed == 0:
        print(f"\n🎉 ¡TODOS LOS TESTS PASARON! 🎉")
        return 0
    else:
        print(f"\n⚠️  Algunos tests fallaron. Revisa los detalles arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main())