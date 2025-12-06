#!/usr/bin/env python
"""
Script de rapport de tests avec pourcentages (Exercices 5 & 6)
Mis à jour pour inclure les tests Selenium (Exercice 11)
"""
import yaml
import json
import sys

def load_yaml_tests():
    """Charger les tests depuis le fichier YAML"""
    try:
        with open('test_list.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("❌ Fichier test_list.yaml introuvable")
        print("Assurez-vous qu'il est dans le même dossier que ce script.")
        return None
    except yaml.YAMLError as e:
        print(f"❌ Erreur YAML: {e}")
        return None

def load_json_results():
    """Charger les résultats des tests Django depuis le JSON"""
    try:
        with open('result_test_auto.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  Fichier result_test_auto.json introuvable")
        print("Tous les tests Django auto seront marqués comme 'Not found'")
        return {"tests": []}

def load_selenium_results():
    """Charger les résultats des tests Selenium depuis le JSON (EXERCICE 11)"""
    try:
        with open('result_test_selenium.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  Fichier result_test_selenium.json introuvable")
        print("Tous les tests Selenium auto seront marqués comme 'Not found'")
        return {"tests": []}

def normalize_test_id(test_id):
    """Normaliser l'ID du test (TC001 format)"""
    if isinstance(test_id, int):
        return f"TC{test_id:03d}"
    elif isinstance(test_id, str) and test_id.isdigit():
        return f"TC{int(test_id):03d}"
    return test_id

def generate_report(yaml_tests, json_results):
    """Générer le rapport visuel avec statistiques"""
    print("📊 RAPPORT DES TESTS")
    print("=" * 50)
    
    if not yaml_tests or "tests" not in yaml_tests:
        print("❌ Aucun test trouvé dans le YAML")
        return
    
    tests = yaml_tests["tests"]
    
    # Charger les résultats Selenium (EXERCICE 11)
    selenium_results = load_selenium_results()
    
    # Créer un dictionnaire des résultats Django
    django_results_dict = {}
    for test in json_results.get("tests", []):
        django_results_dict[normalize_test_id(test["id"])] = test["status"]
    
    # Créer un dictionnaire des résultats Selenium (EXERCICE 11)
    selenium_results_dict = {}
    for test in selenium_results.get("tests", []):
        selenium_results_dict[normalize_test_id(test["id"])] = test["status"]
    
    # Initialiser les compteurs
    stats = {
        "total": len(tests),
        "passed": 0,
        "failed": 0,
        "not_found": 0,
        "manual": 0,
        "passed_and_manual": 0,
        "selenium_passed": 0,  # EXERCICE 11: compteur spécifique Selenium
        "selenium_failed": 0,   # EXERCICE 11: compteur spécifique Selenium
        "selenium_not_found": 0 # EXERCICE 11: compteur spécifique Selenium
    }
    
    # Afficher chaque test
    for test in tests:
        test_id = normalize_test_id(test.get("id", "INCONNU"))
        test_type = test.get("type", "auto-unittest")
        
        if test_type == "manuel":
            status_symbol = "🫱Manual test needed"
            stats["manual"] += 1
        elif test_type == "auto-selenium":
            # EXERCICE 11: Chercher le résultat dans les tests Selenium
            status = selenium_results_dict.get(test_id)
            if status == "passed":
                status_symbol = "🌐Passed (Selenium)"
                stats["passed"] += 1
                stats["passed_and_manual"] += 1
                stats["selenium_passed"] += 1
            elif status == "failed":
                status_symbol = "🌐Failed (Selenium)"
                stats["failed"] += 1
                stats["selenium_failed"] += 1
            else:
                status_symbol = "🌐Not found (Selenium)"
                stats["not_found"] += 1
                stats["selenium_not_found"] += 1
        else:  # auto-unittest ou auto-django
            # Chercher le résultat dans le JSON Django
            status = django_results_dict.get(test_id)
            if status == "passed":
                status_symbol = "✅Passed"
                stats["passed"] += 1
                stats["passed_and_manual"] += 1
            elif status == "failed":
                status_symbol = "❌Failed"
                stats["failed"] += 1
            else:
                status_symbol = "🕳️Not found"
                stats["not_found"] += 1
        
        # Afficher la ligne du test
        print(f"{test_id} | {test_type} | {status_symbol}")
    
    # Calculer les pourcentages
    if stats["total"] > 0:
        stats["passed_pct"] = (stats["passed"] / stats["total"]) * 100
        stats["failed_pct"] = (stats["failed"] / stats["total"]) * 100
        stats["not_found_pct"] = (stats["not_found"] / stats["total"]) * 100
        stats["manual_pct"] = (stats["manual"] / stats["total"]) * 100
        stats["passed_and_manual_pct"] = ((stats["passed"] + stats["manual"]) / stats["total"]) * 100
        
        # EXERCICE 11: Pourcentages spécifiques Selenium
        total_selenium = stats["selenium_passed"] + stats["selenium_failed"] + stats["selenium_not_found"]
        if total_selenium > 0:
            stats["selenium_passed_pct"] = (stats["selenium_passed"] / total_selenium) * 100
            stats["selenium_failed_pct"] = (stats["selenium_failed"] / total_selenium) * 100
            stats["selenium_not_found_pct"] = (stats["selenium_not_found"] / total_selenium) * 100
        else:
            stats["selenium_passed_pct"] = 0
            stats["selenium_failed_pct"] = 0
            stats["selenium_not_found_pct"] = 0
    else:
        stats["passed_pct"] = stats["failed_pct"] = stats["not_found_pct"] = 0
        stats["manual_pct"] = stats["passed_and_manual_pct"] = 0
        stats["selenium_passed_pct"] = stats["selenium_failed_pct"] = stats["selenium_not_found_pct"] = 0
    
    # Afficher les statistiques (Exercice 6)
    print("\n" + "=" * 50)
    print("📈 STATISTIQUES")
    print("=" * 50)
    print(f"Number of tests: {stats['total']}")
    print(f"✅ Passed tests: {stats['passed']} ({stats['passed_pct']:.1f}%)")
    print(f"❌ Failed tests: {stats['failed']} ({stats['failed_pct']:.1f}%)")
    print(f"🕳️ Not found tests: {stats['not_found']} ({stats['not_found_pct']:.1f}%)")
    print(f"🫱 Test to pass manually: {stats['manual']} ({stats['manual_pct']:.1f}%)")
    print(f"✅ Passed + 🫱 Manual: {stats['passed'] + stats['manual']} ({stats['passed_and_manual_pct']:.1f}%)")
    
    # EXERCICE 11: Statistiques spécifiques pour Selenium
    total_selenium = stats["selenium_passed"] + stats["selenium_failed"] + stats["selenium_not_found"]
    if total_selenium > 0:
        print("\n" + "=" * 50)
        print("🌐 STATISTIQUES SELENIUM (E2E)")
        print("=" * 50)
        print(f"Total tests Selenium: {total_selenium}")
        print(f"🌐 Passed Selenium: {stats['selenium_passed']} ({stats['selenium_passed_pct']:.1f}%)")
        print(f"🌐 Failed Selenium: {stats['selenium_failed']} ({stats['selenium_failed_pct']:.1f}%)")
        print(f"🌐 Not found Selenium: {stats['selenium_not_found']} ({stats['selenium_not_found_pct']:.1f}%)")
        
        # Taux de réussite Selenium
        selenium_success_rate = stats["selenium_passed_pct"]
        print(f"🎯 Taux de réussite Selenium: {selenium_success_rate:.1f}%")
        
        if selenium_success_rate >= 80:
            print("   🎉 Excellent taux de réussite pour les tests E2E !")
        elif selenium_success_rate >= 60:
            print("   👍 Bon taux de réussite pour les tests E2E")
        elif selenium_success_rate >= 40:
            print("   ⚠️  Taux de réussite acceptable pour les tests E2E")
        else:
            print("   ❌ Taux de réussite faible pour les tests E2E")
    
    # Recommandations basées sur les résultats Selenium
    print("\n" + "=" * 50)
    print("💡 RECOMMANDATIONS")
    print("=" * 50)
    
    if stats["selenium_not_found"] > 0:
        print(f"⚠️  {stats['selenium_not_found']} test(s) Selenium marqué(s) 'auto-selenium' non trouvé(s)")
        print("   Assurez-vous d'avoir exécuté selenium_tests.py et qu'il génère result_test_selenium.json")
    
    if stats["selenium_failed"] > 0:
        print(f"🔧 {stats['selenium_failed']} test(s) Selenium ont échoué. Vérifiez votre application web.")
    
    if total_selenium == 0:
        print("🌐 Aucun test Selenium trouvé. Pour ajouter des tests E2E:")
        print("   1. Ajoutez des tests avec type: 'auto-selenium' dans test_list.yaml")
        print("   2. Exécutez selenium_tests.py pour générer les résultats")

def main():
    """Fonction principale"""
    print("🧪 LECTURE DES TESTS AUTO VIA RESULT_TEST_AUTO.JSON...")
    print("🌐 LECTURE DES TESTS SELENIUM VIA RESULT_TEST_SELENIUM.JSON...")
    
    # 1. Charger les tests YAML
    yaml_tests = load_yaml_tests()
    if not yaml_tests:
        return 1
    
    # 2. Charger les résultats JSON Django
    json_results = load_json_results()
    
    # 3. Générer le rapport
    generate_report(yaml_tests, json_results)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())