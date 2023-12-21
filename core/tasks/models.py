from django.db import models

#Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"ID: {self.id}, Titulo: {self.title}"
    
class SubTask(models.Model):
    main_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_complete = models.BooleanField(default=False)