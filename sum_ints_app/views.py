from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Data
from celery import chain
from sum_integers.celery import app
from .tasks import load_data, test_func, save_result

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
                Data.objects.create(input=json_array_str,
                                    output={})
        else:
            print(form.errors)

        print(Data.objects.all())
    return redirect('/')


def run_calculation(request):
    ids = [x for x in Data.objects.values_list('id', flat=True)]

    for id in ids:
        chain(load_data.s(id), test_func.s(), save_result.s(id))()

    return redirect('/')
