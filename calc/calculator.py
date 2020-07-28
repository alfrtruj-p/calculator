import os
import openpyxl as xl
from calc import prices

from PyInstaller.utils.hooks import collect_data_files

#datas = collect_data_files('openpyxl')

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'static/piql_prices.xlsx')
wb = xl.load_workbook(my_file)
sheet = wb['prices']

#option = input('What option would you like to buy: ')

pricing = {}
cost = {}
prices.price_table(pricing, sheet)
#prices.cost_table(cost, sheet)

piqlConnect_bundle = prices.price_calculation(pricing, 'piqlConnect_yearly')
online_price = prices.price_calculation(pricing, 'online_storage_monthly_gb')
offline_price = prices.price_calculation(pricing, 'offline_digital_less_reel')
#price_of_service = prices.price_calculation(pricing, 'piqlConnect_yearly')
#cost_of_service = prices.cost_calculation(cost, option)
#print(price_of_service)
#print(cost_of_service)

#storage = input('What storage service would you like to buy (online/offline/both): ')

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





