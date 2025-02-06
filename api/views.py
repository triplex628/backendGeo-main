import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from . import models
from . import serializers

from utils.report_generator import ReportGenerator
from .models import AdminModel, EmployeeTaskModel, ItemModel, EmployeeModel, TaskModel


class EmployeeView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = models.EmployeeModel.objects.all()
    serializer_class = serializers.EmployeeSerializer

    def get_queryset(self):
        plot_id = self.request.query_params.get('plot_id')

        if plot_id:
            return models.EmployeeModel.objects.filter(plot__id=plot_id) 

        return models.EmployeeModel.objects.all()

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            employee = get_object_or_404(models.EmployeeModel, id=kwargs['pk'])
            serializer = self.get_serializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class AdminView(ListAPIView):
    queryset = models.AdminModel.objects.all()
    serializer_class = serializers.AdminSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TaskView(RetrieveUpdateDestroyAPIView, ListCreateAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        plot_id = self.request.query_params.get('plot_id')

        if plot_id:
            return models.TaskModel.objects.filter(plot__id=plot_id, is_available=True) 

        return models.TaskModel.objects.filter(is_available=True)



    def post(self, request, *args, **kwargs):

        created_by_login = request.data.get('created_by')
        request_data = request.data.copy()
        created_by_user = get_object_or_404(AdminModel, username=created_by_login)
        request_data['admin'] = created_by_user.id
        del request_data['created_by']





        serializer = self.get_serializer(data=request_data)
        print(serializer)
        if not serializer.is_valid():
            print(serializer.errors)  # Выводим ошибки сериализатора
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            task = get_object_or_404(models.TaskModel, id=kwargs['pk'])
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)




    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        employee_tasks = models.EmployeeTaskModel.objects.filter(task=instance, is_finished=False)
        if employee_tasks:
            employees = [f"{employee_task.employee}" for employee_task in employee_tasks]
            return Response({
                "message": "Task couldn't delete",
                "employees": employees,
            }, status=status.HTTP_409_CONFLICT)

        instance.is_available = False
        instance.save()

        return Response({"message": "Task marked as not available"}, status=status.HTTP_200_OK)


