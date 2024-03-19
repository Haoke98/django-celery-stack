# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/7
@Software: PyCharm
@disc:
======================================="""
import importlib
import inspect

from celery import current_app
from django.contrib import admin, messages
from django.template.defaultfilters import pluralize
from django.utils.translation import gettext_lazy as _
from kombu.utils.json import loads
from simplepro.admin import FieldOptions
from simplepro.decorators import button
from simpleui.admin import AjaxAdmin

from ..models import RegisteredTask


@admin.register(RegisteredTask)
class RegisteredTaskAdmin(AjaxAdmin):
    """Admin-interface for periodic tasks."""
    celery_app = current_app
    # date_hierarchy = 'start_time'
    list_display = ('name', 'doc', 'params', 'createdAt')
    list_filter = []
    actions = ('run_tasks', 'discover_registered_tasks', 'inspect_control')
    search_fields = ('name',)
    readonly_fields = ()

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @button("重新加载已注册任务", enable=True)
    def discover_registered_tasks(self, request, queryset):
        from django_celery_stack.models import RegisteredTask
        RegisteredTask.objects.all().delete()
        for hostname, name in enumerate(current_app.tasks):
            print("task:", name)
            if name.split('.')[0] == 'celery':
                continue
            full_func_name = name
            # 使用字符串分割来找到模块名和函数名
            module_path, func_name = full_func_name.rsplit('.', 1)
            # 动态导入模块
            module = importlib.import_module(module_path)
            method = getattr(module, func_name)
            params = ""
            sig = inspect.signature(method)
            for hostname, param in enumerate(sig.parameters.values()):
                print(hostname, param)
                params += "{}. {}\n".format(hostname, param)

            if not name.startswith('celery.'):
                RegisteredTask(
                    name=name,
                    doc=method.__doc__,
                    params=params,
                ).save()
        return

    @button("InspectControl", enable=True)
    def inspect_control(self, request, queryset):
        controlIns = current_app.control.inspect()
        # TODO: 尽快实现在Django的管理页面(admin)中进行呢查看和管理
        print("=" * 20, "Stats (statistics of worker)", "=" * 20)
        stats: dict = controlIns.stats()
        if stats:
            for hostname, statInfo in stats.items():
                print(hostname)
                for k, v in statInfo.items():
                    if isinstance(v, dict):
                        print(" " * 10, "|", "-" * 10, k, ":")
                        for kk, vv in v.items():
                            print(" " * 23, "|", "-" * 10, kk, "=", vv)
                    else:
                        print(" " * 10, "|", "-" * 10, k, "=", v)
        print("=" * 50, "\n" * 4)
        print("=" * 20, "Active Tasks (currently executed by workers)", "=" * 20)
        activeTasksMap: dict = controlIns.active()
        if activeTasksMap:
            for hostname, activeTasks in activeTasksMap.items():
                print(hostname)
                for activeTask in activeTasks:
                    print(" " * 10, "|", "-" * 10, activeTask)
        print("=" * 50, "\n" * 4)

        print("=" * 20, "active queues", "=" * 20)
        queues: dict = controlIns.active_queues()
        if queues:
            for hostname, queues in queues.items():
                print(hostname)
                for queue in queues:
                    print(" " * 10, "|", "-" * 10, queue)
        print("=" * 50, "\n" * 4)
        print("=" * 20, "registered tasks", "=" * 20)
        registeredTasksMap = controlIns.registered()
        if registeredTasksMap:
            for hostname, registeredTasks in registeredTasksMap.items():
                print(hostname)
                for task in registeredTasks:
                    print(" " * 10, "|", "-" * 10, task)
        print("=" * 50, "\n" * 4)
        return

    def get_layer_config(self, request, queryset):
        return {
            'title': '测试批量修改',
            'params': [{
                'type': 'radio',
                'key': 'type',
                'label': '修改类型',
                'require': True,
                'value': 1,
                'options': [{
                    'key': 1,
                    'label': '更新'
                }, {
                    'key': 0,
                    'label': '新增'
                }]
            }, {
                'type': 'checkbox',
                'key': 'ck',
                'label': 'Checkbox',
                'require': True,
                'value': [1],
                'options': [{
                    'key': 1,
                    'label': '更新'
                }, {
                    'key': 0,
                    'label': '新增'
                }]
            }]
        }

    def run_tasks(self, request, queryset):
        post = request.POST
        self.celery_app.loader.import_default_modules()

        task = queryset[0]
        args = loads(post.get('args'))
        # FIXME: 这里直接用 " 来替换 ' 符号的话容易出现多层嵌套时的混淆问题, 必须特殊处理!!!
        kwargs = loads(post.get('kwargs').replace("'", '"'))
        queue = post.get('queue', None)
        print("queue:", queue, type(args), type(kwargs), args, kwargs)
        if task.doc is None:
            human_readable_name = str(task)
        else:
            human_readable_name = task.doc[:min(len(task.doc), 20)]

        tasks = [
            (
                self.celery_app.tasks.get(task.name),
                args,
                kwargs,
                queue,
                human_readable_name
            )
        ]

        if any(t[0] is None for t in tasks):
            for i, t in enumerate(tasks):
                if t[0] is None:
                    break

            # variable "i" will be set because list "tasks" is not empty
            not_found_task_name = queryset[i].task

            self.message_user(
                request,
                _(f'task "{not_found_task_name}" not found'),
                level=messages.ERROR,
            )
            return

        task_ids = [
            task.apply_async(args=args, kwargs=kwargs, queue=queue,
                             periodic_task_name=periodic_task_name)
            if queue and len(queue)
            else task.apply_async(args=args, kwargs=kwargs,
                                  periodic_task_name=periodic_task_name)
            for task, args, kwargs, queue, periodic_task_name in tasks
        ]
        tasks_run = len(task_ids)
        self.message_user(
            request,
            _('{0} task{1} {2} successfully run').format(
                tasks_run,
                pluralize(tasks_run),
                pluralize(tasks_run, _('was,were')),
            ),
        )

    run_tasks.short_description = _('Run selected tasks')
    run_tasks.type = 'success'
    run_tasks.icon = 'el-icon-s-promotion'

    def generate_run_task_form(self, request, queryset, *args, **kwargs):
        print("qs:", len(queryset))
        for i, q in enumerate(queryset):
            print(i, q, q.name)
            full_func_name = q.name
            # 使用字符串分割来找到模块名和函数名
            module_path, func_name = full_func_name.rsplit('.', 1)
            # 动态导入模块
            module = importlib.import_module(module_path)
            method = getattr(module, func_name)
            sig = inspect.signature(method)
            doc = "\r{}Parameters:".format(method.__doc__)
            for i, param in enumerate(sig.parameters.values()):
                print(i, param)
                doc += "\n\t{}. {}".format(i, param)
            print("doc:\n", doc)
            controlIns = current_app.control.inspect()
            queues: dict = controlIns.active_queues()
            queueOptions = []
            if queues:
                for hostname, queues in queues.items():
                    print(hostname)
                    for queue in queues:
                        print(" " * 10, "|", "-" * 10, queue)
                        queue_name = queue['name']
                        queueOptions.append({
                            'key': queue_name,
                            'label': "{} ==> {}".format(queue_name, hostname)
                        })
            return {
                # 弹出层中的输入框配置

                # 这里指定对话框的标题
                'title': '任务运行控制台',
                # 提示信息
                'tips': '任务名称: {}'.format(q.name),
                # 确认按钮显示文本
                'confirm_button': '确认 | 开始运行',
                # 取消按钮显示文本
                'cancel_button': '取消',

                # 弹出层对话框的宽度，默认50%
                'width': '60%',

                # 表单中 label的宽度，对应element-ui的 label-width，默认80px
                'labelWidth': "100px",
                'params': [
                    {
                        # 这里的type 对应el-input的原生input属性，默认为input
                        'type': 'textarea',
                        # key 对应post参数中的key
                        'key': 'doc',
                        # 显示的文本
                        'label': '参数文档',
                        'value': doc,
                        # 附加参数
                        'extras': {
                            'editable': False,
                            'rows': 14,
                            'disabled': True
                        }
                    },
                    {
                        # 这里的type 对应el-input的原生input属性，默认为input
                        'type': 'textarea',
                        # key 对应post参数中的key
                        'key': 'args',
                        # 显示的文本
                        'label': '位置参数',
                        # 为空校验，默认为False
                        'require': True,
                        # 附加参数
                        'extras': {
                            'placeholder': '[param1,param2,param3]',
                            'prefix-icon': 'el-icon-delete',
                            'suffix-icon': 'el-icon-setting',
                            'clearable': True
                        }
                    }, {
                        'type': 'textarea',
                        'key': 'kwargs',
                        'label': '关键字参数',
                        'require': True,
                        # size对应elementui的size，取值为：medium / small / mini
                        'size': 'small',
                        # 附加参数
                        'extras': {
                            'placeholder': '{"param1":"value","param2":"value"}',
                        }
                    },
                    {
                        # FIXME:后期得改成多选,因为Celery本身就支持多队列
                        'type': 'select',
                        'key': 'queue',
                        'label': '任务队列',
                        'require': True,
                        # size对应elementui的size，取值为：medium / small / mini
                        'width': "400px",
                        'size': 'small',
                        # 附加参数
                        'extras': {
                        },
                        'options': queueOptions
                    }
                ]
            }

    run_tasks.layer = generate_run_task_form

    fields_options = {
        'name': {
            'fixed': 'left',
            'min_width': '300px',
            'align': 'left',
            "show_overflow_tooltip": True
        },
        'doc': {
            'min_width': '500px',
            'align': 'left',
            "show_overflow_tooltip": True
        },
        'params': {
            'min_width': '300px',
            'align': 'left',
            "show_overflow_tooltip": True
        },
        'createdAt': FieldOptions.DATE_TIME,
    }

    def formatter(self, obj, field_name, value):
        if field_name in ["doc", "params"]:
            if value is not None:
                return value.replace("\n", "<br>")
        return value
