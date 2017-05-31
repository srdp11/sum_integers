from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Data

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

    return redirect('/')


def run(request):
    return request
