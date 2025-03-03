from django.urls import path
from .views import BoardListCreateView, BoardDeleteView, ColumnListCreateView, ColumnDeleteView, TaskListCreateView, TaskDeleteView, TaskUpdateView



urlpatterns = [
    
    path('boards/', BoardListCreateView.as_view(), name='board-create-list'),
    path('boards/<int:pk>/', BoardDeleteView.as_view(), name='board-delete'),
    
    
    path('columns/', ColumnListCreateView.as_view(), name='column-create-list'),
    path('columns/<int:pk>/', ColumnDeleteView.as_view(), name='column-delete'),
    
    
    path('tasks/', TaskListCreateView.as_view(), name='task-create-list'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update")
]


