#!/usr/bin/env python
"""
Script pour exécuter les tests Django et générer un fichier JSON avec les résultats
"""
import json
import os
import sys
import django
from django.test.runner import DiscoverRunner
from io import StringIO

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
django.setup()

class JSONTestRunner(DiscoverRunner):
    """Runner personnalisé qui génère un fichier JSON avec les résultats"""
    
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        print("🔍 Exécution des tests Django...")
        
        # Capturer la sortie standard
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Exécuter les tests normalement
            result = super().run_tests(test_labels, extra_tests, **kwargs)
            
            # Récupérer la sortie
            output = sys.stdout.getvalue()
            
            # Sauvegarder la sortie brute pour débogage
            with open('test_output_raw.txt', 'w', encoding='utf-8') as f:
                f.write(output)
            
            # Analyser les résultats (version simplifiée)
            test_results = self._parse_test_results_simple(output)
            
            # Sauvegarder dans un fichier JSON
            with open('result_test_auto.json', 'w', encoding='utf-8') as f:
                json.dump(test_results, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {test_results['total_tests']} tests exécutés")
            print("✅ Résultats sauvegardés dans result_test_auto.json")
            
            return result
            
        finally:
            sys.stdout = old_stdout
    
    def _parse_test_results_simple(self, output):
        """Version simplifiée pour parser les résultats"""
        lines = output.split('\n')
        
        # Initialiser les résultats
        results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'test_cases': []
        }
        
        # Chercher la ligne de résumé
        for line in lines:
            if 'Ran' in line and 'test' in line and 'in' in line:
                # Exemple: "Ran 3 tests in 0.123s"
                parts = line.split()
                for part in parts:
                    if part.isdigit():
                        results['total_tests'] = int(part)
                        break
            
            if 'OK' in line:
                results['passed'] = results['total_tests']
            elif 'FAILED' in line:
                # Compter les échecs (simplifié)
                results['failed'] = results['total_tests'] - results.get('passed', 0)
        
        return results

def main():
    """Fonction principale"""
    print("=" * 50)
    print("   GÉNÉRATION DE RAPPORT JSON DES TESTS")
    print("=" * 50)
    
    # Créer le runner personnalisé
    runner = JSONTestRunner()
    
    # Exécuter les tests pour l'application 'tasks'
    print("\n📋 Exécution des tests pour l'application 'tasks'...")
    runner.run_tests(['tasks'])
    
    print("\n" + "=" * 50)
    print("   TERMINÉ!")
    print("=" * 50)
    
    # Afficher le contenu du fichier JSON généré
    if os.path.exists('result_test_auto.json'):
        print("\n📄 Contenu du fichier result_test_auto.json :")
        with open('result_test_auto.json', 'r', encoding='utf-8') as f:
            print(f.read())

if __name__ == '__main__':
    main()