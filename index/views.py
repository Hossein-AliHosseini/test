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
        market = form.cleaned_data['market']
    else:
        end = now().date()
        start = end - timedelta(days=14)
        market = Market.objects.first()
        form = Type1Form(initial={
            'market': market,
            'start': start,
            'end': end
        })
    result = ma.delay(start.strftime("%Y-%m-%d"),
                      end.strftime("%Y-%m-%d"),
                      market.id)
    return render(request, 'ma.html', {'task_id': result, 'form': form})


def EMA_view(request):
    form = Type1Form(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        market = form.cleaned_data['market']
    else:
        end = now().date()
        start = end - timedelta(days=14)
        market = Market.objects.first()
        form = Type1Form(initial={
            'market': market,
            'start': start,
            'end': end
        })
    result = ema.delay(start.strftime("%Y-%m-%d"),
                       end.strftime("%Y-%m-%d"), market.id)
    return render(request, 'ema.html', {'task_id': result, 'form': form})


def SO_view(request):
    form = Type2Form(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start']
        market = form.cleaned_data['market']
    else:
        start = now().date()
        market = Market.objects.first()
        form = Type2Form(initial={
            'market': market,
            'start': start,
        })
    result = so.delay(start.strftime("%Y-%m-%d"), market.id)
    return render(request, 'so.html', {'task_id': result, 'form': form})


def ADI_view(request):
    form = Type1Form(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        market = form.cleaned_data['market']
    else:
        end = now().date()
        start = end - timedelta(days=14)
        market = Market.objects.first()
        form = Type1Form(initial={
            'market': market,
            'start': start,
            'end': end
        })
    result = adi.delay(start.strftime("%Y-%m-%d"),
                       end.strftime("%Y-%m-%d"), market.id)
    return render(request, 'adi.html', {'task_id': result, 'form': form})


def check_index_status(request):
    task_id = request.GET.get('task_id')
    status = AsyncResult(task_id)
    if status.ready():
        return JsonResponse(status.get(), safe=False)
    else:
        return False
