from rest_framework import generics, permissions, views, response, status, permissions 
from rest_framework.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer, TaskMaterialSerializer
from .services import change_task_status, assign_executor
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class AcceptTaskView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if task.client != request.user:
            return response.Response({"detail": "Вы не являетесь заказчиком"}, status=status.HTTP_403_FORBIDDEN)
        if task.status != 'review':
            return response.Response({"detail": "Нельзя принять задачу в текущем статусе"}, status=status.HTTP_400_BAD_REQUEST)
        change_task_status(task, 'closed', request.user, "Заказчик подтвердил выполнение")
        return response.Response({"status": "closed", "detail": "Задача закрыта"}, status=status.HTTP_200_OK)

class RevisionTaskView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if task.client != request.user:
            return response.Response({"detail": "Вы не являетесь заказчиком"}, status=status.HTTP_403_FORBIDDEN)
        if task.status != 'review':
            return response.Response({"detail": "Нельзя отправить на доработку в текущем статусе"}, status=status.HTTP_400_BAD_REQUEST)
        change_task_status(task, 'work', request.user, "Отправлено на доработку")
        return response.Response({"status": "work", "detail": "Задача отправлена на доработку"}, status=status.HTTP_200_OK)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get('role')
        qs = Task.objects.all()
        if role == 'executor':
            return qs.filter(status='search')
        elif role == 'customer':
            return qs.filter(client=user)
        elif role == 'executor_my':
            return qs.filter(executor=user)
        else:  
            return qs.all()

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'client_profile'):
            raise PermissionDenied("Только заказчик может создавать задачи")
        serializer.save(client =self.request.user, status='draft')

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        task = self.get_object()
        print(f"User: {self.request.user}, Task client: {task.client}")
        if task.client  != self.request.user:
            raise PermissionDenied("Вы не можете редактировать эту задачу")
        if task.status not in ('draft', 'search'):
            raise PermissionDenied("Нельзя редактировать задачу в текущем статусе")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.client  != self.request.user:
            raise PermissionDenied("Вы не можете удалить эту задачу")
        if instance.status not in ('draft', 'search'):
            raise PermissionDenied("Нельзя удалить задачу в текущем статусе")
        instance.delete()
class TaskMaterialsView(generics.ListAPIView):
    serializer_class = TaskMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        return task.results.all()
        
class DeliverTaskView(generics.CreateAPIView):
    serializer_class = TaskMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)

        if task.executor != self.request.user:
            raise PermissionDenied("Вы не являетесь исполнителем")
        if task.status != 'work':
            raise PermissionDenied("Задача не в статусе 'В работе'")

        serializer.save(task=task)
        change_task_status(task, 'review', self.request.user, "Исполнитель сдал результат")