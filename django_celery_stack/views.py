import json
import subprocess

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import CustomTaskResult
from graphviz import Source


# Create your views here.
def task_result_view(request):
    if request.method == 'GET':
        _id = request.GET.get('id')
        task = CustomTaskResult.objects.get(id=_id)
        meta: dict = json.loads(task.meta)
        children = meta["children"]
        if children is not None and len(children) != 0:
            child_task_ids = []
            for group_task in children:
                print(group_task[0])
                if group_task.__len__() > 1 and group_task[1] is not None:
                    for i, child_task in enumerate(group_task[1]):
                        task_id = child_task[0][0]
                        child_task_ids.append(task_id)
            total = 0
            processed = 0
            childTaskObjs = CustomTaskResult.objects.filter(task_id__in=child_task_ids).all()
            for i, childTaskObj in enumerate(childTaskObjs):
                print(" " * 10, i, childTaskObj.progress, childTaskObj.speed)
                total += childTaskObj.total
                processed += childTaskObj.processed
            task.total = total
            task.processed = processed
        return HttpResponse(
            '''
            <h2>Positional Arguments:</h2>
            <div><ul>{}</ul></div>
            <h2>Named Arguments:</h2>
            <div><ul>{}</ul></div>
            <h2>Result:</h2>
            <div><ul>{}</ul></div>
            <h2>Meta:</h2>
            <div><ul>{}</ul></div>
            <h2>Progress:</h2>
            <table>
                <tbody>
                    <tr>
                        <td>Progress</td>
                        <td>:<td>
                        <td>{:.4f}% ({}/{})</td>
                        <td><td>
                        <td><td>
                        <td>Left</td>
                        <td>:<td>
                        <td>{}</td>
                    </tr>
                    <tr>
                        <td>time</td>
                        <td>:<td>
                        <td>{}</td>
                        <td><td>
                        <td><td>
                        <td>speed</td>
                        <td>:<td>
                        <td>{}/s</td>
                    </tr>
                    <tr>
                        <td>Need</td>
                        <td>:<td>
                        <td>{}</td>
                        <td><td>
                        <td><td>
                        <td>FinishedAt</td>
                        <td>:<td>
                        <td>{}</td>
                    </tr>
                </tbody>
            </table>
            <h2>ExtraProcessInfo:</h2>
            <div><ul>{}</ul></div>
            <h2>TraceBack:</h2>
            <div><ul>{}</ul></div>'''.format(
                task.task_args, task.task_kwargs,
                task.result,
                task.meta,
                task.progress, task.processed, task.total, task.left,
                task.elapsed_time, task.speed,
                task.need_time_dlt, task.finished_time,
                task.extra_process_info,
                task.traceback,
            )
        )


@require_http_methods(["GET"])
def worker_graph(request):
    command = ['celery', '-A', 'proj', 'graph', 'workers']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    graph_dot_str = result.stdout
    src = Source(graph_dot_str)
    png_bytes = src.pipe(format='png')
    response = HttpResponse(png_bytes, content_type='image/png')
    return response
