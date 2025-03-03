from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self):
        return self.name
    
class Column(models.Model):
    title = models.CharField(max_length=100) #column title status (To-do, progress)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    position = models.PositiveIntegerField(default=0) #Order of the column
    
    def __str__(self):
        return f"{self.title} - {self.board.name}"
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title