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


"""def print_order(created, customer, comments, offline, visual, layout, online_data, payment,
          awa, entity, storage, reel, prof, days, piqlreader, qty, service, total, total_2):
    # populate the excel order form with the quantities and prices

    folder = os.path.dirname(os.path.abspath(__file__))
    my_order = os.path.join(folder, 'static/calc/piql_order_form.xlsx')
    wb2 = xl.load_workbook(my_order)
    sh = wb2['order']

    # clear previous values in the excel sheet
    for a in sh['G4':'G7']:
        for cell in a:
            cell.value = None
    for a in sh['E31':'E32']:
        for cell in a:
            cell.value = None
    for a in sh['F18':'H32']:
        for cell in a:
            cell.value = None
    for a in sh['H33':'H34']:
        for cell in a:
            cell.value = None
    sh['F10'] = None
    sh['E20'] = None
    sh['E22'] = None
    sh['E25'] = None
    sh['E27'] = None

    piqlcon = pr.price(table, 'piqlConnect_only_film')
    total_online_price, piqlconnect_price, online_price = online(online_data, payment)
    fee = pr.price(table, 'awa_registration_fee')
    public = pr.price(table, 'awa_contribution_public')
    private = pr.price(table, 'awa_contribution_private')
    management = pr.price(table, 'awa_management_yearly')
    five = pr.price(table, 'awa_reel_yearly_5y')
    ten = pr.price(table, 'awa_reel_yearly_10y')
    twentyfive = pr.price(table, 'awa_reel_yearly_25y')
    prof_price = pr.price(table, 'professional_services_day')
    read = pr.price(table, 'piqlReader')
    inst = pr.price(table, 'piqlReader_installation')
    gold = pr.price(table, 'piqlReader_gold_service')
    platinum = pr.price(table, 'piqlReader_platinum_service')

    sh['G4'] = created
    # sh['G5'] = partner
    sh['G7'] = customer
    sh['F10'] = comments

    if payment == 'only_piqlreader':
        pass
    else:
        if online == 0:
            sh['F18'] = 1
            sh['G18'] = piqlcon
            sh['H18'] = piqlcon
            if offline != 0:
                sh['F19'] = offline
                sh['G19'] = digital(offline)
                sh['H19'] = digital_price(offline, payment)
            if visual != 0:
                sh['F20'] = visual
                sh['E20'] = layout
                sh['G20'] = visual(layout)
                sh['H20'] = visual_price(visual, layout, payment)
        else:
            sh['F21'] = 1
            sh['G21'] = piqlconnect_price
            sh['H21'] = piqlconnect_price
            if offline != 0:
                sh['F19'] = offline
                sh['G19'] = digital(offline)
                sh['H19'] = digital_price(offline, payment)
            if visual != 0:
                sh['F20'] = visual
                sh['E20'] = layout
                sh['G20'] = visual(layout)
                sh['H20'] = visual_price(visual, layout, payment)
            sh['F22'] = online_data
            if payment == 'yearly':
                sh['G22'] = pr.price(table, 'online_storage_yearly_gb')
            if payment == 'monthly':
                sh['G22'] = pr.price(table, 'online_storage_monthly_gb')
            sh['H22'] = online_price
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

    if piqlreader == 'yes':
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
    sh['H34'] = total_2

    wb2.save(my_order)"""


