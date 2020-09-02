import math
import os
import openpyxl as xl
from calc import prices as pr


folder = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(folder, 'static/calc/piql_prices.xlsx')
wb = xl.load_workbook(my_file)
sheet = wb['prices']

table = {}
pr.price_table(table, sheet)


def digital(data):
    # piqlFilm digital prices per amount of GB
    service = 0
    if data == 0:
        digital_price = 0
    else:
        if data < 120:
            service = 'offline_digital_less_reel'
        elif 120 <= data <= 1000:
            service = 'offline_digital_120gb_1000gb'
        elif 1000 < data <= 5000:
            service = 'offline_digital_1001gb_5000gb'
        elif data > 5000:
            service = 'offline_digital_more_5001gb'
        digital_price = pr.price(table, service)
    return digital_price


def visual(layout):
    # pilqFilm visual prices per number of pages per frame
    service = 0
    if layout == '1':
        service = 'offline_visual_1page_reel'
    elif layout == '2':
        service = 'offline_visual_2pages_reel'
    elif layout == '3':
        service = 'offline_visual_3pages_reel'
    elif layout == '4':
        service = 'offline_visual_4pages_reel'
    elif layout == '6':
        service = 'offline_visual_6pages_reel'
    elif layout == '10':
        service = 'offline_visual_8pages_up_reel'
    visual_price = pr.price(table, service)
    return visual_price


def digital_price(data, payment):
    # calculating piqlFilm digital price minus free reel due to piqlConnect
    free_reel = 0 if payment == 'only_piqlfilm' else 120
    film_dig_price = digital(data) if data < 120 else (data - free_reel) * digital(data)
    return film_dig_price


def visual_price(pages, layout, payment):
    # calculating piqlFilm visual price minus free reel due to piqlConnect
    free_reel = 0 if payment == 'only_piqlfilm' else 65000 * int(layout)
    film_vis_price = pr.price(table, 'offline_visual_less_reel') if (pages / int(layout)) < 65000 else (pages - free_reel) * visual(layout)
    return film_vis_price


def offline(payment, type, data_offline, pages, layout):
    # calculating total piqlFilm prices including digital, visual and hybrid
    digital = 0
    visual = 0
    if type == 'digital':
        digital = digital_price(data_offline, payment)
    elif type == 'visual':
        visual = visual_price(pages, layout, payment)
    elif type == 'hybrid':
        digital = digital_price(data_offline, payment)
        visual = visual_price(pages, layout, payment)
        if payment == 'yearly' or payment == 'monthly':
            digital = digital + pr.price(table, 'offline_digital_less_reel')
    piqlfilm_price = digital + visual
    return piqlfilm_price


def online(data, payment):
    # calculate the online storage prices including piqlConnect
    piqlconnect_price = 0
    online_p = 0
    if data == 0:
        pass
    else:
        if payment == 'yearly':
            piqlconnect_price = pr.price(table, 'piqlConnect_yearly')
            online_p = 0 if data < 1000 else (data - 1000) * pr.price(table, 'online_storage_yearly_gb')
        elif payment == 'monthly':
            piqlconnect_price = pr.price(table, 'piqlConnect_monthly')
            online_p = 0 if data < 1000 else (data - 1000) * pr.price(table, 'online_storage_monthly_gb')
    online_price = piqlconnect_price + online_p
    return online_price, piqlconnect_price, online_p


def piql_prices(type, data_offline, data_online, pages, layout, payment):
    # calculate total prices for online and offline storage including piqlConnect
    online_price = 0
    piqlconnect_price = 0
    film_price = 0
    if data_online > 0:
        online_price, piqlconnect, online_p = online(data_online, payment)
        if data_offline > 0 or pages > 0:
            film_price = offline(payment, type, data_offline, pages, layout)
    else:
        payment = 'only_piqlfilm'
        piqlconnect_price = pr.price(table, 'piqlConnect_only_film')
        film_price = offline(payment, type, data_offline, pages, layout)
    preservation_price = piqlconnect_price + online_price + film_price
    return preservation_price, online_price, film_price


def piqlfilm(data, pages, layout):
    # calculate the number of reels
    digital_reel = data / 120
    visual_reel = pages / int(layout) / 65000
    reel = math.ceil(digital_reel + visual_reel)
    return reel


def awa(decision, entity, storage, reel):
    # calculate the prices for Arctic World Archive
    fee = 0
    storage_awa = 0
    reg_fee = pr.price(table, 'awa_registration_fee')
    mgmt_fee = pr.price(table, 'awa_management_yearly')
    if decision == 'no' or reel == 0:
        awa_price = 0
    else:
        if entity == 'public':
            fee = reg_fee + pr.price(table, 'awa_contribution_public')
        elif entity == 'private':
            fee = reg_fee + pr.price(table, 'awa_contribution_private')
        if storage == '5':
            storage_awa = mgmt_fee + (pr.price(table, 'awa_reel_yearly_5y') * reel)
        elif storage == '10':
            storage_awa = mgmt_fee + (pr.price(table, 'awa_reel_yearly_10y') * reel)
        elif storage == '25':
            storage_awa = mgmt_fee + (pr.price(table, 'awa_reel_yearly_25y') * reel)
        awa_price = fee + storage_awa
    return awa_price, fee, storage_awa


def reader(piqlreader, qty, service):
    # calculate the prices for the piqlReader
    support = 0
    installation = pr.price(table, 'piqlReader_installation')
    if piqlreader == 'no':
        piqlreader_price = 0
    else:
        piqlreader = qty * pr.price(table, 'piqlReader')
        if service == 'platinum':
            support = pr.price(table, 'piqlReader_platinum_service')
        elif service == 'gold':
            support = pr.price(table, 'piqlReader_gold_service')
        piqlreader_price = piqlreader + installation + support
    return piqlreader_price, piqlreader, qty, installation, support


def prof_serv(consultacy, days):
    # calculate the prices for professional services
    prof_serv_price = days * pr.price(table, 'professional_services_day') if consultacy == 'yes' else 0
    return prof_serv_price, days


