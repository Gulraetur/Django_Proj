from django.urls import path
from .views import TaskListCreateView, TaskDetailView, DeliverTaskView, AcceptTaskView, RevisionTaskView, TaskMaterialsView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:task_id>/deliver/', DeliverTaskView.as_view(), name='deliver'),
    path('<int:task_id>/accept/', AcceptTaskView.as_view(), name='accept'),
    path('<int:task_id>/revision/', RevisionTaskView.as_view(), name='revision'),
    path('<int:task_id>/materials/', TaskMaterialsView.as_view(), name='materials'),
]