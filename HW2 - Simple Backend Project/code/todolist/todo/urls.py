from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    #path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'), #새로운 할일을 추가
    path('tasks/create/', views.TaskCreateView, name='task-create'), #새로운 할일을 추가 (grpc 연동)
    path('tasks/list/', views.TaskListView.as_view(), name='task-list'), #할일 목록을 모두 조회
    path('tasks/completed/', views.CompletedListView.as_view(), name='completed-list'), #Completed가 True인 할일 목록 조회
    path('tasks/incompleted/', views.IncompletedListView.as_view(), name='incompleted-list'), #Completed가 False인 할일 목록 조회
    path('tasks/high-prior/', views.HighPriorListView.as_view(), name='important-list'), #prior_rank가 1인 할일 목록 조회
    path('tasks/<int:id>/', views.TaskView.as_view(), name='check-task'), #특정 할일 조회
    path('tasks/<int:id>/complete/', views.TaskCompleteView.as_view(), name='complete-task'), #특정 할일 상태를 완료로 변경
    path('tasks/<int:id>/modify/', views.TaskUpdateView.as_view(), name='update-task'), #특정 할일 수정
    path('tasks/<int:id>/delete/', views.TaskDeleteView.as_view(), name='delete-task'), #특정 할일 삭제
    path('tasks/delete-completed/', views.DeleteCompletedView.as_view(), name='delete-completed-tasks'), #Completed가 True인 할일 삭제
    path('tasks/delete-all/', views.DeleteAllView.as_view(), name='delete-all-tasks'), #모든 할일 삭제
]
