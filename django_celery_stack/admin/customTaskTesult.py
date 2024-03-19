# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/2/19
@Software: PyCharm
@disc:
======================================="""

from django.contrib import admin
from simplepro.admin import FieldOptions
from simplepro.dialog import ModalDialog

from ..models import CustomTaskResult


# Register your models here.

@admin.register(CustomTaskResult)
class CustomTaskResultAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'task_id', 'periodic_task_name', 'task_name', 'status', 'date_created', 'date_done',
        'worker',
        'elapsed_time', 'progress', 'processed', 'total', 'speed',
        'left', 'need_time_dlt', 'finished_time',
        'task_args', 'task_kwargs', 'extra_process_info', 'result_data', 'show_traceback', 'content_type',
        'content_encoding',)

    list_filter = ['periodic_task_name', 'task_name', 'status', 'worker', 'content_type', 'content_encoding',
                   'date_created', 'date_done', ]
    search_fields = ['task_id', 'periodic_task_name', 'task_name', 'result', 'meta', 'traceback']

    def task_name(self, obj):
        return obj.task_name

    task_name.short_description = '名称'

    def result_data(self, obj):
        return obj.result or "No result available"

    result_data.short_description = '结果'

    def show_traceback(self, obj):
        modal = ModalDialog()
        # 这个是单元格显示的文本
        modal.cell = '<el-link type="primary">点击查看</el-link>'
        modal.title = "详情对话框"
        modal.width = "1200px"
        modal.height = "600px"
        # 这里的url可以写死，也可以用django的反向获取url，可以根据model的数据，传到url中
        modal.url = "/celery/task/results/detail?id=%s" % obj.id
        # 是否显示取消按钮
        modal.show_cancel = True

        return modal

    # 这个是列头显示的文本
    show_traceback.short_description = "详情"

    def formatter(self, obj, field_name, value):
        if field_name == "speed":
            return "{:.4f}".format(value)
        if field_name == "progress":
            if value:
                return "{:.4f}%".format(value)
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'task_id': {
            'fixed': 'left',
            'min_width': '100px',
            'align': 'center',
            "show_overflow_tooltip": True
        },
        'date_created': FieldOptions.DATE_TIME,
        'date_done': {
            'min_width': '190px',
            'align': 'left'
        },
        'elapsed_time': FieldOptions.DURATION,
        'periodic_task_name': {
            'min_width': '200x',
            'align': 'left',
            'show_overflow_tooltip': True,
        },
        'task_name': {
            'min_width': '240px',
            'align': 'left',
            'show_overflow_tooltip': True,
        },
        'status': {
            'min_width': '120px',
            'align': 'center',
        },

        'content_type': {
            'min_width': '200px',
            'align': 'left'
        },
        'content_encoding': {
            'min_width': '200px',
            'align': 'left'
        },
        'worker': {
            'min_width': '120px',
            'align': 'left',
            'show_overflow_tooltip': True
        },
        'progress': {
            'min_width': '120px',
            'align': 'right',
        },
        'total': {
            'min_width': '120px',
            'align': 'right',
        },
        'processed': {
            'min_width': '120px',
            'align': 'right',
        },
        'speed': {
            'min_width': '120px',
            'align': 'right',
        },
        'left': {
            'min_width': '120px',
            'align': 'right',
        },
        'need_time_dlt': FieldOptions.DURATION,
        'finished_time': {
            'min_width': '180px',
            'align': 'left'
        },
        'task_kwargs': {
            'min_width': '220px',
            'align': 'left'
        },
        'task_args': {
            'min_width': '220px',
            'align': 'left'
        },
        'result_data': {
            'min_width': '540px',
            'align': 'left'
        },
        'extra_process_info': {
            'min_width': '540px',
            'align': 'left'
        },
        'show_traceback': {
            'min_width': '100px',
            'align': 'center',
            'fixed': 'right'
        },
        'meta': {
            'min_width': '400px',
            'align': 'left'
        }
    }
