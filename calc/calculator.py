import math
import os
import openpyxl as xl
from openpyxl import load_workbook
from calc import prices

from PyInstaller.utils.hooks import collect_data_files

# datas = collect_data_files('openpyxl')

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'static/calc/piql_prices.xlsx')
wb = xl.load_workbook(my_file)
sheet = wb['prices']

pr_table = {}
co_table = {}
prices.price_table(pr_table, sheet)
prices.cost_table(co_table, sheet)

# cost_of_service = prices.cost(cost, option)


def dig_price(data):
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
        digital_price = prices.price(pr_table, service)
    return digital_price


def digital_price(data, payment):
    free_reel = 0 if payment == 'only_piqlfilm' else 120
    piqlfilm_digital_price = dig_price(data) if data < 120 else (data - free_reel) * dig_price(data)
    return piqlfilm_digital_price


def vis_price(layout):
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
    visual_price = prices.price(pr_table, service)
    return visual_price


def visual_price(pages, layout, payment):
    free_reel = 0 if payment == 'only_piqlfilm' else 65000 * int(layout)
    piqlfilm_visual_price = prices.price(pr_table, 'offline_visual_less_reel') \
        if (pages / int(layout)) < 65000 else (pages - free_reel) * vis_price(layout)
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


def onl_price(data_online, payment):
    piqlconnect_price = 0
    online_p = 0
    if data_online == 0:
        pass
    else:
        if payment == 'yearly':
            piqlconnect_price = prices.price(pr_table, 'piqlConnect_yearly')
            if data_online < 1000:
                online_p = 0
            else:
                online_p = (data_online - 1000) * prices.price(pr_table, 'online_storage_yearly_gb')
        elif payment == 'monthly':
            piqlconnect_price = prices.price(pr_table, 'piqlConnect_monthly')
            if data_online < 1000:
                online_p = 0
            else:
                online_p = (data_online - 1000) * prices.price(pr_table, 'online_storage_monthly_gb')
    online_price = piqlconnect_price + online_p
    return online_price, piqlconnect_price, online_p


def piqlfilm(data, pages, layout):
    digital_reel = data / 120
    visual_reel = pages / int(layout) / 65000
    reel = math.ceil(digital_reel + visual_reel)
    return reel


def storage_prices(type, data_offline, data_online, pages, layout, payment):
    online_price = 0
    piqlconnect_price = 0
    piqlfilm_price = 0

    if data_online > 0:
        online_price, piqlconnect, online_p = onl_price(data_online, payment)
        if data_offline > 0 or pages > 0:
            piqlfilm_price = offline_type(payment, type, data_offline, pages, layout)
    else:
        payment = 'only_piqlfilm'
        piqlconnect_price = prices.price(pr_table, 'piqlConnect_only_film')
        piqlfilm_price = offline_type(payment, type, data_offline, pages, layout)
    preservation_price = piqlconnect_price + online_price + piqlfilm_price
    return preservation_price, online_price, piqlfilm_price


def awa(decision, entity, storage, reel):
    fee = 0
    storage_awa = 0
    reg_fee = prices.price(pr_table, 'awa_registration_fee')
    mgmt_fee = prices.price(pr_table, 'awa_management_yearly')
    if decision == 'no':
        awa_price = 0
    elif reel == 0:
        awa_price = 0
    else:
        if entity == 'public':
            fee = reg_fee + prices.price(pr_table, 'awa_contribution_public')
        elif entity == 'private':
            fee = reg_fee + prices.price(pr_table, 'awa_contribution_private')
        if storage == '5':
            storage_awa = mgmt_fee + (prices.price(pr_table, 'awa_reel_yearly_5y') * reel)
        elif storage == '10':
            storage_awa = mgmt_fee + (prices.price(pr_table, 'awa_reel_yearly_10y') * reel)
        elif storage == '25':
            storage_awa = mgmt_fee + (prices.price(pr_table, 'awa_reel_yearly_25y') * reel)
        awa_price = fee + storage_awa
    return awa_price, fee, storage_awa


def reader(piqlreader, qty, service):
    support = 0
    installation = prices.price(pr_table, 'piqlReader_installation')
    if piqlreader == 'no':
        piqlreader_price = 0
    else:
        piqlreader = qty * prices.price(pr_table, 'piqlReader')
        if service == 'platinum':
            support = prices.price(pr_table, 'piqlReader_platinum_service')
        elif service == 'gold':
            support = prices.price(pr_table, 'piqlReader_gold_service')
        piqlreader_price = piqlreader + installation + support
    return piqlreader_price, piqlreader, qty, installation, support


