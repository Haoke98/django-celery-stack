import datetime

from django.db import models
from django_celery_results.models import TaskResult
from django.utils.translation import gettext_lazy as _
from simplepro.models import BaseModel
from .. import managers
from django.conf import settings


# Create your models here.
class CustomTaskResult(TaskResult):
    total = models.IntegerField(default=0, null=True, blank=True, verbose_name='总量')
    processed = models.IntegerField(default=0, null=True, blank=True, verbose_name="已处理")
    extra_process_info = models.TextField(null=True, blank=True)

    objects = managers.CustomTaskResultManager()

    @property
    def progress(self):
        if self.processed is not None and self.total is not None:
            if self.total != 0:
                p = self.processed / self.total * 100
                return p
        return 0

    @property
    def elapsed_time(self):
        if self.date_done is not None:
            return self.date_done - self.date_created
        else:
            return datetime.datetime.now() - self.date_created

    # elapsed_time.short_description = '已运行'

    @property
    def speed(self):
        if self.processed is not None:
            return self.processed / self.elapsed_time.total_seconds()
        else:
            return 0

    # speed.short_description = '速率'

    @property
    def left(self):
        if self.processed is not None:
            return self.total - self.processed

    # left.short_description = '剩下'

    @property
    def need_time_dlt(self):
        if self.left is not None:
            if self.left == 0 or self.speed == 0:
                return datetime.timedelta(seconds=0)
            return datetime.timedelta(seconds=self.left / self.speed)

    # need_time_dlt.short_description = '还需'

    @property
    def finished_time(self):
        if self.need_time_dlt is None:
            return datetime.datetime.now()
        return datetime.datetime.now() + self.need_time_dlt

    class Meta:
        verbose_name = _('Custom Task Result')
        verbose_name_plural = _('Custom Task Result')


class TaskState(BaseModel):
    task_id = models.CharField(
        max_length=getattr(
            settings,
            'DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH',
            255
        ),
        null=True, blank=True,
        verbose_name=_('Task ID'),
        help_text=_('Celery ID for the Task that was run'), db_index=True)
    total = models.IntegerField(default=0, null=True, blank=True, verbose_name='总量', db_index=True)
    processed = models.IntegerField(default=0, null=True, blank=True, verbose_name="已处理", db_index=True)
    extra_process_info = models.TextField(null=True, blank=True)
    traceback = models.TextField(
        blank=True, null=True,
        verbose_name=_('Traceback'),
        help_text=_('Text of the traceback if the task generated one'))

    @property
    def progress(self):
        if self.processed is not None and self.total is not None:
            if self.total != 0:
                p = self.processed / self.total * 100
                return p
        return 0

    @property
    def elapsed_time(self):
        ctr = CustomTaskResult.objects.get(task_id=self.task_id)
        return self.createdAt - ctr.date_created

    # elapsed_time.short_description = '已运行'

    @property
    def speed(self):
        if self.processed is not None:
            return self.processed / self.elapsed_time.total_seconds()
        else:
            return 0

    # speed.short_description = '速率'

    @property
    def left(self):
        if self.processed is not None:
            return self.total - self.processed

    # left.short_description = '剩下'

    @property
    def need_time_dlt(self):
        if self.left is not None:
            if self.left == 0 or self.speed == 0:
                return datetime.timedelta(seconds=0)
            return datetime.timedelta(seconds=self.left / self.speed)

    # need_time_dlt.short_description = '还需'

    @property
    def finished_time(self):
        if self.need_time_dlt is None:
            return datetime.datetime.now()
        return datetime.datetime.now() + self.need_time_dlt

    class Meta:
        verbose_name = _('Task State')
        verbose_name_plural = _('Task State')


class TasksChain(BaseModel):
    name = models.CharField(
        max_length=200, unique=True,
        verbose_name=_('Name'),
        help_text=_('Short Description For This Task'),
    )
    tasks = models.TextField(null=True, unique=True)

    class Meta:
        verbose_name = _('Tasks Chain')
        verbose_name_plural = _('Tasks Chain')


class RegisteredTask(BaseModel):
    name = models.CharField(max_length=200, unique=True, null=True)
    doc = models.TextField(null=True)
    params = models.TextField(null=True)
    registeredAt = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _('Registered Task')
        verbose_name_plural = _('Registered Task')
