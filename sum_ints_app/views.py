from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UploadFileForm
from .models import Data, Result, Run
from celery import chain, group
from .tasks import load_data, handle_data, save_result
import time


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

    return redirect('/')


def run_calculation(request):
    ids = [x for x in Data.objects.values_list('id', flat=True)]

    run = Run.objects.create()

    res = group([chain(load_data.s(id), handle_data.s(id, run.id), save_result.s(id, run.id)) for id in ids])()

    return redirect('/')


def last_status(request):
    last_run = Run.objects.latest('id')

    data_count = Data.objects.all().count()

    if data_count == 0:
        return JsonResponse({'last_run': 'False'})

    results = Result.objects.filter(run=last_run)

    if data_count != results.count():
        results = Result.objects.get(run=Run.objects.get(id=(last_run.id - 1)))

    if results.filter(is_success=False).count() > 0:
        return JsonResponse({'last_run': 'False'})
    else:
        return JsonResponse({'last_run': 'True'})


def last_results(request):
    return 3
