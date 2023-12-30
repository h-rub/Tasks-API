#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer

# Create your views here.
class TaskListAPIView(APIView): 
    """
    Access with http://localhost:8000/api/tasks

    GET: request will return a list of all tasks in the db 
    POST: request will create an entry in the db and return the entry just created
    """
    def get(self, request):
        """ GET request will return a list of all tasks in the db """
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     request_data = request.data
    #     if request_data:
    #         title = request.data['title']
    #         description = request.data['description']
    #         task_created = Task.objects.create(title=title, description=description)
    #         response = {'status': 'Success', 'message': 'Task created successfully'}
    #         return Response(response)
    #     else:
    #         return Response({'status': 'ERROR','message': 'Did not provide title and description'}, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailAPIView(APIView): # Access with "http://localhost:8000/api/tasks/{task_id}"

    def get_task(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk): # GET request will return the specific task in the db
        task = self.get_task(pk)
        if task:
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        return Response({'message': 'Task {pk} not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk): # PUT request will update the specific task
        task = self.get_task(pk)

        if not task:
            return Response({'message': f'Task {pk} not found'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def put(self, request, pk):
    #     task = self.get_task(pk)
    #     if task:
    #         serializer = TaskSerializer(task, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({'message': f'Task {pk} not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk): # DELETE request will delete the specific task
        task = self.get_task(pk)

        if not task:
            return Response({'message': f'Task {pk} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        task.delete()
        return Response({'message': f'Task {pk} deleted'}, status=status.HTTP_204_NO_CONTENT)
    
class TaskSubtaskAPIView(APIView): #Access with "http://localhost:8000/api/tasks/{task_id}/subtask"
    
    def get_subtask(self, pk):
        try:
            return SubTask.objects.filter(main_task_id=pk)
        except SubTask.DoesNotExist:
            return None
        
    def get(self, request, pk): # GET request will return all subtasks related to the main task
        try:
            task = Task.objects.get(pk=pk) # Try to find the task
            subtasks = self.get_subtask(pk)

            task_serializer = TaskSerializer(task)
            subtask_serializer = SubTaskSerializer(subtasks, many=True)

            response_data = {
                'Main task': task_serializer.data,
                'subtasks': subtask_serializer.data,
            }

            return Response(response_data)
        except Task.DoesNotExist:
            return Response({'message': f'Task with id {pk} not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, pk): # POST request will create a subtask for the main task
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': f'Task with id {pk} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        request.data['main_task'] = pk

        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubtaskDetailAPIView(APIView): #Access with "http://localhost:8000/api/tasks/{task_id}/subtask/{subtask_id}"
    
    def get_subtask(self, spk):
        try:
            return SubTask.objects.get(pk=spk)
        except SubTask.DoesNotExist:
            return Response({'message': f'Subtask with id {spk} not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, mpk, spk): # GET request will return only the specific subtask
        try:
            task = Task.objects.get(pk=mpk) # Try to find the task
            subtasks = self.get_subtask(spk)

            subtask_serializer = SubTaskSerializer(subtasks)


            return Response(subtask_serializer.data)
        except Task.DoesNotExist:
            return Response({'message': f'Task with id {mpk} not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, mpk, spk): # PUT request will update the subtask, allows partial updates
        try:
            task = Task.objects.get(pk=mpk) # Try to find the task
            subtasks = self.get_subtask(spk)


            serializer_context = {'request': request} # Allow partial updates for PUT requests
            subtask_serializer = SubTaskSerializer(subtasks, data=request.data, context=serializer_context, partial=True) # Allow partial updates 
            if subtask_serializer.is_valid():
                subtask_serializer.save()
                return Response(subtask_serializer.data)
            return Response(subtask_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({'message': f'Task with id {mpk} not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, mpk, spk): # Delete the specific subtask
        try:
            task = Task.objects.get(pk=mpk) # Try to find the task
            subtasks = self.get_subtask(spk)
            
            subtasks.delete()
            
            return Response({'message': f'Subtask with id {spk} deleted'}, status=status.HTTP_204_NO_CONTENT)
        
        except Task.DoesNotExist:
            return Response({'message': f'Task with id {mpk} not found'}, status=status.HTTP_404_NOT_FOUND)
