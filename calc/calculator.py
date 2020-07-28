import os
import openpyxl as xl
from calc import prices

from PyInstaller.utils.hooks import collect_data_files
#datas = collect_data_files('openpyxl')

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'static/piql_prices.xlsx')
wb = xl.load_workbook(my_file)
sheet = wb['prices']

pricing = {}
cost = {}
prices.price_table(pricing, sheet)
prices.cost_table(cost, sheet)

piqlConnect_bundle = prices.price_calculation(pricing, 'piqlConnect_yearly')
online_price = prices.price_calculation(pricing, 'online_storage_monthly_gb')
offline_price = prices.price_calculation(pricing, 'offline_digital_less_reel')
#cost_of_service = prices.cost_calculation(cost, option)

# fix this part, missing the visual only film, but also to refactor it
def digital_price_only_film(data):
    if data <= 120:
        piqlfilm_digital_price = prices.price_calculation(pricing, 'offline_digital_less_reel')
    elif 120 > data >= 1000:
        piqlfilm_digital_price = data * prices.price_calculation(pricing, 'offline_digital_120gb_1000gb')
    elif 1000 > data >= 5000:
        piqlfilm_digital_price = data * prices.price_calculation(pricing, 'offline_digital_1001gb_5000gb')
    else:
        piqlfilm_digital_price = data * prices.price_calculation(pricing, 'offline_digital_more_5001gb')
    return piqlfilm_digital_price


def digital_price(data):
    if data <= 120:
        piqlfilm_digital_price = 0
    elif 120 > data >= 1000:
        piqlfilm_digital_price = (data - 120) * prices.price_calculation(pricing, 'offline_digital_120gb_1000gb')
    elif 1000 > data >= 5000:
        piqlfilm_digital_price = (data - 120) * prices.price_calculation(pricing, 'offline_digital_1001gb_5000gb')
    else:
        piqlfilm_digital_price = (data - 120) * prices.price_calculation(pricing, 'offline_digital_more_5001gb')
    return piqlfilm_digital_price


def visual_price(pages, layout):
    if pages <= 65000:
        piqlfilm_visual_price = 0
    else:
        if layout == '1':
            piqlfilm_visual_price = pages * layout * prices.price_calculation(pricing, 'offline_visual_1page_reel')
        elif layout == '2':
            piqlfilm_visual_price = pages * layout * prices.price_calculation(pricing, 'offline_visual_2pages_reel')
        elif layout == '3':
            piqlfilm_visual_price = pages * layout * prices.price_calculation(pricing, 'offline_visual_3pages_reel')
        elif layout == '4':
            piqlfilm_visual_price = pages * layout * prices.price_calculation(pricing, 'offline_visual_4pages_reel')
        elif layout == '6':
            piqlfilm_visual_price = pages * layout * prices.price_calculation(pricing, 'offline_visual_6pages_reel')
        elif layout >= '8':
            piqlfilm_visual_price = pages * layout * prices.price_calculation(pricing, 'offline_visual_8pages_up_reel')
    return piqlfilm_visual_price


def offline_type(type, data_offline, pages, layout):
    offline_digital = 0
    offline_visual = 0
    if type == 'digital':
        offline_digital = digital_price(data_offline)
    elif type == 'visual':
        offline_visual = visual_price(pages, layout)
    elif type == 'hybrid':
        offline_digital = digital_price(data_offline)
        offline_visual = visual_price(pages, layout)
    piqlfilm_price = offline_digital + offline_visual
    return piqlfilm_price


def storage_prices(type, data_offline, data_online, pages, layout, payment):
    online_price = 0
    piqlconnect_price = 0
    piqlfilm_price = 0
    if payment == 'only_piqlfilm':
        piqlconnect_price = prices.price_calculation(pricing, 'piqlConnect_only_film')
        piqlfilm_price = offline_type(type, data_offline, pages, layout)
    elif payment == 'yearly':
        piqlconnect_price = prices.price_calculation(pricing, 'piqlConnect_yearly')
        online_price = (data_online - 1000) * prices.price_calculation(pricing, 'online_storage_yearly_gb')
        if data_offline > 0:
            piqlfilm_price = offline_type(type, data_offline, pages, layout)
    elif payment == 'monthly':
        piqlconnect_price = prices.price_calculation(pricing, 'piqlConnect_monthly')
        online_price = (data_online - 1000) * prices.price_calculation(pricing, 'online_storage_monthly_gb')
        if data_offline > 0:
            piqlfilm_price = offline_type(type, data_offline, pages, layout)
    preservation_price = piqlconnect_price + online_price + piqlfilm_price
    return preservation_price


def calculation(piqlConnect_bundle, online, online_price, offline, offline_price):
    offline_total_price = 0
    online_total_price = 0
    if offline >= 120.0:
        offline_total_price = (offline - 120.0) * offline_price
        number_reels = offline / 120
    if online >=1000.0:
        online_total_price = (online - 1000.0) * online_price
    total_price = piqlConnect_bundle + offline_total_price + online_total_price
    return total_price





