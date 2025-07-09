#!/usr/bin/env python3
"""
Debug script to check and rebuild SSG assets
"""
import sys
import subprocess
from pathlib import Path

def check_assets():
    """Check if assets are present and valid"""
    ssg_dir = Path(__file__).parent / "ssg"
    dist_dir = ssg_dir / "dist" / "assets"
    
    print(f"Checking assets in: {dist_dir}")
    
    if not dist_dir.exists():
        print("❌ Assets directory does not exist")
        return False
    
    required_files = ["style.css", "main.js"]
    all_good = True
    
    for file in required_files:
        file_path = dist_dir / file
        if not file_path.exists():
            print(f"❌ Missing: {file}")
            all_good = False
        else:
            size = file_path.stat().st_size
            if size == 0:
                print(f"❌ Empty: {file}")
                all_good = False
            else:
                print(f"✅ Found: {file} ({size} bytes)")
    
    return all_good

def rebuild_assets():
    """Rebuild SSG assets"""
    ssg_dir = Path(__file__).parent / "ssg"
    print(f"Rebuilding assets in: {ssg_dir}")
    
    try:
        subprocess.run(["npm", "run", "build"], cwd=ssg_dir, check=True)
        print("✅ Build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def main():
    print("=== SSG Asset Debugger ===")
    
    if "--rebuild" in sys.argv:
        print("Rebuilding assets...")
        if rebuild_assets():
            print("Checking rebuilt assets...")
            check_assets()
        else:
            print("❌ Rebuild failed")
            sys.exit(1)
    else:
        print("Checking current assets...")
        if not check_assets():
            print("\n💡 Run with --rebuild to rebuild assets")
            sys.exit(1)
        else:
            print("\n✅ All assets are present and valid")

if __name__ == "__main__":
    main()