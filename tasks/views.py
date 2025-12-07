from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def task_list(request):
    """Affiche toutes les tâches"""
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/list.html', {'tasks': tasks})

def create_task(request):
    """Crée une nouvelle tâche"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create.html', {'form': form})

def update_task(request, pk):
    """Modifie une tâche existante"""
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/update_task.html', {'form': form, 'task': task})

def delete_task(request, pk):
    """Supprime une tâche"""
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/delete.html', {'task': task})
# Ajoute ces vues si besoin
def task_detail(request, pk):
    """Détails d'une tâche"""
    task = get_object_or_404(Task, id=pk)
    return render(request, 'tasks/detail.html', {'task': task})

def toggle_complete(request, pk):
    """Basculer l'état de complétion"""
    task = get_object_or_404(Task, id=pk)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def filter_by_priority(request, priority):
    """Filtrer par priorité"""
    tasks = Task.objects.filter(priority=priority)
    return render(request, 'tasks/list.html', {
        'tasks': tasks,
        'filter': priority
    })