# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/2/19
@Software: PyCharm
@disc:
======================================="""
from django_celery_results.models import TaskResult
from django.contrib import admin
from .customTaskTesult import CustomTaskResultAdmin
from .taskResult import TaskResultAdmin
from .taskchain import TasksChainAdmin
from .registeredTask import RegisteredTaskAdmin
from .taskStates import TaskStateAdmin

# 取消注册默认的 TaskResultAdmin
admin.site.unregister(TaskResult)
