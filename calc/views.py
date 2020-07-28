from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from calc import calculator

from .forms import InputForm, UserForm
from .models import Input

# Create your views here.


def data_history(request):
    quotes = Input.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'calc/data_history.html', {'quotes': quotes})


def data_quote(request, pk):
    quote = get_object_or_404(Input, pk=pk)
    #price = calculator.calculation(calculator.piqlConnect_bundle, quote.online_data, calculator.online_price,
                                   #quote.offline_data, calculator.offline_price)
    price = calculator.storage_prices(quote.type, quote.offline_data, quote.online_data, quote.pages,
                                      quote.layout, quote.payment)
    args = {'quote': quote, 'price': price}
    return render(request, 'calc/data_quote.html', args)


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
    args = {'form': form}
    return render(request, 'calc/data_input.html', args)


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
    return render(request, 'calc/data_input.html', {'form': form})


@login_required
def quote_delete(request, pk):
    quote = get_object_or_404(Input, pk=pk)
    quote.delete()
    return redirect('data_history')


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'calc/signup.html', {'form': form})




