# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/2/19
@Software: PyCharm
@disc:
======================================="""
import time

from celery import current_task
from celery import shared_task


@shared_task
def chain_test_first_task(*args, **kwargs):
    print("args:", args, "kwargs:", kwargs)
    total = 5
    for i in range(1, total + 1):
        time.sleep(1)
        progress = (i / total) * 100
        current_task.update_state(state='PROGRESS',
                                  meta={'progress': round(progress, 2), 'total': total})

    return {'progress': "100%", 'total': total}


@shared_task
def chain_test_second_task(*args, **kwargs):
    print("args:", args, "kwargs:", kwargs)
    total = 5
    for i in range(1, total + 1):
        time.sleep(1)
        progress = (i / total) * 100
        current_task.update_state(state='PROGRESS',
                                  meta={'progress': round(progress, 2), 'total': total})

    return {'progress': "100%", 'total': total}


@shared_task
def chain_test_third_task(*args, **kwargs):
    print("args:", args, "kwargs:", kwargs)
    total = 5
    for i in range(1, total + 1):
        time.sleep(1)
        progress = (i / total) * 100
        current_task.update_state(state='PROGRESS',
                                  meta={'progress': round(progress, 2), 'total': total})

    return {'progress': "100%", 'total': total}
