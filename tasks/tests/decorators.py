# Contenu CORRECT :
def tc(test_case_id):
    """Décorateur pour ajouter un ID de test case"""
    def decorator(test_func):
        test_func.test_case_id = test_case_id
        return test_func
    return decorator