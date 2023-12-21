from django.urls import path
from .views import TaskListAPIView, TaskDetailAPIView, TaskSubtaskAPIView, SubtaskDetailAPIView

urlpatterns = [
    path('', TaskListAPIView.as_view(), name="tasks-lists"),
    path('<int:pk>', TaskDetailAPIView.as_view(), name="tasks-detail"),
    path('<int:pk>/subtask', TaskSubtaskAPIView.as_view(), name="task-subtask"),
    path('<int:mpk>/subtask/<int:spk>', SubtaskDetailAPIView.as_view(), name="subtask-detail"),
]