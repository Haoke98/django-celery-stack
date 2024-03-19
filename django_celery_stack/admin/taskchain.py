# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/2/19
@Software: PyCharm
@disc:
======================================="""
from celery import current_app, chain
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from kombu.utils.json import loads
from simplepro.admin import FieldOptions
from simplepro.components.widgets import MultiSelectInput, trim_name
from django.template.loader import render_to_string
from ..models import TasksChain

DIRECTIONAL_TASK_SPLITTER = "-->"


def load_tasks():
    # 在这里动态加载其他应用程序中注册的任务
    # 例如，假设你想要获取所有应用程序中的 shared_tasks，可以这样实现：
    # 在这里动态加载其他应用程序中注册的任务
    loader = current_app.loader
    # FIXME: 这里的自动发现机制有问题, 尤其是此项目作为依赖包导入到其他项目时会出错
    # loader.autodiscover_tasks(packages=['django_celery_stack', 'marketSubject'])


class TaskSelectMultipleWidget(MultiSelectInput):
    """Widget that lets you choose between task names."""

    def __init__(self, *args, **kwargs):
        super(TaskSelectMultipleWidget, self).__init__(*args, **kwargs)
        self.options = self.tasks_as_choices()

    def tasks_as_choices(self):
        load_tasks()
        _options = []
        for name in current_app.tasks:
            if not name.startswith('celery.'):
                _options.append({
                    'id': name,
                    'text': name
                })

        return _options


class TaskMultipleChoiceFormField(forms.MultipleChoiceField):
    """Field that lets you choose between task names."""

    def __init__(self, field_name: str, *args, **kwargs):
        """
        :param field_name: 字段名称, 对应最终表单数据中的key值.
        """
        super(TaskMultipleChoiceFormField, self).__init__(*args, **kwargs)
        self.widget = TaskSelectMultipleWidget(name=field_name, attrs={"style": "width:80%;"})

    def valid_value(self, value):
        return True


class TaskChainForm(forms.ModelForm):
    """Form that lets you create and modify periodic tasks."""

    tasks = TaskMultipleChoiceFormField(
        field_name='tasks',
        label=_('Task (registered)'),
        required=True,
        help_text=_('The Name of the Celery Task that Should be Run.  '
                    '(Example: "proj.tasks.import_contacts")'),
    )

    class Meta:
        """Form metadata."""

        model = TasksChain
        fields = ('name', 'tasks', 'info')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(TaskChainForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        print("instance:", instance)
        if instance and instance.tasks is not None:
            print("tasks:", instance.tasks)
            tasks_list = instance.tasks.split(DIRECTIONAL_TASK_SPLITTER)
            self.initial['tasks'] = tasks_list

    def clean(self):
        data = super().clean()
        print("data:", data)
        regtask = data.get('tasks')
        print("regtask:", regtask)
        if regtask:
            result = DIRECTIONAL_TASK_SPLITTER.join(regtask)
            print("result:", result)
            data['tasks'] = result
        if not data['tasks']:
            exc = forms.ValidationError(_('At least two registered tasks need to be selected'))
            self._errors['tasks'] = self.error_class(exc.messages)
            raise exc

        if data.get('expire_seconds') is not None and data.get('expires'):
            raise forms.ValidationError(
                _('Only one can be set, in expires and expire_seconds')
            )
        return data

    def _clean_json(self, field):
        value = self.cleaned_data[field]
        print("value:", value)
        try:
            loads(value)
        except ValueError as exc:
            raise forms.ValidationError(
                _('Unable to parse JSON: %s') % exc,
            )
        print("value after loads:", value)
        return value

    def clean_args(self):
        return self._clean_json('args')

    def clean_kwargs(self):
        return self._clean_json('kwargs')


@admin.register(TasksChain)
class TasksChainAdmin(admin.ModelAdmin):
    form = TaskChainForm
    list_display = ('id', 'name', 'tasks', 'updatedAt', 'createdAt', 'info', 'deletedAt')
    search_fields = ['name', 'tasks']
    actions = ['run']

    def formatter(self, obj, field_name, value):
        if field_name == "tasks":
            tasks = value.split(DIRECTIONAL_TASK_SPLITTER)
            res = "<br/>⬇︎<br>".join(tasks)
            return res
        return value

    def run(self, request, queryset, **kwargs):
        for i, qs in enumerate(queryset):
            print(f"{i + 1}.", qs.name, ":")
            task_names = qs.tasks.split(DIRECTIONAL_TASK_SPLITTER)
            task_signatures = []
            for task_name in task_names:
                print(" " * 20, task_name, end='')
                task_func = current_app.tasks.get(task_name)
                print(" " * 20, type(task_func), task_func)
                task_signatures.append(task_func.s())
            # 定义任务链
            task_chain = chain(*task_signatures)
            # 将任务链应用到Celery中
            result = task_chain.apply_async()
            print("任务链Applied:", result)
        return {
            'state': True,
            'msg': f'任务链已启动'
        }

    run.short_description = _('Start up')

    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'name': {
            'min_width': '200px',
            'align': 'left'
        },
        'tasks': {
            'min_width': '380px',
            'align': 'center',
        },
        'info': {
            'min_width': '200px',
            'align': 'left',
            'show_overflow_tooltip': True
        }
    }
