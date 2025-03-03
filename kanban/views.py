from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Board, Column, Task
from django.shortcuts import get_object_or_404
from .serializers import BoardSerializer, ColumnSerializer, TaskSerializer


class BoardListCreateView(generics.ListCreateAPIView):
    """View to ls all boards and create a new board"""
    
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user) # Only return the user's boards
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user) # Set the owner to the logged-in user
    
    
class BoardDeleteView (generics.DestroyAPIView):
    """VIEW that delete a board"""
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)
    
    
class ColumnListCreateView(generics.ListCreateAPIView):
    """View to list and create column for a specific"""
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user) #only get the list of columns
    
    
    def perform_create(self, serializer):
        board_id = self.request.data.get("board") #get board ID from request
        serializer.save(board_id=board_id) # Assign the column to the correct board
        

class ColumnDeleteView (generics.DestroyAPIView):
    """view to delete a column"""
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user)

        
class  TaskListCreateView(generics.ListCreateAPIView):
    """View to list and create task for a specific column"""
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(column__board__owner=self.request.user) # returns tasks for the user board
    
    def perform_create(self, serializer):
        column_id = self.request.data.get("column") # get column_id from the request
        serializer.save(column_id=column_id) # Asssign task to the correct column 
        
        
class TaskDeleteView(generics.DestroyAPIView):
    """Delete a task based on then"""
    queryset= Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return Task.objects.filter(column__board__owner=self.request.user)
    
class TaskUpdateView(generics.UpdateAPIView):
    """Allows a user to update a task, including moving it to another column"""
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_object(self):
        """Ensure the user owns the board before updating the task"""
        task = get_object_or_404(Task, id=self.kwargs["pk"])
        if task.column.board.owner != self.request.user:
            self.permission_denied(self.request, message="You do not own this board")
        return task
    
    def update(self, request, *args, **kwargs):
        """Custom update method to validate column movement"""
        task = self.get_object()
        newColumnID = request.data.get('column')
        
        if newColumnID:
            new_column = get_object_or_404(Column, id=newColumnID)
            
            # Ensure the new column belongs to the same board
            if new_column.board != task.column.board:
                return Response(
                    {"error": "Column does not belomg to the same board"}, status=status.HTTP_400_BAD_REQUEST
                )
        
            task.column = new_column
        
        return super().update(request, *args, **kwargs)