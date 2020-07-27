from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from calc import calculator

from .forms import InputForm
from .models import Input

# Create your views here.


def data_quote(request, pk):
    quote = get_object_or_404(Input, pk=pk)
    #price = calculator.calculation(calculator.piqlConnect_bundle, calculator.online, calculator.online_price, calculator.offline, calculator.offline_price)
    stuff_for_frontend = {'quote': quote}
    return render(request, 'calc/data_quote.html', stuff_for_frontend)


@login_required
def data_input(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            input = form.save(commit=False)
            input.partner_name = request.user
            input.created_date = timezone.now()
            input.save()
            return redirect('data_quote', pk=input.pk)
    else:
        form = InputForm()
        stuff_for_frontend = {'form': form}

    return render(request, 'calc/data_input.html', stuff_for_frontend)


@login_required
def data_edit(request, pk):
    input = get_object_or_404(Input, pk=pk)
    if request.method == 'POST':
        # updating an existing form
        form = InputForm(request.POST, instance=input)
        if form.is_valid():
            input = form.save(commit=False)
            input.partner_name = request.user
            input.created_date = timezone.now()
            input.save()
            return redirect('data_quote', pk=input.pk)
    else:
        form = InputForm(instance=input)
        stuff_for_frontend = {'form': form}
    return render(request, 'calc/data_input.html', stuff_for_frontend)


def data_history(request):
    quotes = Input.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    stuff_for_frontend = {'quotes': quotes}
    return render(request, 'calc/data_history.html', stuff_for_frontend)
