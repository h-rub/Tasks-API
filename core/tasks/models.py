from django.db import models

#Create your models here.
class Task(models.Model): # Main tasks table
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"ID: {self.id}, Titulo: {self.title}"
    
class SubTask(models.Model): # Subtasks table
    main_task = models.ForeignKey(Task, on_delete=models.CASCADE) # Relate to main task table with foreign key
    title = models.CharField(max_length=200)
    is_complete = models.BooleanField(default=False)