from rest_framework import serializers
from . import models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskModel
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    task_info = serializers.SerializerMethodField()

    class Meta:
        model = models.EmployeeModel
        fields = '__all__'

    def get_task_info(self, obj):
        employee_task = models.EmployeeTaskModel.objects.filter(employee=obj, is_finished=False).first()
        if employee_task:
            task_serializer = TaskSerializer(employee_task.task)
            task_info = {
                'task_id': employee_task.task.id,
                'task': task_serializer.data,
            }
            return task_info
        else:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patronymic'] = representation.get('patronymic', '')
        return representation

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminModel
        fields = '__all__'


class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlotModel
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemModel
        fields = '__all__'


class EmployeeTaskSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    task_title = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()
    admin_name = serializers.SerializerMethodField()

    class Meta:
        model = models.EmployeeTaskModel
        fields = '__all__'

    def get_admin_name(self,obj):
        return f"{obj.admin.name} {obj.admin.surname} "
    
    def get_employee_name(self, obj):
        return f"{obj.employee.surname} {obj.employee.name}"

    def get_task_title(self, obj):
        return f"{obj.task.title}"
    
    def get_total_time(self, obj):
        total_seconds = obj.total_time.total_seconds()
        return int(total_seconds)


class TrackingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrackingTaskModel
        fields = '__all__'
