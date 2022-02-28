from celery.result import AsyncResult

from django.shortcuts import render
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponse

from .forms import *
from .tasks import *

from datetime import timedelta


def MA_view(request):
    form = Type1Form(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
    else:
        end = now().date()
        start = end - timedelta(days=14)
        form = Type1Form(initial={
            'start': start,
            'end': end
        })
    result = ma.delay(start, end)
    return render(request, 'ma.html', {'result': result, 'form': form})


def EMA_view(request):
    form = Type1Form(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
    else:
        end = now().date()
        start = end - timedelta(days=14)
        form = Type1Form(initial={
            'start': start,
            'end': end
        })
    result = ema.delay(start, end)
    return render(request, 'ema.html', {'result': result, 'form': form})


def SO_view(request):
    form = Type2Form(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start']
    else:
        start = now().date()
        form = Type2Form(initial={
            'start': start,
        })
    result = so.delay(start)
    return render(request, 'so.html', {'result': result, 'form': form})


def ADI_view(request):
    form = Type1Form(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
    else:
        end = now().date()
        start = end - timedelta(days=14)
        form = Type1Form(initial={
            'start': start,
            'end': end
        })
    result = ema.delay(start, end)
    return render(request, 'adi.html', {'result': result, 'form': form})


def check_index_status(request):
    task_id = request.GET.get('task_id')
    status = AsyncResult(task_id)
    if status.ready():
        return JsonResponse(status.get(), safe=False)
    else:
        return False