def prof_serv(consultacy, days):
    prof_serv_price = days * prices.price(pr_table, 'professional_services_day') if consultacy == 'yes' else 0
    return prof_serv_price, days


def print_order(created, customer, comments, offline, visual, layout, online, payment,
          awa, entity, storage, reel, prof, days, qty, service, total, total_2):
    folder = os.path.dirname(os.path.abspath(__file__))
    my_order = os.path.join(folder, 'static/calc/piql_order_form.xlsx')
    wb2 = xl.load_workbook(my_order)
    sh = wb2['order']

    piqlcon = prices.price(pr_table, 'piqlConnect_only_film')
    online_price, piqlconnect_price, online_p = onl_price(online, payment)
    fee = prices.price(pr_table, 'awa_registration_fee')
    public = prices.price(pr_table, 'awa_contribution_public')
    private = prices.price(pr_table, 'awa_contribution_private')
    management = prices.price(pr_table, 'awa_management_yearly')
    five = prices.price(pr_table, 'awa_reel_yearly_5y')
    ten = prices.price(pr_table, 'awa_reel_yearly_10y')
    twentyfive = prices.price(pr_table, 'awa_reel_yearly_25y')
    prof_price = prices.price(pr_table, 'professional_services_day')
    read = prices.price(pr_table, 'piqlReader')
    inst = prices.price(pr_table, 'piqlReader_installation')
    gold = prices.price(pr_table, 'piqlReader_gold_service')
    platinum = prices.price(pr_table, 'piqlReader_platinum_service')

    sh['G4'] = created
    """sh['G5'] = partner"""
    sh['G7'] = customer
    sh['F10'] = comments

    if online == 0:
        sh['F18'] = 1
        sh['G18'] = piqlcon
        sh['H18'] = piqlcon
        if offline != 0:
            sh['F19'] = offline
            sh['G19'] = dig_price(offline)
            sh['H19'] = digital_price(offline, payment)
        if visual != 0:
            sh['F20'] = visual
            sh['E20'] = layout
            sh['G20'] = vis_price(layout)
            sh['H20'] = visual_price(visual, layout, payment)
    else:
        sh['F21'] = 1
        sh['G21'] = piqlconnect_price
        sh['H21'] = piqlconnect_price
        if offline != 0:
            sh['F19'] = offline
            sh['G19'] = dig_price(offline)
            sh['H19'] = digital_price(offline, payment)
        if visual != 0:
            sh['F20'] = visual
            sh['E20'] = layout
            sh['G20'] = vis_price(layout)
            sh['H20'] = visual_price(visual, layout, payment)
        sh['F22'] = online
        if payment == 'yearly':
            sh['G22'] = prices.price(pr_table, 'online_storage_yearly_gb')
        if payment == 'monthly':
            sh['G22'] = prices.price(pr_table, 'online_storage_monthly_gb')
        sh['H22'] = online_p
        sh['E22'] = payment

    if awa == 'yes':
        sh['E25'] = entity
        sh['E27'] = storage
        sh['F27'] = reel
        sh['F24'] = 1
        sh['G24'] = fee
        sh['H24'] = fee
        sh['F25'] = 1
        if entity == 'public':
            sh['G25'] = public
            sh['H25'] = public
        if entity == 'private':
            sh['G25'] = private
            sh['H25'] = private
        sh['F26'] = 1
        sh['G26'] = management
        sh['H26'] = management
        if storage == '5':
            sh['G27'] = five
            sh['H27'] = five * reel
        if storage == '10':
            sh['G27'] = ten
            sh['H27'] = ten * reel
        if storage == '25':
            sh['G27'] = twentyfive
            sh['H27'] = twentyfive * reel

    if prof == 'yes':
        sh['F28'] = days
        sh['G28'] = prof_price
        sh['H28'] = prof_price * days

    if qty != 0:
        sh['F29'] = qty
        sh['G29'] = read
        sh['H29'] = read * qty
        sh['F30'] = 1
        sh['G30'] = inst
        sh['H30'] = inst
        sh['E31'] = service
        sh['F31'] = 1
        if service == 'gold':
            sh['G31'] = gold
            sh['H31'] = gold
        if service == 'platinum':
            sh['G31'] = platinum
            sh['H31'] = platinum

    if reel != 0:
        sh['E32'] = reel
        if awa == 'yes':
            sh['G32'] = 20
            sh['H32'] = reel * 20
        if awa == 'no':
            sh['G32'] = 30
            sh['H32'] = reel * 30

    sh['H33'] = total
    sh['H32'] = total_2

    wb2.save(my_order)



