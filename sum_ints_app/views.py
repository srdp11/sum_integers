from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UploadFileForm
from .models import Data, Result, Run
from celery import chain, group
from .tasks import load_data, handle_data, save_result
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import json


# Create your views here.


def render_main(request):
    return render(request, 'sum_ints_app/index.html')


def save_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            for file in request.FILES.getlist('file'):
                file.seek(0)
                json_array_str = file.read().decode('utf-8')
                Data.objects.create(input=json_array_str)
        else:
            print(form.errors)

        print(Data.objects.all())
        print(Result.objects.all())
        print(Run.objects.all())

    return redirect('/')


def run_calculation(request):
    ids = [x for x in Data.objects.values_list('id', flat=True)]

    run = Run.objects.create()

    res = group([chain(load_data.s(id), handle_data.s(id, run.id), save_result.s(id, run.id)) for id in ids])()

    return redirect('/')


def last_status(request):
    data_count = Data.objects.count()

    if data_count == 0 or Run.objects.count() == 0:
        return JsonResponse({'last_run': 'False'})

    last_run = Run.objects.latest('id')
    results = Result.objects.filter(run=last_run)

    if results.count() == 0:
        return JsonResponse({'last_run': 'False'})

    if data_count != results.count():
        if Run.objects.count() > 1:
            results = Result.objects.filter(run=Run.objects.get(id=(last_run.id - 1)))
        else:
            return JsonResponse({'last_run': 'False'})

    if results.filter(is_success=False).count() > 0:
        return JsonResponse({'last_run': 'False'})
    else:
        return JsonResponse({'last_run': 'True'})


def last_results(request):
    data_count = Data.objects.count()

    if data_count == 0 or Run.objects.count() == 0:
        return JsonResponse({'results': 'null'})

    last_run = Run.objects.latest('id')
    results = Result.objects.filter(run=last_run)

    if results.count() == 0:
        return JsonResponse({'results': 'null'})

    results = Result.objects.filter(run=last_run)

    json_results = []
    for x in results:
        json_results.append(dict(x))

    # if we have some non-complete tasks
    if data_count > results.count():
        complete_data_ids = [x[0] for x in list(results.values_list('input'))]
        all_data_id = [x[0] for x in list(Data.objects.all().values_list('id'))]
        non_complete_tasks_id = [x for x in all_data_id if x not in complete_data_ids]

        non_complete_tasks = Result.objects.filter(run=(last_run.id - 1)).filter(input__in=non_complete_tasks_id)

        if non_complete_tasks.exists():
            for x in non_complete_tasks:
                json_results.append(dict(x))

    return JsonResponse(json_results, safe=False)


def clear(request):
    Data.objects.all().delete()
    Result.objects.all().delete()
    Run.objects.all().delete()

    return redirect('/')