class PlotView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = models.PlotModel.objects.all()
    serializer_class = serializers.PlotSerializer

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            plot = get_object_or_404(models.PlotModel, id=kwargs['pk'])
            serializer = self.get_serializer(plot)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        admin_id = request.data.get('admin_id')

        # Обновление данных запроса, чтобы включить admin, если он присутствует
        update_data = request.data.copy()
        if admin_id:
            admin = get_object_or_404(models.AdminModel, id=admin_id)
            update_data['admin_id'] = admin.id

        serializer = self.get_serializer(instance, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Plot deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ItemView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ItemSerializer
    queryset = models.ItemModel.objects.all()

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            item = get_object_or_404(models.ItemModel, id=kwargs['pk'])
            serializer = self.get_serializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Plot deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        

class TaskHandlerView(APIView):
    def get(self, request, *args, **kwargs):
        employee_task_id = request.query_params.get('employee_task_id')
        employee_task = get_object_or_404(models.EmployeeTaskModel, id=employee_task_id)
        
        tracking_task = models.TrackingTaskModel.get_latest_tracking_task(employee_task)

        start_time = tracking_task.start_time if tracking_task.start_time else timezone.now()
        end_time = tracking_task.end_time if tracking_task.end_time else timezone.now() 

        time = employee_task.total_time + end_time - start_time

        data = {
            "time": time.total_seconds(),
            "start_time": start_time,
            "end_time": end_time,
            "is_paused": employee_task.is_paused,
            "is_finished": employee_task.is_finished,
        }

        return Response(data=data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        task_id = request.query_params.get('task_id')
        employee_id = request.query_params.get('employee_id')

        type_of_action = request.data.get('action')

        employee = get_object_or_404(models.EmployeeModel, id=employee_id)
        task = get_object_or_404(models.TaskModel, id=task_id) 

        employee_task = models.EmployeeTaskModel.objects.filter(employee=employee, is_finished=False).first()
        if employee_task is None:
            return Response(data="Task did't selected", status=status.HTTP_404_NOT_FOUND)

        print(employee_task)

        match type_of_action:
            case 'start':
                pause_message = "В работе"
                employee_task.is_started = True

                if employee_task.is_paused:
                    employee_task.is_paused = False


                
                

                tracking_task = models.TrackingTaskModel.objects.filter(employee_task=employee_task)

                start_time = timezone.now() 
                if not tracking_task:
                    employee_task.start_time = start_time
                    
                tracking_task = models.TrackingTaskModel(
                    start_time = start_time,
                    employee_task = employee_task
                )
                employee_task.paused_message = f"{pause_message}"

                employee_task.save()
                tracking_task.save()


                data = {
                    "message": f"{employee_task.employee} has started task",
                    "task": employee_task.task.title,
                }

                return Response(data=data, status=status.HTTP_200_OK)
                
            case 'end':
                task.employee_task = None
                task.save()
                
                tracking_task = models.TrackingTaskModel.get_latest_tracking_task(employee_task)

                # if employee_task.is_paused:
                #     return Response({"message": "You have not finished task"}, status=status.HTTP_409_CONFLICT)

                end_time = timezone.now()
                tracking_task.end_time = end_time
                tracking_task.save()

                employee_task.is_finished = True
                employee_task.is_started = False

                employee_task.end_time = end_time
                employee_task.total_time += tracking_task.end_time - tracking_task.start_time
                employee.status =False

                employee.save()
                employee_task.save()

                return Response({"message": f"{employee_task} has been finished"}, status=status.HTTP_200_OK)
            case "pause":
                pause_message = request.data.get('message')
                print(pause_message)
                tracking_task = models.TrackingTaskModel.get_latest_tracking_task(employee_task)
                tracking_task.end_time = timezone.now()
                tracking_task.save()
                
                employee_task.is_paused = True
                employee_task.paused_message = f"{pause_message}"
                employee_task.total_time += tracking_task.end_time - tracking_task.start_time
                employee_task.save()

                return Response({"message": f"{employee_task} ---- {pause_message} has been paused"}, status=status.HTTP_200_OK)
            case _:
                return Response({"message": "Invalid type of action with timer"}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeTaskView(ListAPIView):
    serializer_class = serializers.EmployeeTaskSerializer
    queryset = models.ItemModel.objects.all()

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            item = get_object_or_404(models.EmployeeTaskModel, id=kwargs['pk'])
            serializer = self.get_serializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        plot_id = self.request.query_params.get('plot_id')

        if plot_id:
            employee_tasks = models.EmployeeTaskModel.objects.filter(task__plot_id=plot_id, is_finished=False)
            print(employee_tasks)
            serializer = self.get_serializer(employee_tasks, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        task_id = self.request.query_params.get('task_id')
        employee_id = self.request.query_params.get('employee_id')

        employee = get_object_or_404(models.EmployeeModel, id=employee_id)
        task = get_object_or_404(models.TaskModel, id=task_id)
        
        employee_task = models.EmployeeTaskModel.objects.filter(
            employee=employee,
            task=task,
            is_finished=False
        ).first()

        tracking_task = models.TrackingTaskModel.get_latest_tracking_task(employee_task)

        if tracking_task is None:
            return Response({"detail": "not found"}, status=status.HTTP_409_CONFLICT)

        if tracking_task.end_time is None:
            end_time = timezone.now() 
            time = employee_task.total_time + end_time - tracking_task.start_time
            employee_task.total_time = time
        
        serializer = self.get_serializer(employee_task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        task_id = self.request.query_params.get('task_id')
        employee_id = self.request.query_params.get('employee_id')

        employee = get_object_or_404(models.EmployeeModel, id=employee_id)
        task = get_object_or_404(models.TaskModel, id=task_id)
        
        employee_task = models.EmployeeTaskModel.objects.filter(
            employee=employee,
            task=task,
            is_finished=False
        ).first()

        serializer = self.get_serializer(employee_task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(employee_task, serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def choose_task(request, *args, **kwargs):
    employee_id = request.query_params.get('employee_id')
    task_id = request.query_params.get('task_id')
    admin_id = request.query_params.get('admin_id')
    item_id = request.query_params.get('item_id')
    comment = request.data.get('comment')

    # Отладочный вывод для проверки
    print("Received data:", request.data)
    print("Admin ID:", admin_id)

    # Проверка на наличие employee_id и admin_id
    if not employee_id or not admin_id:
        return Response({"error": "employee_id and admin_id are required."}, status=status.HTTP_400_BAD_REQUEST)

    employee = get_object_or_404(models.EmployeeModel, id=employee_id)
    task = get_object_or_404(models.TaskModel, id=task_id)
    item = get_object_or_404(models.ItemModel, id=item_id)

    employee_task = models.EmployeeTaskModel.objects.filter(employee=employee, is_finished=False).first()

    if employee_task is not None:
        serializer = serializers.EmployeeTaskSerializer(employee_task)
        serialized_data = serializer.data
        return Response(data={"message": f"Task is already assigned to {serialized_data}"}, status=status.HTTP_409_CONFLICT)

    employee_task = models.EmployeeTaskModel(
        employee=employee,
        task=task,
        item=item,
        employee_comment=comment,
        admin_id=admin_id  # Устанавливаем admin_id при создании employee_task
    )

    employee_task.save()
    serializer = serializers.EmployeeTaskSerializer(employee_task)
    serialized_data = serializer.data

    return Response({"message": serialized_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def sign_in(request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def generate_report(request, *args, **kwargs):
    # for production
    start_time = timezone.datetime.strptime(request.query_params.get('start_time'), '%Y-%m-%d')
    end_time = timezone.datetime.strptime(request.query_params.get('end_time'), '%Y-%m-%d')
    end_time = end_time.replace(hour=23, minute=59, second=59)
    # Get the admin ID from request parameters (assuming it's passed as a query parameter)
 
    # for testing
    # start_time = timezone.datetime.strptime(request.query_params.get('start_time'), "%Y-%m-%dT%H:%M:%S.%fZ")
    # end_time = timezone.datetime.strptime(request.query_params.get('end_time'), "%Y-%m-%dT%H:%M:%S.%fZ")

    employee_tasks = models.EmployeeTaskModel.objects.filter(start_time__gte=start_time, end_time__lte=end_time)



    report_generator = ReportGenerator()
#    report_generator.upload_items()
    response = report_generator.generate_report(employee_tasks)

    return response
    # return Response({"message": "hello"}, status=status.HTTP_200_OK)



@api_view(['POST'])
def create_employee_task(request):
    # Получаем параметры из запроса
    task_id = request.data.get('task_id')
    employee_id = request.data.get('employee_id')
    item_id = request.data.get('item_id')
    admin_id = request.data.get('admin_id')
    print(admin_id)

    # Проверяем наличие всех параметров
    if not (task_id and employee_id and item_id and admin_id):
        print("error")
        return Response({"error": "All parameters (task_id, employee_id, item_id, admin_id) are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем соответствующие объекты или возвращаем 404
    task = get_object_or_404(TaskModel, id=task_id)
    employee = get_object_or_404(EmployeeModel, id=employee_id)
    item = get_object_or_404(ItemModel, id=item_id)
    admin = get_object_or_404(AdminModel, id=admin_id)

    if employee.status:
        return Response({"error": "Работник занят задачей"}, status=status.HTTP_400_BAD_REQUEST)


    # Создаем объект EmployeeTaskModel
    employee_task = EmployeeTaskModel.objects.create(
        task=task,
        employee=employee,
        item=item,
        admin=admin,
        is_paused=False,
        paused_message="Не начал",
        is_started=False,
        is_finished=False,
        total_time=datetime.timedelta(milliseconds=0), # Обнуляем время
        start_time=None,
        end_time=None
    )

    data = {
        "id": employee_task.id,
        "task": employee_task.task.id,
        "employee": employee_task.employee.id,
        "item": employee_task.item.id,
        "admin": employee_task.admin.id,
        "is_paused": employee_task.is_paused,
        "is_started": employee_task.is_started,
        "is_finished": employee_task.is_finished,
        "total_time": employee_task.total_time
    }
    print(data)

    employee.status = True
    employee.save()

    # Возвращаем успешный ответ с созданным объектом
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def plan_break(request):
    tasks = EmployeeTaskModel.objects.filter(is_started=True, is_paused=False, is_finished=False)
    updated_count = 0
    for task in tasks:

        task.is_paused = True
        task.paused_message = "Автоматическая пауза"

        try:
            tracking_task = models.TrackingTaskModel.objects.filter(employee_task=task).latest('start_time')

            tracking_task.end_time = timezone.now()

            # Применяй обновление total_time также, как в функции pause
            task.total_time += tracking_task.end_time - tracking_task.start_time
            task.save()
            tracking_task.save()  # Не забудь сохранить tracking_task
        except models.TrackingTaskModel.DoesNotExist:
            continue

        updated_count += 1

    return Response({
        'status': 'Успешно',
        'message': f'{updated_count} задач были поставлены на паузу.'
    })


class EmployeeAuthView(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        pin_code = request.data.get('pin_code')

        if not id or not pin_code:
            return Response({'error': 'Требуется указать имя и PIN-код.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = EmployeeModel.objects.get(id=id, pin_code=pin_code)
            # Успешная аутентификация
            return Response({'redirect_url': 'https://example.com/tasks&employee_id=' + str(employee.id)}, status=status.HTTP_200_OK)
        except EmployeeModel.DoesNotExist:
            # Ошибка аутентификации
            return Response({'error': 'Неверное имя, фамилия или PIN-код.'}, status=status.HTTP_401_UNAUTHORIZED)