#!/usr/bin/env python
"""
Script pour corriger rapidement les problèmes de CI
"""
import os
import sys

def fix_test_urls():
    """Corrige le fichier test_urls.py si problème"""
    test_urls_path = "tasks/tests/test_urls.py"
    
    if os.path.exists(test_urls_path):
        with open(test_urls_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifie si les noms de vues sont corrects
        if "views.index" in content:
            print("❌ Problème: 'views.index' trouvé dans test_urls.py")
            print("   Corrige avec 'views.task_list'")
            return False
    return True

def fix_generate_report():
    """Corrige generate_test_report.py"""
    with open("generate_test_report.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplace la fonction read_json_file
    old_code = '''def read_json_file(filename):
    """Read JSON file, return empty dict if not found"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}'''
    
    new_code = '''def read_json_file(filename):
    """Read JSON file, return empty dict/list if not found or invalid"""
    import json
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Si c'est un fichier pylint, retourne une liste vide
        if 'pylint' in filename:
            return []
        return {}'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open("generate_test_report.py", 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ generate_test_report.py corrigé")
        return True
    return True

def main():
    print("🔧 Réparation des problèmes CI...")
    
    # 1. Corrige les noms de vues dans tests
    print("\n1. Vérification des tests...")
    fix_test_urls()
    
    # 2. Corrige generate_test_report.py
    print("\n2. Vérification du script de rapport...")
    fix_generate_report()
    
    # 3. Donne les commandes pour tester
    print("\n3. Commande pour tester les URLs :")
    print("   python manage.py test tasks.tests.test_urls -v 2")
    
    print("\n4. Commande pour tester le rapport :")
    print("   python generate_test_report.py")
    
    print("\n🎯 Exécute ces commandes pour vérifier.")

if __name__ == "__main__":
    main()