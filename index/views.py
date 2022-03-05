from celery.result import AsyncResult

from django.shortcuts import render
from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from index.forms import Type1Form, Type2Form
from index.tasks import ma, ema, so, adi
from nobitex.models import Market, Trade

from datetime import timedelta


@login_required(login_url='signup')
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
    result = ma.delay(request.user.email,
                      start.strftime("%Y-%m-%d"),
                      end.strftime("%Y-%m-%d"),
                      market.id)
    return render(request, 'ma.html', {'task_id': result, 'form': form})


@login_required(login_url='signup')
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
    first = Trade.objects.order_by('time').first().time.date()
    duration = (end - start).days
    result = ema.delay(start.strftime("%Y-%m-%d"),
                       end.strftime("%Y-%m-%d"),
                       market.id, duration,
                       first.strftime("%Y-%m-%d"))
    return render(request, 'ema.html', {'task_id': result, 'form': form})


@login_required(login_url='signup')
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


@login_required(login_url='signup')
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
    first = Trade.objects.order_by('time').first().time.date()
    result = adi.delay(start.strftime("%Y-%m-%d"),
                       end.strftime("%Y-%m-%d"), market.id,
                       start.strftime("%Y-%m-%d"))
    return render(request, 'adi.html', {'task_id': result, 'form': form})


def check_index_status(request):
    task_id = request.GET.get('task_id')
    status = AsyncResult(task_id)
    if status.ready():
        return JsonResponse(status.get(), safe=False)
    else:
        return False
