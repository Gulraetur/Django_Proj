from .models import Task, TaskHistory

def change_task_status(task, new_status, changed_by, comment=''):
    old_status = task.status
    task.status = new_status
    task.save()
    TaskHistory.objects.create(
        task=task,
        from_status=old_status,
        to_status=new_status,
        changed_by=changed_by,
        comment=comment
    )

def assign_executor(task, executor, changed_by):
    task.executor = executor
    task.status = 'work'
    task.save()
    TaskHistory.objects.create(
        task=task,
        from_status='search',
        to_status='work',
        changed_by=changed_by,
        comment=f'Выбран исполнитель {executor.get_full_name()}'
    )
    task.responses.exclude(executor=executor).update(status='rejected')
    task.responses.filter(executor=executor).update(status='accepted')