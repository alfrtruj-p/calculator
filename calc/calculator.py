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

pricing = {}
cost = {}
prices.price_table(pricing, sheet)
prices.cost_table(cost, sheet)

# cost_of_service = prices.cost_calculation(cost, option)


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
    visual_price = prices.price_calculation(pricing, service)
    return visual_price


def visual_price(pages, layout, payment):
    if payment == 'only_piqlfilm':
        free_reel = 0
    else:
        free_reel = 65000 * int(layout)
    if (pages / int(layout)) < 65000:
        piqlfilm_visual_price = prices.price_calculation(pricing, 'offline_visual_less_reel')
    else:
        piqlfilm_visual_price = (pages - free_reel) * vis_price(layout)
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
            piqlconnect_price = prices.price_calculation(pricing, 'piqlConnect_yearly')
            if data_online < 1000:
                online_p = 0
            else:
                online_p = (data_online - 1000) * prices.price_calculation(pricing, 'online_storage_yearly_gb')
        elif payment == 'monthly':
            piqlconnect_price = prices.price_calculation(pricing, 'piqlConnect_monthly')
            if data_online < 1000:
                online_p = 0
            else:
                online_p = (data_online - 1000) * prices.price_calculation(pricing, 'online_storage_monthly_gb')
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
        piqlconnect_price = prices.price_calculation(pricing, 'piqlConnect_only_film')
        piqlfilm_price = offline_type(payment, type, data_offline, pages, layout)
    preservation_price = piqlconnect_price + online_price + piqlfilm_price
    return preservation_price, online_price, piqlfilm_price


def awa(decision, entity, storage, reel):
    fee = 0
    storage_awa = 0
    reg_fee = prices.price_calculation(pricing, 'awa_registration_fee')
    mgmt_fee = prices.price_calculation(pricing, 'awa_management_yearly')
    if decision == 'no':
        awa_price = 0
    elif reel == 0:
        awa_price = 0
    else:
        if entity == 'public':
            fee = reg_fee + prices.price_calculation(pricing, 'awa_contribution_public')
        elif entity == 'private':
            fee = reg_fee + prices.price_calculation(pricing, 'awa_contribution_private')
        if storage == '5':
            storage_awa = mgmt_fee + (prices.price_calculation(pricing, 'awa_reel_yearly_5y') * reel)
        elif storage == '10':
            storage_awa = mgmt_fee + (prices.price_calculation(pricing, 'awa_reel_yearly_10y') * reel)
        elif storage == '25':
            storage_awa = mgmt_fee + (prices.price_calculation(pricing, 'awa_reel_yearly_25y') * reel)
        awa_price = fee + storage_awa
    return awa_price, fee, storage_awa


def reader(piqlreader, qty, service):
    support = 0
    installation = prices.price_calculation(pricing, 'piqlReader_installation')
    if piqlreader == 'no':
        piqlreader_price = 0
    else:
        piqlreader = qty * prices.price_calculation(pricing, 'piqlReader')
        if service == 'platinum':
            support = prices.price_calculation(pricing, 'piqlReader_platinum_service')
        elif service == 'gold':
            support = prices.price_calculation(pricing, 'piqlReader_gold_service')
        piqlreader_price = piqlreader + installation + support
    return piqlreader_price, piqlreader, qty, installation, support


def prof_serv(consultacy, days):
    if consultacy == 'yes':
        prof_serv_price = days * prices.price_calculation(pricing, 'professional_services_day')
    else:
        prof_serv_price = 0
    return prof_serv_price, days


