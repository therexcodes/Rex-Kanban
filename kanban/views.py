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
        """Ensure the board is created with the logged-in user as owner"""
        try:
            serializer.save(owner=self.request.user) # Set the owner to the logged-in user
        except Exception as e:
            return Response (
                {"error": "An error occurred while creating the board."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
class BoardDeleteView (generics.DestroyAPIView):
    """VIEW that delete a board"""
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """Custom delete method to handle errors properly"""
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Board deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Board.DoesNotExist:
            return Response({"error": "Board not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
class ColumnListCreateView(generics.ListCreateAPIView):
    """View to list and create column for a specific"""
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user) #only get the list of columns
    
    
    def perform_create(self, serializer):
        board_id = self.request.data.get("board") #get board ID from request
        
        try:
            board = Board.objects.get(id=board_id, owner=self.request.user)
            serializer.save(board=board)  # Assign the column to the correct board
        except Board.DoesNotExist:
            raise Response(
                {"error": "Board not found or you do not have permission to add columns to it."},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception:
            raise Response(
                {"error": "An error occurred while creating the column."},
                status=status.HTTP_400_BAD_REQUEST
            )
        

class ColumnDeleteView (generics.DestroyAPIView):
    """view to delete a column"""
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """Custom delete method to handle errors properly"""
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Column deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Column.DoesNotExist:
            return Response({"error": "Column not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(
                {"error": "An unexpected error occurred while deleting the column."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        
class  TaskListCreateView(generics.ListCreateAPIView):
    """View to list and create task for a specific column"""
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(column__board__owner=self.request.user) # returns tasks for the user board
    
    def perform_create(self, serializer):
        column_id = self.request.data.get("column") # get column_id from the request
        
        try:
            column = Column.objects.get(id=column_id, board__owner=self.request.user)
            serializer.save(column=column)  # Assign the task to the correct column
        except Column.DoesNotExist:
            return Response(
                {"error": "Column not found or you do not have permission to add tasks to it."},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception:
            return Response(
                {"error": "An error occurred while creating the task."},
                status=status.HTTP_400_BAD_REQUEST
            ) 
        
        
class TaskDeleteView(generics.DestroyAPIView):
    """Delete a task based on then"""
    queryset= Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return Task.objects.filter(column__board__owner=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """Custom delete method to handle errors properly"""
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(
                {"error": "An unexpected error occurred while deleting the task."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
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