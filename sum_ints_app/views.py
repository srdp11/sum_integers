from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Data, Result
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

        print(Result.objects.all())
    return redirect('/')


def run_calculation(request):
    ids = [x for x in Data.objects.values_list('id', flat=True)]

    # chains = []
    #
    # for id in ids:
    #     chains.append(chain(load_data.s(id),
    #                         handle_data.s(id),
    #                         save_result.s(id))())
    #
    # for x in chains:
    #     print(x.ready())

    res = group([chain(load_data.s(id), handle_data.s(id), save_result.s(id)) for id in ids])()

    return redirect('/')
