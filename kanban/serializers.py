from rest_framework import serializers
from .models import Board, Column, Task


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    
    class Meta:
        model = Board
        fields = ["id","name","owner","created_at"]
        
        
class ColumnSerializer(serializers.ModelSerializer):
    board = serializers.ReadOnlyField(source="board.id")
    
    class Meta:
        model = Column
        fields = ["id","title","board","position"]
        
class TaskSerializer(serializers.ModelSerializer):
    column = serializers.ReadOnlyField(source="column.id")  

    class Meta:
        model = Task
        fields = ["id", "title", "description", "column", "created_at", "updated_at"]
