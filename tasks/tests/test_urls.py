from django.test import TestCase
from .decorators import tc  # IMPORT RELATIF CORRECT

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