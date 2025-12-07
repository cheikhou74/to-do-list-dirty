from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_priority = models.BooleanField(default=False, verbose_name="Prioritaire")  # AJOUTEZ CETTE LIGNE
    
    def __str__(self):
        return self.title