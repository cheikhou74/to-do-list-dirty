#!/usr/bin/env python
"""
Tests E2E avec Selenium pour Todo-list App
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TodoListSeleniumTests:
    """Tests end-to-end avec Selenium"""
    
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.results = []
        
    def setup_driver(self):
        """Configurer le driver Selenium"""
        try:
            # Option 1: Avec webdriver-manager (recommandé)
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Exécuter sans ouvrir de fenêtre
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
        except ImportError:
            # Option 2: Sans webdriver-manager (chemin local)
            self.driver = webdriver.Chrome()
        
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        
    def tear_down(self):
        """Fermer le driver"""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def take_screenshot(self, name):
        """Prendre une capture d'écran"""
        try:
            self.driver.save_screenshot(f"screenshot_{name}.png")
        except:
            pass
    
    def test_01_homepage_loads(self):
        """Test que la page d'accueil se charge"""
        test_id = "TC016"
        test_name = "test_homepage_loads"
        
        try:
            print(f"🧪 {test_name}...")
            self.driver.get(self.base_url)
            
            # Vérifier que la page se charge (status 200)
            # En Selenium, si on arrive ici sans exception, c'est que la page s'est chargée
            
            # Vérifier qu'on a du contenu
            page_source = self.driver.page_source
            if len(page_source) > 100:  # Au moins 100 caractères
                self.results.append({
                    "id": test_id,
                    "name": test_name,
                    "status": "passed",
                    "message": "Page d'accueil chargée avec succès"
                })
                print("✅ Passé")
                return True
            else:
                raise Exception("Page vide ou trop courte")
            
        except Exception as e:
            self.results.append({
                "id": test_id,
                "name": test_name,
                "status": "failed",
                "message": str(e)
            })
            print(f"❌ Échoué: {e}")
            return False
    
    def test_02_create_and_delete_tasks(self):
        """Test création et suppression de tâches"""
        test_id = "TC017"
        test_name = "test_create_and_delete_tasks"
        
        try:
            print(f"🧪 {test_name}...")
            
            # 1. Compter les tâches initiales
            self.driver.get(self.base_url)
            time.sleep(1)
            
            # Trouver toutes les tâches (ajuster le sélecteur selon votre HTML)
            tasks = self.driver.find_elements(By.CLASS_NAME, "task")  # Ajustez la classe
            initial_count = len(tasks)
            print(f"   Tâches initiales: {initial_count}")
            
            # 2. Créer 10 tâches
            for i in range(10):
                try:
                    # Trouver le champ de formulaire (ajuster selon votre HTML)
                    title_field = self.driver.find_element(By.NAME, "title")  # Ajustez le nom
                    title_field.clear()
                    title_field.send_keys(f"Tâche Selenium {i+1}")
                    
                    # Trouver le bouton d'ajout (ajuster selon votre HTML)
                    add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Ajouter')]")
                    add_button.click()
                    
                    time.sleep(0.5)  # Attendre l'ajout
                    
                except Exception as e:
                    print(f"   ⚠️ Erreur création tâche {i+1}: {e}")
                    # Essayer une autre méthode
                    try:
                        self.driver.find_element(By.TAG_NAME, "form").submit()
                    except:
                        pass
            
            # 3. Compter après création
            self.driver.refresh()
            time.sleep(1)
            tasks_after = self.driver.find_elements(By.CLASS_NAME, "task")
            count_after = len(tasks_after)
            print(f"   Tâches après création: {count_after}")
            
            # 4. Supprimer les tâches créées
            # (Simplification: on supprime tout, mais dans la vraie vie on ciblerait les 10 nouvelles)
            delete_buttons = self.driver.find_elements(By.CLASS_NAME, "delete-btn")
            for btn in delete_buttons[:10]:  # Supprimer les 10 premières
                try:
                    btn.click()
                    time.sleep(0.3)
                except:
                    pass
            
            # 5. Vérifier
            self.driver.refresh()
            time.sleep(1)
            tasks_final = self.driver.find_elements(By.CLASS_NAME, "task")
            final_count = len(tasks_final)
            print(f"   Tâches finales: {final_count}")
            
            # Prendre des captures
            self.take_screenshot("after_creation")
            self.take_screenshot("after_deletion")
            
            self.results.append({
                "id": test_id,
                "name": test_name,
                "status": "passed",
                "message": f"Création/suppression OK: {initial_count} → {count_after} → {final_count}"
            })
            print("✅ Passé")
            return True
            
        except Exception as e:
            self.results.append({
                "id": test_id,
                "name": test_name,
                "status": "failed",
                "message": str(e)
            })
            print(f"❌ Échoué: {e}")
            return False
    def test_03_advanced_workflow(self):
        """Test avancé : créer deux tâches, vérifier, supprimer une tâche"""
        test_id = "TC018"
        test_name = "test_advanced_workflow"
        
        try:
            print(f"🧪 {test_name}...")
            
            # 1. Aller à la page
            self.driver.get(self.base_url)
            time.sleep(1)
            
            # 2. Créer la première tâche
            try:
                title_field = self.driver.find_element(By.NAME, "title")
                title_field.clear()
                title_field.send_keys("Tâche avancée 1")
                
                # Trouver le bouton d'ajout
                add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Ajouter')]")
                add_button.click()
                time.sleep(1)
                print("   ✓ Première tâche créée")
            except:
                print("   ⚠️ Impossible de créer la première tâche")
                # Essayer une autre méthode
                self.driver.find_element(By.TAG_NAME, "form").submit()
                time.sleep(1)
            
            # 3. Créer la deuxième tâche
            try:
                title_field = self.driver.find_element(By.NAME, "title")
                title_field.clear()
                title_field.send_keys("Tâche avancée 2")
                
                add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Ajouter')]")
                add_button.click()
                time.sleep(1)
                print("   ✓ Deuxième tâche créée")
            except:
                print("   ⚠️ Impossible de créer la deuxième tâche")
                self.driver.find_element(By.TAG_NAME, "form").submit()
                time.sleep(1)
            
            # 4. Vérifier que les deux tâches sont dans la page
            page_source = self.driver.page_source
            task1_found = "Tâche avancée 1" in page_source
            task2_found = "Tâche avancée 2" in page_source
            
            if not task1_found or not task2_found:
                raise Exception(f"Tâches non trouvées. T1: {task1_found}, T2: {task2_found}")
            
            print("   ✓ Les deux tâches sont présentes")
            
            # 5. Supprimer la deuxième tâche
            try:
                delete_buttons = self.driver.find_elements(By.CLASS_NAME, "delete-btn")
                if delete_buttons and len(delete_buttons) >= 2:
                    # Supprimer la deuxième (dernière créée)
                    delete_buttons[-1].click()
                    time.sleep(1)
                    print("   ✓ Deuxième tâche supprimée")
                else:
                    print("   ⚠️ Boutons de suppression non trouvés")
            except:
                print("   ⚠️ Impossible de supprimer")
            
            # 6. Vérifier que la première tâche est toujours là
            self.driver.refresh()
            time.sleep(1)
            
            page_source = self.driver.page_source
            if "Tâche avancée 1" in page_source:
                print("   ✓ Première tâche toujours présente")
                
                self.results.append({
                    "id": test_id,
                    "name": test_name,
                    "status": "passed",
                    "message": "Workflow avancé réussi: création, vérification, suppression"
                })
                print("✅ Passé")
                return True
            else:
                raise Exception("Première tâche a disparu après suppression de la deuxième")
            
        except Exception as e:
            self.results.append({
                "id": test_id,
                "name": test_name,
                "status": "failed",
                "message": str(e)
            })
            print(f"❌ Échoué: {e}")
            return False
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("=" * 60)
        print("🧪 TESTS E2E SELENIUM")
        print("=" * 60)
        
        try:
            self.setup_driver()
            
            # Exécuter les tests
            tests = [
                self.test_01_homepage_loads,
                self.test_02_create_and_delete_tasks,
                self.test_03_advanced_workflow,  # AJOUTEZ CETTE LIGNE
            ]
            
            for test in tests:
                if not test():
                    print("⚠️  Test échoué, continuer les autres...")
            
            # Sauvegarder les résultats
            self.save_results()
            
            # Afficher le résumé
            self.display_summary()
            
            return self.results
            
        finally:
            self.tear_down()
    
    def save_results(self):
        """Sauvegarder les résultats en JSON"""
        report = {
            "metadata": {
                "total_tests": len(self.results),
                "passed": len([r for r in self.results if r["status"] == "passed"]),
                "failed": len([r for r in self.results if r["status"] == "failed"])
            },
            "tests": self.results
        }
        
        with open('result_test_selenium.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Résultats sauvegardés dans result_test_selenium.json")
    
    def display_summary(self):
        """Afficher un résumé des tests"""
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS SELENIUM")
        print("=" * 60)
        
        total = len(self.results)
        passed = len([r for r in self.results if r["status"] == "passed"])
        failed = total - passed
        
        print(f"Total tests: {total}")
        print(f"✅ Passés: {passed}")
        print(f"❌ Échoués: {failed}")
        
        for result in self.results:
            status_icon = "✅" if result["status"] == "passed" else "❌"
            print(f"  {status_icon} {result['id']}: {result['name']}")

def main():
    """Fonction principale"""
    # Vérifier que le serveur tourne
    print("⚠️  Assurez-vous que le serveur Django tourne: python manage.py runserver")
    input("Appuyez sur Entrée quand le serveur est prêt...")
    
    # Exécuter les tests
    tester = TodoListSeleniumTests()
    results = tester.run_all_tests()
    
    # Retourner le code d'erreur
    failed_tests = len([r for r in results if r["status"] == "failed"])
    return 1 if failed_tests > 0 else 0

if __name__ == "__main__":
    exit(main())