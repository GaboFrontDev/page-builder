#!/usr/bin/env python3
"""
Script para rebuildar el SSG (Static Site Generator) y actualizar los assets de Tailwind CSS.

Este script:
1. Ejecuta el build del SSG usando Vite
2. Actualiza los assets de todos los sitios deployados
3. Proporciona información sobre el proceso

Uso:
    python build_ssg.py [--update-sites]
    
Opciones:
    --update-sites: Actualiza los assets de todos los sitios deployados existentes
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
from typing import List, Optional


def run_command(cmd: List[str], cwd: Optional[str] = None) -> tuple[bool, str]:
    """Ejecuta un comando y retorna el resultado."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def build_ssg() -> bool:
    """Ejecuta el build del SSG."""
    print("🔨 Construyendo Next.js SSG...")
    
    ssg_dir = Path(__file__).parent / "nextjs-ssg"
    
    # Verificar que el directorio existe
    if not ssg_dir.exists():
        print(f"❌ Error: Directorio SSG no encontrado en {ssg_dir}")
        return False
    
    # Ejecutar npm run build
    success, output = run_command(["npm", "run", "build"], cwd=str(ssg_dir))
    
    if success:
        print("✅ SSG construido exitosamente")
        print(f"📄 Output: {output}")
        
        # Verificar que los assets se generaron
        dist_dir = ssg_dir / "dist"
        if dist_dir.exists():
            assets = list(dist_dir.glob("**/*"))
            print(f"📦 Assets generados: {[f.name for f in assets if f.is_file()]}")
            
            # Verificar tamaños
            for asset in assets:
                if asset.is_file():
                    size = asset.stat().st_size
                    print(f"   - {asset.name}: {size} bytes")
            
            return True
        else:
            print("❌ Error: Directorio dist no encontrado después del build")
            return False
    else:
        print(f"❌ Error en el build: {output}")
        return False


def update_deployed_sites() -> bool:
    """Actualiza los assets de todos los sitios deployados."""
    print("🔄 Actualizando sitios deployados...")
    
    try:
        from nextjs_ssg_generator import NextJSSSGGenerator
        
        # Crear generador
        sites_dir = Path(__file__).parent.parent / "generated-sites"
        generator = NextJSSSGGenerator(str(sites_dir))
        
        updated_count = 0
        
        # Buscar todos los sitios deployados
        for subdomain_dir in sites_dir.iterdir():
            if subdomain_dir.is_dir():
                # Buscar páginas en el subdominio
                for page_dir in subdomain_dir.iterdir():
                    if page_dir.is_dir():
                        # Verificar si tiene assets Next.js
                        assets_dir = page_dir / "_next"
                        if assets_dir.exists():
                            print(f"   📁 Actualizando {subdomain_dir.name}/{page_dir.name}")
                            generator._copy_nextjs_assets(page_dir)
                            updated_count += 1
                    else:
                        # Verificar si es una página root
                        if page_dir.name == "index.html":
                            assets_dir = subdomain_dir / "_next"
                            if assets_dir.exists():
                                print(f"   📁 Actualizando {subdomain_dir.name} (root)")
                                generator._copy_nextjs_assets(subdomain_dir)
                                updated_count += 1
        
        print(f"✅ {updated_count} sitios actualizados")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando sitios: {e}")
        return False


def main():
    """Función principal."""
    print("🚀 Rebuild SSG - Generador de sitios estáticos")
    print("=" * 50)
    
    # Verificar argumentos
    update_sites = "--update-sites" in sys.argv
    
    # Step 1: Build SSG
    if not build_ssg():
        print("❌ Fallo en el build del SSG")
        sys.exit(1)
    
    # Step 2: Update deployed sites if requested
    if update_sites:
        print()
        if not update_deployed_sites():
            print("❌ Fallo actualizando sitios deployados")
            sys.exit(1)
    
    print()
    print("✅ Proceso completado exitosamente!")
    print()
    print("💡 Para actualizar sitios existentes, usa: python build_ssg.py --update-sites")
    print("📚 Los assets se encuentran en: backend/nextjs-ssg/dist/")


if __name__ == "__main__":
    main()