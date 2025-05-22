from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Task, Notification
from .forms import TaskForm, UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'tasks/register.html', {'form': form})

@login_required
def dashboard(request):
    tasks = Task.objects.filter(
        Q(created_by=request.user) | Q(assigned_to=request.user)
    ).order_by('-created_at')
    
    # Get task statistics
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='COMPLETED').count()
    pending_tasks = tasks.filter(status='PENDING').count()
    in_progress_tasks = tasks.filter(status='IN_PROGRESS').count()
    
    # Get upcoming deadlines
    upcoming_deadlines = tasks.filter(
        deadline__gte=timezone.now(),
        deadline__lte=timezone.now() + timedelta(days=7)
    ).exclude(status='COMPLETED')
    
    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'upcoming_deadlines': upcoming_deadlines,
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            
            # Create notification for assigned user
            if task.assigned_to:
                Notification.objects.create(
                    user=task.assigned_to,
                    task=task,
                    message=f"You have been assigned to task: {task.title}"
                )
            
            messages.success(request, 'Task created successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user != task.created_by:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            old_assigned_to = task.assigned_to
            task = form.save()
            
            # Create notification if assignee changed
            if task.assigned_to and task.assigned_to != old_assigned_to:
                Notification.objects.create(
                    user=task.assigned_to,
                    task=task,
                    message=f"You have been assigned to task: {task.title}"
                )
            
            messages.success(request, 'Task updated successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit'})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user != task.created_by:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('dashboard')
    return render(request, 'tasks/delete_task.html', {'task': task})

@login_required
def search_tasks(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    
    tasks = Task.objects.filter(
        Q(created_by=request.user) | Q(assigned_to=request.user)
    )
    
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    if status:
        tasks = tasks.filter(status=status)
    
    if priority:
        tasks = tasks.filter(priority=priority)
    
    return render(request, 'tasks/search_results.html', {
        'tasks': tasks,
        'query': query,
        'status': status,
        'priority': priority
    })

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    unread_count = notifications.filter(is_read=False).count()
    
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification = get_object_or_404(Notification, id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
    
    return render(request, 'tasks/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })
