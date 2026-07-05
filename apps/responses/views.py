from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Response
from .serializers import ResponseSerializer
from apps.tasks.models import Task
from apps.tasks.services import assign_executor

class ResponseCreateView(generics.CreateAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        if not hasattr(self.request.user, 'executor_profile'):
            raise PermissionDenied("Только исполнитель может откликаться")
        if task.client == self.request.user:
            raise PermissionDenied("Нельзя откликаться на свою задачу")
        if Response.objects.filter(task=task, executor=self.request.user).exists():
            raise PermissionDenied("Вы уже откликнулись на эту задачу")
        serializer.save(task=task, executor=self.request.user, status='pending')
        print("DEBUG: task_id =", task_id)
        print("DEBUG: user =", self.request.user)
        print("DEBUG: data =", serializer.initial_data)

class MyResponsesView(generics.ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Response.objects.filter(executor=self.request.user)

class TaskResponsesView(generics.ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        if task.client != self.request.user:
            raise PermissionDenied("Вы не можете просматривать отклики на эту задачу")
        return Response.objects.filter(task=task)

class ResponseAcceptRejectView(generics.UpdateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        response = self.get_object()
        task = response.task
        if task.client != self.request.user:
            raise PermissionDenied("Вы не можете управлять этим откликом")
        if task.status != 'search':
            raise PermissionDenied("Нельзя принимать отклики в текущем статусе")
        action = self.request.data.get('action')
        if action == 'accept':
            assign_executor(task, response.executor, self.request.user)
        elif action == 'reject':
            response.status = 'rejected'
            response.save()
        else:
            raise PermissionDenied("Неверное действие")