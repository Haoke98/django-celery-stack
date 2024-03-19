# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/6
@Software: PyCharm
@disc:
======================================="""
import json
import logging

from django_celery_results.backends import DatabaseBackend
from ..models import CustomTaskResult, TaskState


class CustomDatabaseBackend(DatabaseBackend):
    TaskModel = CustomTaskResult

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def store_result(self, task_id, result, state,
                     traceback=None, request=None, **kwargs):
        from django_celery_stack.models import CustomTaskResult
        # 存储任务结果的逻辑
        logging.debug("Saving the result....\ntask_id=\n%s\nkwargs=\n%s",
                      task_id,
                      json.dumps(kwargs, ensure_ascii=False, indent=4)
                      )
        # 创建或更新你自定义的模型实例，存储任务结果
        # custom_result, created = CustomTaskResult.objects.update_or_create(task_id=task_id, defaults={'result': result})
        # 这里可以存储额外的信息到你的自定义模型中
        # 例如：custom_result.progress = 50
        super(CustomDatabaseBackend, self).store_result(task_id, result, state, traceback, request, **kwargs)

    def get_result(self, task_id):
        # from django_celery_stack.models import CustomTaskResult
        # # 获取任务结果的逻辑
        # # 从你自定义的模型中获取任务结果
        # try:
        #     custom_result = CustomTaskResult.objects.get(task_id=task_id)
        #     return custom_result.result
        # except CustomTaskResult.DoesNotExist:
        #     return None
        print("Getting the result.... task_id={}".format(task_id))
        super(CustomDatabaseBackend, self).get_result(task_id)

    def get_extended_result(self, task_id):
        from django_celery_stack.models import CustomTaskResult
        # 获取扩展的任务结果，包含额外的信息
        # 从你自定义的模型中获取任务结果以及额外的信息
        try:
            custom_result = CustomTaskResult.objects.get(task_id=task_id)
            return {'result': custom_result.result, 'progress': custom_result.progress}
        except CustomTaskResult.DoesNotExist:
            return None

    def _store_result(
            self,
            task_id,
            result,
            status,
            traceback=None,
            request=None,
            using=None,
            total=None,
            processed=None,
            extra_process_info=None
    ):
        """Store return value and status of an executed task."""
        content_type, content_encoding, result = self.encode_content(result)
        logging.debug("_____________________sotring:%s_______status:%s_______________", task_id, status)
        meta = {
            **self._get_meta_from_request(request),
            "children": self.current_task_children(request),
        }
        _, _, encoded_meta = self.encode_content(
            meta,
        )

        task_props = {
            'content_encoding': content_encoding,
            'content_type': content_type,
            'meta': encoded_meta,
            'result': result,
            'status': status,
            'task_id': task_id,
            'traceback': traceback,
            'using': using,
            'total': total,
            'processed': processed,
            'extra_process_info': extra_process_info
        }

        task_props.update(
            self._get_extended_properties(request, traceback)
        )

        self.TaskModel._default_manager.store_result(**task_props)
        ts = TaskState(task_id=task_id, processed=processed, extra_process_info=extra_process_info,
                       traceback=traceback)
        ts.save()
        return result
