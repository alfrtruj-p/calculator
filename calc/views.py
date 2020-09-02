from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from calc import calculator as ca, order
import os

from .forms import InputForm, UserForm
from .models import Input


def data_history(request):
    quotes = Input.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    paginator = Paginator(quotes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'calc/data_history.html', {'quotes': quotes, 'page_obj': page_obj})


def data_quote(request, pk):
    quote = get_object_or_404(Input, pk=pk)
    price, online, offline = ca.piql_prices(quote.type, quote.offline_data, quote.online_data, quote.pages,
                                            quote.layout, quote.payment)

    reel = ca.piqlfilm(quote.offline_data, quote.pages, quote.layout)
    price_awa, fee, storage_awa = ca.awa(quote.awa, quote.awa_contribution, quote.awa_storage, reel)
    price_piqlreader, piqlreader, qty, installation, support = ca.reader(quote.piqlreader, quote.quantity, quote.service)
    price_prof_serv, days = ca.prof_serv(quote.consultancy, quote.days)

    first_year_price = price + price_awa + price_piqlreader + price_prof_serv
    second_year_price = online + storage_awa + support

    args = {'quote': quote, 'price': price, 'offline': offline, 'online': online, 'reel': reel,
            'price_awa': price_awa, 'fee': fee, 'storage_awa': storage_awa, 'first_year_price': first_year_price,
            'second_year_price': second_year_price, 'price_piqlreader': price_piqlreader, 'piqlreader': piqlreader,
            'qty': qty, 'installation': installation, 'support': support, 'price_prof_serv': price_prof_serv,
            'days': days}
    return render(request, 'calc/data_quote.html', args)


def data_order(request, pk):
    quote = get_object_or_404(Input, pk=pk)
    price, online, offline = ca.piql_prices(quote.type, quote.offline_data, quote.online_data, quote.pages,
                                            quote.layout, quote.payment)

    reel = ca.piqlfilm(quote.offline_data, quote.pages, quote.layout)
    price_awa, fee, storage_awa = ca.awa(quote.awa, quote.awa_contribution, quote.awa_storage, reel)
    price_piqlreader, piqlreader, qty, installation, support = ca.reader(quote.piqlreader, quote.quantity, quote.service)
    price_prof_serv, days = ca.prof_serv(quote.consultancy, quote.days)

    first_year_price = price + price_awa + price_piqlreader + price_prof_serv
    second_year_price = online + storage_awa + support

    order_form = order.print_order(quote.created_date, quote.customer_name, quote.comment, quote.offline_data,
                                        quote.pages, quote.layout, quote.online_data, quote.payment, quote.awa,
                                        quote.awa_contribution, quote.awa_storage, reel, quote.consultancy, quote.days,
                                        quote.piqlreader, quote.quantity, quote.service, first_year_price,
                                        second_year_price)

    os.system('start "excel" "C:/Users/AlfredoTrujillo/PycharmProjects/calculator/calc/static/calc/piql_order_form.xlsx"')

    args = {'quote': quote, 'price': price, 'offline': offline, 'online': online, 'reel': reel,
            'price_awa': price_awa, 'fee': fee, 'storage_awa': storage_awa, 'first_year_price': first_year_price,
            'second_year_price': second_year_price, 'price_piqlreader': price_piqlreader, 'piqlreader': piqlreader,
            'qty': qty, 'installation': installation, 'support': support, 'price_prof_serv': price_prof_serv,
            'days': days, 'order_form': order_form}
    return render(request, 'calc/data_order.html', args)


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