def print_order(created, customer, comments, offline, visual, layout, online, payment,
          awa, entity, storage, reel, prof, days, qty, service, total, total_2):
    FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_order = os.path.join(FOLDER, 'static/calc/piql_order_form.xlsx')
    wb2 = xl.load_workbook(my_order)
    sheet_order = wb2['order']

    date = sheet_order.cell(4, 7)
    date.value = created
    """piql_partner = sheet_order.cell(5, 7)
    piql_partner.value = partner"""
    client = sheet_order.cell(7, 7)
    client.value = customer
    notes = sheet_order.cell(10, 6)
    notes.value = comments

    piqlcon = prices.price_calculation(pricing, 'piqlConnect_only_film')
    online_price, piqlconnect_price, online_p = onl_price(online, payment)
    fee = prices.price_calculation(pricing, 'awa_registration_fee')
    public = prices.price_calculation(pricing, 'awa_contribution_public')
    private = prices.price_calculation(pricing, 'awa_contribution_private')
    management = prices.price_calculation(pricing, 'awa_management_yearly')
    five = prices.price_calculation(pricing, 'awa_reel_yearly_5y')
    ten = prices.price_calculation(pricing, 'awa_reel_yearly_10y')
    twentyfive = prices.price_calculation(pricing, 'awa_reel_yearly_25y')
    prof_price = prices.price_calculation(pricing, 'professional_services_day')
    read = prices.price_calculation(pricing, 'piqlReader')
    inst = prices.price_calculation(pricing, 'piqlReader_installation')
    gold = prices.price_calculation(pricing, 'piqlReader_gold_service')
    platinum = prices.price_calculation(pricing, 'piqlReader_platinum_service')

    if online == 0:
        piqlconnect_qty = sheet_order.cell(18, 6)
        piqlconnect_qty.value = 1
        piqlconnect = sheet_order.cell(18, 7)
        piqlconnect.value = piqlcon
        piqlconnect_t = sheet_order.cell(18, 8)
        piqlconnect_t.value = piqlcon
        if offline != 0:
            data_offline = sheet_order.cell(19, 6)
            data_offline.value = offline
            digital_pr = sheet_order.cell(19, 7)
            digital_pr.value = dig_price(offline)
            digital_pr_t = sheet_order.cell(19, 8)
            digital_pr_t.value = digital_price(offline, payment)
        if visual != 0:
            pages_offline = sheet_order.cell(20, 6)
            pages_offline.value = visual
            pg_pr_frame = sheet_order.cell(20, 5)
            pg_pr_frame.value = layout
            visual_pr = sheet_order.cell(20, 7)
            visual_pr.value = vis_price(layout)
            visual_pr_t = sheet_order.cell(20, 8)
            visual_pr_t.value = visual_price(visual, layout, payment)
    else:
        piqlconnect_online_qty = sheet_order.cell(21, 6)
        piqlconnect_online_qty.value = 1
        piqlconnect_online = sheet_order.cell(21, 7)
        piqlconnect_online.value = piqlconnect_price
        piqlconnect_online = sheet_order.cell(21, 8)
        piqlconnect_online.value = piqlconnect_price
        if offline != 0:
            data_offline = sheet_order.cell(19, 6)
            data_offline.value = offline
            digital_pr = sheet_order.cell(19, 7)
            digital_pr.value = dig_price(offline)
            digital_pr_t = sheet_order.cell(19, 8)
            digital_pr_t.value = digital_price(offline, payment)
        if visual != 0:
            pages_offline = sheet_order.cell(20, 6)
            pages_offline.value = visual
            pg_pr_frame = sheet_order.cell(20, 5)
            pg_pr_frame.value = layout
            visual_pr = sheet_order.cell(20, 7)
            visual_pr.value = vis_price(layout)
            visual_pr_t = sheet_order.cell(20, 8)
            visual_pr_t.value = visual_price(visual, layout, payment)
        online_pr = sheet_order.cell(22, 6)
        online_pr.value = online
        online_pr_t = sheet_order.cell(22, 7)
        if payment == 'yearly':
            online_pr_t.value = prices.price_calculation(pricing, 'online_storage_yearly_gb')
        if payment == 'monthly':
            online_pr_t.value = prices.price_calculation(pricing, 'online_storage_monthly_gb')
        online_pr_t = sheet_order.cell(22, 8)
        online_pr_t.value = online_p
        pay = sheet_order.cell(22, 5)
        pay.value = payment

    if awa == 'yes':
        company = sheet_order.cell(25, 5)
        company.value = entity
        awastorage = sheet_order.cell(27, 5)
        awastorage.value = storage
        film = sheet_order.cell(27, 6)
        film.value = reel
        reg_fee_qty = sheet_order.cell(24, 6)
        reg_fee_qty.value = 1
        reg_fee = sheet_order.cell(24, 7)
        reg_fee.value = fee
        reg_fee_t = sheet_order.cell(24, 8)
        reg_fee_t.value = fee
        contrib_qty = sheet_order.cell(25, 6)
        contrib_qty.value = 1
        contrib = sheet_order.cell(25, 7)
        contrib_t = sheet_order.cell(25, 8)
        if entity == 'public':
            contrib.value = public
            contrib_t.value = public
        if entity == 'private':
            contrib.value = private
            contrib_t.value = private
        mgmt = sheet_order.cell(26, 6)
        mgmt.value = 1
        mgmt = sheet_order.cell(26, 7)
        mgmt.value = management
        mgmt = sheet_order.cell(26, 8)
        mgmt.value = management
        storage_pr = sheet_order.cell(27, 7)
        storage_pr_t = sheet_order.cell(27, 8)
        if storage == '5':
            storage_pr.value = five
            storage_pr_t.value = five * reel
        if storage == '10':
            storage_pr.value = ten
            storage_pr_t.value = ten * reel
        if storage == '25':
            storage_pr.value = twentyfive
            storage_pr_t.value = twentyfive * reel

    if prof == 'yes':
        duration = sheet_order.cell(28, 6)
        duration.value = days
        prof_pr = sheet_order.cell(28, 7)
        prof_pr.value = prof_price
        prof_pr_t = sheet_order.cell(28, 8)
        prof_pr_t.value = prof_price * days

    if qty != 0:
        quantity = sheet_order.cell(29, 6)
        quantity.value = qty
        reader_pr = sheet_order.cell(29, 7)
        reader_pr.value = read
        reader_pr_t = sheet_order.cell(29, 8)
        reader_pr_t.value = read * qty
        install = sheet_order.cell(30, 6)
        install.value = 1
        install_pr = sheet_order.cell(30, 7)
        install_pr.value = inst
        install_pr_t = sheet_order.cell(30, 8)
        install_pr_t.value = inst
        agreement = sheet_order.cell(31, 5)
        agreement.value = service
        agreement_qty = sheet_order.cell(31, 6)
        agreement_qty.value = 1
        agreement_pr = sheet_order.cell(31, 7)
        agreement_pr_t = sheet_order.cell(31, 8)
        if service == 'gold':
            agreement_pr.value = gold
            agreement_pr_t.value = gold
        if service == 'platinum':
            agreement_pr.value = platinum
            agreement_pr_t.value = platinum

    if reel != 0:
        reel_2 = sheet_order.cell(32, 5)
        reel_2.value = reel
        ship = sheet_order.cell(32, 7)
        ship_t = sheet_order.cell(32, 8)
        if awa == 'yes':
            ship.value = 20
            ship_t.value = reel * 20
        if awa == 'no':
            ship.value = 30
            ship_t.value = reel * 30

    first_year = sheet_order.cell(33, 8)
    first_year.value = total
    second_year = sheet_order.cell(34, 8)
    second_year.value = total_2

    wb2.save(my_order)



