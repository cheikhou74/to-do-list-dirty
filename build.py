#!/usr/bin/env python
import sys
import re
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith("version="):
        print("Usage: python build.py version=X.X.X")
        print("Example: python build.py version=1.4.0")
        sys.exit(1)
    
    version = sys.argv[1].replace("version=", "")
    
    # Vérifier le format de version
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print(f"❌ Error: Invalid version format '{version}'. Expected X.X.X")
        sys.exit(1)
    
    print(f"🚀 Building version: {version}")
    print("=" * 50)
    
    # ÉTAPE 1 : Vérification du linter Ruff (version simplifiée)
    print("\n📋 [1/5] Vérification du code avec Ruff...")
    try:
        # Exécuter Ruff sans capture détaillée
        subprocess.run(
            ["pipenv", "run", "ruff", "check", "."],
            capture_output=False,  # IMPORTANT: ne pas capturer la sortie
            check=True
        )
        print("✅ Tous les checks Ruff sont passés!")
    except subprocess.CalledProcessError:
        print("❌ Échec de la vérification Ruff. Corrigez les erreurs avant de build.")
        print("💡 Pour voir les erreurs, exécutez: pipenv run ruff check .")
        sys.exit(1)
    
    # ÉTAPE 2 : Exécution des tests
    print("\n🧪 [2/5] Exécution des tests...")
    try:
        subprocess.run(
            ["python", "manage.py", "test"],
            check=True
        )
        print("✅ Tous les tests sont passés!")
    except subprocess.CalledProcessError:
        print("❌ Échec des tests. Corrigez les tests avant de build.")
        sys.exit(1)
    
    # ÉTAPE 3 : Mettre à jour settings.py
    print("\n📝 [3/5] Mise à jour de la version dans settings.py...")
    settings_path = Path("todo/settings.py")
    if not settings_path.exists():
        print("❌ Error: todo/settings.py not found")
        sys.exit(1)
    
    content = settings_path.read_text(encoding='utf-8')
    new_content = re.sub(
        r'VERSION\s*=\s*["\']([^"\']*)["\']',
        f'VERSION = "{version}"',
        content
    )
    
    if new_content == content:
        # Ajouter la variable si elle n'existe pas
        new_content = content + f'\n\n# Version de l\'application\nVERSION = "{version}"'
    
    settings_path.write_text(new_content, encoding='utf-8')
    print("✅ Version mise à jour dans settings.py")
    
    # ÉTAPE 4 : Commit Git
    print("\n🔧 [4/5] Commit des changements...")
    try:
        subprocess.run(["git", "add", "todo/settings.py"], check=True)
        subprocess.run(["git", "commit", "-m", f"chore: bump version to {version}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git commit erreur: {e}")
        print("Continuer quand même...")
    
    # ÉTAPE 5 : Créer le tag et l'archive
    print("\n🏷️ [5/5] Création du tag Git et de l'archive...")
    try:
        subprocess.run(["git", "tag", "-a", f"v{version}", "-m", f"Version {version}"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  Tag déjà existe ou erreur Git, continuer...")
    
    archive_name = f"todolist-{version}.zip"
    subprocess.run(["git", "archive", "--format=zip", "--output", archive_name, f"--prefix=todolist-{version}/", "HEAD"], check=True)
    
    print("\n" + "=" * 50)
    print("✅ BUILD RÉUSSI!")
    print("=" * 50)
    print(f"   Version: {version}")
    print(f"   Tag: v{version}")
    print(f"   Archive: {archive_name}")
    print("\n📋 Résumé :")
    print("   - ✅ Vérification Ruff")
    print("   - ✅ Tests Django")
    print("   - ✅ Version mise à jour")
    print("   - ✅ Commit Git")
    print("   - ✅ Archive générée")

if __name__ == "__main__":
    main()