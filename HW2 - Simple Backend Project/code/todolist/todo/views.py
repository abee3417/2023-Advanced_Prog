from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
import json, sys

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

sys.path.insert(1, 'C:/Users/32192530/Desktop/todolist/grpc_files') #상위 폴더의 grpc 파일들을 가져오기 위함
from grpc_files import grpc_client

# Create your views here.
def test(request):
    return render(request, 'todo/test.html')

'''
class TaskCreateView(generics.CreateAPIView): #새로운 할일을 추가
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
'''

@csrf_exempt
def TaskCreateView(request): #새로운 할일을 추가 (grpc 연동)
    if request.method == "POST":
        # 여기서 grpc_client의 메서드를 호출
        data = json.loads(request.body)
        grpc_client.create_task(data['content'], data['due_date'], data['prior_rank'])
        return JsonResponse({"message": "Add new data successfully"})

class TaskListView(generics.ListAPIView): #할일 목록을 모두 조회
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class CompletedListView(generics.ListAPIView): #Completed가 True인 할일 목록 조회
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(completed=True)

class IncompletedListView(generics.ListAPIView): #Completed가 False인 할일 목록 조회
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(completed=False)

class HighPriorListView(generics.ListAPIView): #prior_rank가 1인 할일 목록 조회
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(prior_rank=1)

class TaskView(generics.RetrieveAPIView): #특정 할일 조회
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

class TaskCompleteView(generics.UpdateAPIView): #특정 할일 상태를 완료로 변경
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.completed = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class TaskUpdateView(generics.UpdateAPIView): #특정 할일 수정
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

class TaskDeleteView(generics.DestroyAPIView): #특정 할일 삭제
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

class DeleteCompletedView(generics.DestroyAPIView): #Completed가 True인 할일 삭제
    def delete(self, request, *args, **kwargs):
        Task.objects.filter(completed=True).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteAllView(generics.DestroyAPIView): #모든 할일 삭제
    def delete(self, request, *args, **kwargs):
        Task.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)