# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/8
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin
from simplepro.admin import FieldOptions

from ..models import TaskState


@admin.register(TaskState)
class TaskStateAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_id', 'processed', 'createdAt', 'extra_process_info', 'traceback', ]
    list_filter = ['task_id']
    date_hierarchy = 'createdAt'
    search_fields = ['extra_process_info', 'task_id', 'traceback']
    ordering = ('-createdAt',)

    fields_options = {
        'id': {
            'min_width': '100px',
            'align': 'right',
            'fixed': 'left',
            "show_overflow_tooltip": True
        },
        'task_id': {
            'min_width': '200px',
            'align': 'left',
            'fixed': 'left',
            "show_overflow_tooltip": True

        },
        'processed': {
            'min_width': '100px',
            'align': 'right',
        },
        'extra_process_info': {
            'min_width': '600px',
            'align': 'left',
        },
        'traceback': {
            'min_width': '500px',
            'align': 'left',
        },
        'createdAt': FieldOptions.DATE_TIME,
    }
