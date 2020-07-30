import os
import openpyxl as xl
from calc import prices

from PyInstaller.utils.hooks import collect_data_files

# datas = collect_data_files('openpyxl')

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'static/piql_prices.xlsx')
wb = xl.load_workbook(my_file)
sheet = wb['prices']

pricing = {}
cost = {}
prices.price_table(pricing, sheet)
prices.cost_table(cost, sheet)

# cost_of_service = prices.cost_calculation(cost, option)


def dig_price(data):
    if data < 120:
        service = 'offline_digital_less_reel'
    elif 120 < data <= 1000:
        service = 'offline_digital_120gb_1000gb'
    elif 1000 < data <= 5000:
        service = 'offline_digital_1001gb_5000gb'
    else:
        service = 'offline_digital_more_5001gb'
    digital_price = prices.price_calculation(pricing, service)
    return digital_price


def digital_price(data, payment):
    if payment == 'only_piqlfilm':
        free_reel = 0
    else:
        free_reel = 120
    if data < 120:
        piqlfilm_digital_price = dig_price(data)
    else:
        piqlfilm_digital_price = (data - free_reel) * dig_price(data)
    return piqlfilm_digital_price


def vis_price(layout):
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
    visual_price = prices.price_calculation(pricing, service)
    return visual_price


def visual_price(pages, layout, payment):
    if payment == 'only_piqlfilm':
        free_reel = 0
    else:
        free_reel = 65000 * int(layout)
    if pages/int(layout) < 65000:
        piqlfilm_visual_price = prices.price_calculation(pricing, 'offline_visual_less_reel')
    else:
        piqlfilm_visual_price = (pages - free_reel) * vis_price(layout)
    print(piqlfilm_visual_price)
    return piqlfilm_visual_price


def offline_type(payment, type, data_offline, pages, layout):
    offline_digital = 0
    offline_visual = 0
    if type == 'digital':
        offline_digital = digital_price(data_offline, payment)
    elif type == 'visual':
        offline_visual = visual_price(pages, layout, payment)
    elif type == 'hybrid':
        offline_digital = digital_price(data_offline, payment)
        offline_visual = visual_price(pages, layout, payment)
    piqlfilm_price = offline_digital + offline_visual
    return piqlfilm_price


def storage_prices(type, data_offline, data_online, pages, layout, payment):
    online_price = 0
    piqlconnect_price = 0
    piqlfilm_price = 0
    if payment == 'only_piqlfilm':
        piqlconnect_price = prices.price_calculation(pricing, 'piqlConnect_only_film')
        piqlfilm_price = offline_type(payment, type, data_offline, pages, layout)
    elif payment == 'yearly':
        piqlconnect_price = prices.price_calculation(pricing, 'piqlConnect_yearly')
        print(piqlconnect_price)
        online_price = (data_online - 1000) * prices.price_calculation(pricing, 'online_storage_yearly_gb')
        print(online_price)
        if data_offline > 0 or pages > 0:
            piqlfilm_price = offline_type(payment, type, data_offline, pages, layout)
            print(piqlfilm_price)
    elif payment == 'monthly':
        piqlconnect_price = prices.price_calculation(pricing, 'piqlConnect_monthly')
        online_price = (data_online - 1000) * prices.price_calculation(pricing, 'online_storage_monthly_gb')
        if data_offline > 0 or pages > 0:
            piqlfilm_price = offline_type(payment, type, data_offline, pages, layout)
    preservation_price = piqlconnect_price + online_price + piqlfilm_price
    return preservation_price