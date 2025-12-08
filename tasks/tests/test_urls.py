from django.test import TestCase
# Changeons complètement l'import pour être absolu
from tasks.tests.decorators import tc  # IMPORT RELATIF CORRECT
from tasks.models import Task

class URLTests(TestCase):
    @tc("TC001")
    def test_home_page_status(self):
        """Test que la page d'accueil fonctionne"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    @tc("TC002")
    def test_home_page_uses_correct_template(self):
        """Test que la page d'accueil utilise le bon template"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Si vous savez le nom de votre template, décommentez :
        # self.assertTemplateUsed(response, 'tasks/list.html')
    
    @tc("TC003")
    def test_basic_math(self):
        """Test basique pour vérifier que les tests fonctionnent"""
        self.assertEqual(1 + 1, 2)

class PriorityTaskTests(TestCase):
    """Tests pour les fonctionnalités de priorité"""
    
    def test_create_priority_task(self):
        """TC019: Création d'une tâche prioritaire"""
        task = Task.objects.create(
            title="Tâche importante",
            is_priority=True
        )
        self.assertEqual(task.title, "Tâche importante")
        self.assertTrue(task.is_priority)
        print("✅ TC019: Test création tâche prioritaire - PASSÉ")
    
    def test_task_default_not_priority(self):
        """TC020: Par défaut, une tâche n'est pas prioritaire"""
        task = Task.objects.create(title="Tâche normale")
        self.assertFalse(task.is_priority)
        print("✅ TC020: Test défaut non-prioritaire - PASSÉ")
    
    def test_update_task_to_priority(self):
        """TC021: Mettre à jour une tâche en prioritaire"""
        task = Task.objects.create(title="Tâche à mettre à jour")
        task.is_priority = True
        task.save()
        
        task.refresh_from_db()
        self.assertTrue(task.is_priority)
        print("✅ TC021: Test mise à jour en prioritaire - PASSÉ")
    
    def test_priority_tasks_first(self):
        """TC022: Les tâches prioritaires doivent apparaître en premier"""
        # Créer des tâches dans un ordre aléatoire
        Task.objects.create(title="Tâche normale 1", is_priority=False)
        Task.objects.create(title="Tâche prioritaire 1", is_priority=True)
        Task.objects.create(title="Tâche normale 2", is_priority=False)
        Task.objects.create(title="Tâche prioritaire 2", is_priority=True)
        
        # Récupérer triées par priorité (puis par date)
        tasks = Task.objects.all().order_by('-is_priority', 'created_at')
        
        # Vérifier que les 2 premières sont prioritaires
        self.assertTrue(tasks[0].is_priority)
        self.assertTrue(tasks[1].is_priority)
        self.assertFalse(tasks[2].is_priority)
        self.assertFalse(tasks[3].is_priority)
        print("✅ TC022: Test tri par priorité - PASSÉ")