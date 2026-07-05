from django.urls import path
from .views import (
    ResponseCreateView, MyResponsesView, TaskResponsesView, ResponseAcceptRejectView
)

urlpatterns = [
    path('create/<int:task_id>/', ResponseCreateView.as_view(), name='create'),
    path('my/', MyResponsesView.as_view(), name='my'),
    path('task/<int:task_id>/', TaskResponsesView.as_view(), name='task_responses'),
    path('<int:pk>/', ResponseAcceptRejectView.as_view(), name='accept_reject'),
]