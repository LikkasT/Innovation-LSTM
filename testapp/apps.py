from django.apps import AppConfig
from background_task.models import Task
from .tasks import my_background_task


class TestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testapp'
    def ready(self):
        # 检查是否已经有已调度的任务
        if not Task.objects.filter(task_name='my_background_task').exists():
            # 如果没有,则安排任务在应用程序启动时执行
            my_background_task.schedule(delay=0)



