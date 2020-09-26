import os
import openpyxl as xl
from calc import prices as pr, film
from calculator import settings


def online_tier(data):  # calculate the online storage price per terabyte stored
    free_tb = 1000
    if data < 1000:
        online_p = 0
    else:
        if 1000 < data <= 50999:
            online_p = (data - free_tb) * pr.price(table, 'online_storage_0_50_tb')
        elif 51000 <= data <= 100999:
            online_p = (data - free_tb) * pr.price(table, 'online_storage_51_100_tb')
        else:
            online_p = (data - free_tb) * pr.price(table, 'online_storage_100_up_tb')
    return online_p


def online(data, payment):  # calculate the online storage prices including piqlConnect
    piqlconnect_price = 0
    online_p = 0
    if data == 0:
        pass
    else:
        if payment == 'yearly':
            piqlconnect_price = pr.price(table, 'piqlConnect_yearly')
            online_p = online_tier(data)

        elif payment == 'monthly':
            piqlconnect_price = pr.price(table, 'piqlConnect_monthly')
            online_p = online_tier(data)
    online_price = piqlconnect_price + online_p
    return online_price, piqlconnect_price, online_p


def piql_prices(type, data_offline, data_online, pages, layout, payment):
    # calculate total prices for online and offline storage including piqlConnect
    online_price = 0
    piqlconnect_price = 0
    film_price = 0
    piqlconnect_bundle = 0
    if data_online > 0:
        online_price, piqlconnect_bundle, online_p = online(data_online, payment)
        if data_offline > 0 or pages > 0:
            film_price, vis = film.offline(payment, type, data_offline, pages, layout, table)
    else:
        payment = 'only_piqlfilm'
        piqlconnect_price = pr.price(table, 'piqlConnect_only_film')
        film_price, vis = film.offline(payment, type, data_offline, pages, layout, table)
    preservation_price = piqlconnect_price + online_price + film_price
    return preservation_price, online_price, piqlconnect_bundle, film_price, piqlconnect_price


def awa(decision, entity, storage, reel):  # calculate the prices for Arctic World Archive
    reg_fee = pr.price(table, 'awa_registration_fee')
    con_fee = 0
    storage_awa = 0
    mgmt_fee = 0
    if decision == 'no' or reel == 0:
        awa_price = 0
    else:
        con_fee = pr.price(table, 'awa_contribution_public') if entity == 'public' else pr.price(table, 'awa_contribution_private')
        if storage == '5':
            mgmt_fee = pr.price(table, 'awa_management_yearly') * 5
            storage_awa = pr.price(table, 'awa_reel_yearly_5y') * reel * 5
        elif storage == '10':
            mgmt_fee = pr.price(table, 'awa_management_yearly') * 10
            storage_awa = pr.price(table, 'awa_reel_yearly_10y') * reel * 10
        else:
            mgmt_fee = pr.price(table, 'awa_management_yearly') * 25
            storage_awa = pr.price(table, 'awa_reel_yearly_25y') * reel * 25
        awa_price = reg_fee + con_fee + mgmt_fee + storage_awa
    return awa_price, reg_fee, con_fee, mgmt_fee, storage_awa


def reader(piqlreader, qty, service):  # calculate the prices for the piqlReader
    support = 0
    installation = pr.price(table, 'piqlReader_installation')
    if piqlreader == 'no':
        piqlreader_price = 0
    else:
        piqlreader = qty * pr.price(table, 'piqlReader')
        support = pr.price(table, 'piqlReader_platinum_service') if service == 'platinum' else pr.price(table, 'piqlReader_gold_service')
        piqlreader_price = piqlreader + installation + support
    return piqlreader_price, piqlreader, qty, installation, support


def prof_serv(consultacy, days):  # calculate the prices for professional services
    prof_serv_price = days * pr.price(table, 'professional_services_day') if consultacy == 'yes' else 0
    return prof_serv_price, days


folder = settings.BASE_DIR
my_file = os.path.join(folder, 'calc/static/calc/piql_prices.xlsx')
wb = xl.load_workbook(my_file)
sheet = wb['prices']

table = {}
pr.price_table(table, sheet)  # create a dictionary with prices/per service from excel sheet


x = online(3000, 'yearly')
print(x)