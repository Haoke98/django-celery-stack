# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/6
@Software: PyCharm
@disc:
======================================="""
import logging

from django_celery_results.managers import TaskResultManager, transaction_retry


class CustomTaskResultManager(TaskResultManager):
    @transaction_retry(max_retries=2)
    def store_result(self, content_type, content_encoding,
                     task_id, result, status,
                     traceback=None, meta=None,
                     periodic_task_name=None,
                     task_name=None, task_args=None, task_kwargs=None,
                     worker=None, using=None, total=None, processed=None, extra_process_info=None):
        """Store the result and status of a task.

        Arguments:
            content_type (str): Mime-type of result and meta content.
            content_encoding (str): Type of encoding (e.g. binary/utf-8).
            task_id (str): Id of task.
            periodic_task_name (str): Celery Periodic task name.
            task_name (str): Celery task name.
            task_args (str): Task arguments.
            task_kwargs (str): Task kwargs.
            result (str): The serialized return value of the task,
                or an exception instance raised by the task.
            status (str): Task status.  See :mod:`celery.states` for a list of
                possible status values.
            worker (str): Worker that executes the task.
            using (str): Django database connection to use.
            traceback (str): The traceback string taken at the point of
                exception (only passed if the task failed).
            meta (str): Serialized result meta data (this contains e.g.
                children).
            total (int): The total number of content in the task.
            processed (int): The total number of processed content in the task.

        Keyword Arguments:
            exception_retry_count (int): How many times to retry by
                transaction rollback on exception.  This could
                happen in a race condition if another worker is trying to
                create the same task.  The default is to retry twice.

        """

        fields = {
            'status': status,
            'result': result,
            'traceback': traceback,
            'meta': meta,
            'content_encoding': content_encoding,
            'content_type': content_type,
            'periodic_task_name': periodic_task_name,
            'task_name': task_name,
            'task_args': task_args,
            'task_kwargs': task_kwargs,
            'worker': worker,
            'extra_process_info': extra_process_info,
        }
        if total:
            fields["total"] = total
        if processed:
            fields['processed'] = processed
        logging.debug("Task:%s, status: %s, result: %s", task_id, status, result)
        obj, created = self.using(using).get_or_create(task_id=task_id,
                                                       defaults=fields)
        if not created:
            for k, v in fields.items():
                if v is not None:
                    setattr(obj, k, v)
            obj.save(using=using)
        return obj
