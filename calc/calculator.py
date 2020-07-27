import os
import openpyxl as xl
from calc import prices
from PyInstaller.utils.hooks import collect_data_files

#datas = collect_data_files('openpyxl')

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'static/calc/piql_prices.xlsx')
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
online = 3000.0
offline = 360.0

#storage = input('What storage service would you like to buy (online/offline/both): ')

def calculation(piqlConnect_bundle, online, online_price, offline, offline_price):
    offline_total_price = 0
    online_total_price = 0
    if offline >= 120.0:    # calculate offline storage price
        #type_preserv = input('Do you want digital/visual/both: ')
        offline_total_price = (offline - 120.0) * offline_price
        number_reels = offline / 120
        #copy_price = 0
        #service_name = ''
        #if type_preserv == 'digital':
    if online >=1000.0:
        online_total_price = (online - 1000.0) * online_price
    total_price = piqlConnect_bundle + offline_total_price + online_total_price
    return total_price


    #copies = input('Do you want piqlFilm copies (yes/no): ')
    #sh = sheet3
    #service_name = sheet.cell(2, 1)
    #offline_digital_table = {}
    #sales_price = prices.offline_price(offline_digital_table, data, 0, sheet)
    #want_copy = film_copies(copies, sheet)
    #copy_price = sales_price * want_copy
    """else:
        pages = int(input('How many pages: '))
        num_pag_frame = int(input('How many pages per frame: '))
        copies = input('Do you want piqlFilm copies (yes/no): ')
        sh = sheet4
        service_name = sh.cell(2, 1)
        offline_visual_table = {}
        sales_price = prices.offline_price(offline_visual_table, pages, num_pag_frame, sh)
        want_copy = film_copies(copies, sh)
        copy_price = sales_price * want_copy
    paym = 'once'
    sh = sheet1
    piqlconnect = {}
    pqlconct = prices.cloud_price(piqlconnect, paym, sh)
    shipment = float(input('What is the shipment cost: '))
    print('')
    print(f'piqlConnect price is {pqlconct} euros')
    print(f'The {service_name.value} price is {sales_price} euros')
    print(f'The price per copy: {copy_price} euros')
    print(f'The shipment cost is {shipment} euros')
    print('')
    total = sales_price + copy_price + pqlconct + shipment
    print(f'TOTAL of the project: {total} euros')
else:                                                                   # calculate online storage price
    paym = ""
    sh = sheet1
    piqlconnect = {}
    pqlconct = prices.cloud_price(piqlconnect, paym, sh)
    data = float(input('How much data in online storage (GB): '))
    sh = sheet2
    service_name = sh.cell(2, 1)
    online = {}
    online_price = prices.cloud_price(online, paym, sh)
    online_storage = round(online_price * data, 2)
    print('')
    print(f'piqlConnect price: {pqlconct} euros per month')
    print(f'The {service_name.value} price is {online_storage} euros per month')
    total = online_storage + pqlconct
    print('')
    print(f'TOTAL: {total} euros per month')"""