import grpc
import task_pb2
import task_pb2_grpc

def create_task(content, due_date, prior_rank):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = task_pb2_grpc.TaskServiceStub(channel)
        task = task_pb2.Task(content=content, due_date=due_date, prior_rank=prior_rank)
        response = stub.CreateTask(task)
        return response
    
# 나머지 9개 미완성 (todo에 REST-API만 구현)