import grpc
from concurrent import futures

import os, sys, django

sys.path.append('C:/Users/32192530/Desktop/todolist') #Django 프로젝트 경로 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import task_pb2
import task_pb2_grpc
from todo.models import Task

#gRPC 서비스 구현
class TaskService(task_pb2_grpc.TaskServiceServicer):
    def CreateTask(self, request, context):
        task = Task(content=request.content, due_date=str(request.due_date), prior_rank=request.prior_rank)
        task.save()
        return task_pb2.Task(id=task.id, content=task.content, due_date=str(task.due_date), prior_rank=task.prior_rank)

#나머지 9개 미완성 (todo에 REST-API만 구현)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    