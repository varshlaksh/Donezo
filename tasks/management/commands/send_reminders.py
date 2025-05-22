from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task, Notification

class Command(BaseCommand):
    help = 'Sends reminder notifications for tasks nearing their deadline'

    def handle(self, *args, **options):
        # Get tasks due in the next 24 hours that are not completed
        deadline_threshold = timezone.now() + timedelta(days=1)
        tasks = Task.objects.filter(
            deadline__lte=deadline_threshold,
            deadline__gt=timezone.now(),
            status__in=['PENDING', 'IN_PROGRESS']
        )

        for task in tasks:
            # Create notification for task creator
            Notification.objects.create(
                user=task.created_by,
                task=task,
                message=f"Reminder: Task '{task.title}' is due in less than 24 hours!"
            )

            # Create notification for assigned user if different from creator
            if task.assigned_to and task.assigned_to != task.created_by:
                Notification.objects.create(
                    user=task.assigned_to,
                    task=task,
                    message=f"Reminder: Task '{task.title}' is due in less than 24 hours!"
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully sent reminders for {tasks.count()} tasks')) 