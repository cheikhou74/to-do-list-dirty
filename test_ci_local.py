#!/usr/bin/env python
"""
Script simplifié pour tester localement avant de pousser sur GitHub
"""
import subprocess
import os

def run_command(cmd):
    """Exécute une commande et retourne le résultat"""
    print(f"\n▶️  Exécution: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Erreur: {result.stderr[:200]}")
    else:
        print("✅ Succès")
    return result.returncode

def main():
    print("🚀 Test local de la CI/CD Pipeline")
    print("=" * 50)
    
    commands = [
        "pylint tasks/ --exit-zero --output-format=json:pylint_report.json",
        "python manage.py test tasks.tests --noinput --verbosity=2",
        "python generate_test_report.py",
        "python generate_pdf_report.py"
    ]
    
    all_pass = True
    for cmd in commands:
        if run_command(cmd) != 0:
            all_pass = False
    
    if all_pass:
        print("\n🎉 Tous les tests locaux ont réussi!")
        print("Tu peux maintenant pousser sur GitHub.")
    else:
        print("\n⚠️  Certains tests ont échoué. Corrige avant de pousser.")

if __name__ == "__main__":
    main()