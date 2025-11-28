#!/usr/bin/env python
import sys
import re
import subprocess
from pathlib import Path

def run_command(command, error_message):
    """Exécute une commande et gère les erreurs"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {error_message}")
        print(f"Erreur: {e.stderr}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith("version="):
        print("Usage: python build.py version=X.X.X")
        print("Example: python build.py version=1.1.0")
        sys.exit(1)
    
    version = sys.argv[1].replace("version=", "")
    
    # Vérifier le format de version
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print(f"❌ Error: Invalid version format '{version}'. Expected X.X.X")
        sys.exit(1)
    
    print(f"🚀 Building version: {version}")
    print("=" * 50)
    
    # ÉTAPE 1 : Vérification du linter Ruff
    print("\n📋 [1/5] Vérification du code avec Ruff...")
    ruff_result = run_command(
        "pipenv run ruff check .",
        "Échec de la vérification Ruff. Corrigez les erreurs avant de build."
    )
    print("✅ Tous les checks Ruff sont passés!")
    
    # ÉTAPE 2 : Mettre à jour settings.py
    print("\n📝 [2/5] Mise à jour de la version dans settings.py...")
    settings_path = Path("todo/settings.py")
    if not settings_path.exists():
        print("❌ Error: todo/settings.py not found")
        sys.exit(1)
    
    content = settings_path.read_text()
    new_content = re.sub(
        r'VERSION\s*=\s*["\']([^"\']*)["\']',
        f'VERSION = "{version}"',
        content
    )
    
    if new_content == content:
        # Ajouter la variable si elle n'existe pas
        new_content = content + f'\n\n# Version de l\'application\nVERSION = "{version}"'
    
    settings_path.write_text(new_content)
    print("✅ Version mise à jour dans settings.py")
    
    # ÉTAPE 3 : Commit Git
    print("\n🔧 [3/5] Commit des changements...")
    subprocess.run(["git", "add", "todo/settings.py"], check=True)
    subprocess.run(["git", "commit", "-m", f"chore: bump version to {version}"], check=False)
    
    # ÉTAPE 4 : Créer le tag
    print("\n🏷️ [4/5] Création du tag Git...")
    subprocess.run(["git", "tag", "-a", f"v{version}", "-m", f"Version {version}"], check=True)
    
    # ÉTAPE 5 : Créer l'archive
    print("\n📦 [5/5] Création de l'archive...")
    archive_name = f"todolist-{version}.zip"
    subprocess.run(["git", "archive", "--format=zip", "--output", archive_name, f"--prefix=todolist-{version}/", "HEAD"], check=True)
    
    print("\n" + "=" * 50)
    print("✅ BUILD RÉUSSI!")
    print("=" * 50)
    print(f"   Version: {version}")
    print(f"   Tag: v{version}")
    print(f"   Archive: {archive_name}")
    
    # Vérification finale
    print(f"\n🔍 Vérification finale:")
    subprocess.run(["python", "-c", f"from todo import settings; print('   Version actuelle:', settings.VERSION)"])

if __name__ == "__main__":
    main()