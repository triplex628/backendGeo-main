from django.urls import path
from . import views
from .views import EmployeeAuthView, end_task, start_rework, end_rework, start_useful_time, stop_useful_time, stop_non_working_time, get_rework_timer
from utils.report_generator import ReportGenerator
from .models import TaskModel
urlpatterns = [
    path('employees/', views.EmployeeView.as_view(), name='employee-list-create'),
    path('admins/', views.AdminView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', views.EmployeeView.as_view(), name='employee-retrieve-update-delete'),
    path('tasks/', views.TaskView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskView.as_view(), name='task-retrieve-update-delete'),
    path('plots/', views.PlotView.as_view(), name='plot-list-create'),
    path('plots/<int:pk>/', views.PlotView.as_view(), name='plot-retrieve-update-delete'),
    path('items/', views.ItemView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', views.ItemView.as_view(), name='item-retrieve-update-delete'),
    path('employee-tasks/', views.EmployeeTaskView.as_view(), name='employee-task'),
    path('employee-tasks/<int:pk>/', views.EmployeeTaskView.as_view(), name='employee-task-id'),
    path('timer/', views.TaskHandlerView.as_view(), name="time-handler"),
    path('choose-task/', views.choose_task, name="choose_task"),
    path('login/', views.sign_in, name="login"),
    path('generate-report/', views.generate_report, name="generate-report"),
    path('generate-single-report/', views.generate_single_report, name="generate-single-report"),
    path('employee-task/create/', views.create_employee_task, name='create-employee-task'),
    path('plan-break/', views.plan_break, name='plan-break'),
    path('auth/', EmployeeAuthView.as_view(), name='employee-auth'),
    path('check-shift/', views.check_shift, name='check-shift'),
    path('stop-non-working-time/', stop_non_working_time, name='stop_non_working_time'),
    #path('close-task/<int:task_id>/', TaskModel.close_task, name='close-task'),
    #path('employee-task/<int:task_id>/<str:action>/', EmployeeTaskActionAPIView.as_view(), name='employee-task-action'),
    path('end-task/', views.end_task, name='end_task'),
    path('start-rework/', start_rework, name='start_rework'),
    path('end-rework/', end_rework, name='end_rework'),
    path('start-useful-time/', start_useful_time, name='start_useful_time'),
    path('stop-useful-time/', stop_useful_time, name='stop_useful_time'),
    path('get-rework-timer/', views.get_rework_timer, name='get_rework_timer'),
]
