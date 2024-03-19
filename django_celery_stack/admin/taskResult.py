# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/8
@Software: PyCharm
@disc:
======================================="""
import datetime

from django.contrib import admin
from simplepro.admin import FieldOptions
from simplepro.dialog import ModalDialog


class TaskResultAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'task_id', 'periodic_task_name', 'task_name', 'status', 'date_created', 'date_done', 'elapsed_time',
        'worker',
        'content_type',
        'content_encoding', 'task_args', 'task_kwargs', 'result_data', 'show_traceback')

    list_filter = ['periodic_task_name', 'task_name', 'status', 'worker', 'content_type', 'content_encoding',
                   'date_created', 'date_done', ]

    def task_name(self, obj):
        return obj.task_name

    task_name.short_description = '名称'

    def result_data(self, obj):
        return obj.result or "No result available"

    result_data.short_description = '结果'

    def elapsed_time(self, obj):
        if obj.date_done is not None:
            return obj.date_done - obj.date_created
        else:
            return datetime.datetime.now() - obj.date_created

    elapsed_time.short_description = '已运行'

    def show_traceback(self, obj):
        modal = ModalDialog()
        # 这个是单元格显示的文本
        modal.cell = '<el-link type="primary">点击查看</el-link>'
        modal.title = "详情对话框"
        modal.width = "1000px"
        modal.height = "500px"
        # 这里的url可以写死，也可以用django的反向获取url，可以根据model的数据，传到url中
        modal.url = "/api/task/results/detail?id=%s" % obj.id
        # 是否显示取消按钮
        modal.show_cancel = True

        return modal

    # 这个是列头显示的文本
    show_traceback.short_description = "详情"

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
        'elapsed_time': {
            'min_width': '180px',
            'align': 'left'
        },
        'periodic_task_name': {
            'min_width': '200x',
            'align': 'left',
            'show_overflow_tooltip': True,
            'fixed': 'left'
        },
        'task_name': {
            'min_width': '180px',
            'align': 'left',
            'show_overflow_tooltip': True,
            'fixed': 'left'
        },
        'status': {
            'min_width': '120px',
            'align': 'center',
            'fixed': 'left'
        },

        'content_type': {
            'min_width': '130px',
            'align': 'left'
        },
        'worker': {
            'min_width': '120px',
            'align': 'left',
            'show_overflow_tooltip': True
        },
        'task_kwargs': {
            'min_width': '200px',
            'align': 'left'
        },
        'task_args': {
            'min_width': '200px',
            'align': 'left'
        },
        'result_data': {
            'min_width': '540px',
            'align': 'left'
        },
        'show_traceback': {
            'min_width': '100px',
            'align': 'center',
            # 'fixed': 'right'
        },
        'meta': {
            'min_width': '400px',
            'align': 'left'
        }
    }
