from calc import prices as pr, calculator as ca, film
import os
import openpyxl as xl


def clean(sheet):  # clear previous values in the excel sheet
    for a in sheet['G4':'G7']:
        for cell in a:
            cell.value = None
    for a in sheet['E31':'E32']:
        for cell in a:
            cell.value = None
    for a in sheet['F18':'H32']:
        for cell in a:
            cell.value = None
    for a in sheet['H33':'H34']:
        for cell in a:
            cell.value = None
    sheet['F10'] = None
    sheet['E20'] = None
    sheet['E22'] = None
    sheet['E25'] = None
    sheet['E27'] = None


def print_order(created, partner, customer, comments, type, offline, visual, layout, online_data, payment,
          awa, entity, storage, reel, prof, days, piqlreader, qty, service, total, total_2):
    # populate the excel order form with the quantities and prices

    folder = os.path.dirname(os.path.abspath(__file__))
    my_order = os.path.join(folder, 'static/calc/piql_order_form.xlsx')
    wb = xl.load_workbook(my_order)  # open order-form excel file
    sh = wb['order']

    clean(sh)

    piqlcon = pr.price(table, 'piqlConnect_only_film')
    total_online_price, piqlconnect_price, online_price = ca.online(online_data, payment)
    film_pr, digital_pr = film.offline(payment, type, offline, visual, layout, table)
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
    sh['G5'] = partner
    sh['G7'] = customer
    sh['F10'] = comments

    if payment == 'only_piqlreader':
        pass
    else:
        if online_data == 0:
            sh['F18'] = 1
            sh['G18'] = piqlcon
            sh['H18'] = piqlcon
            if offline != 0:
                sh['F19'] = offline
                sh['G19'] = film.digital(offline, table)
                sh['H19'] = digital_pr
            if visual != 0:
                sh['F20'] = visual
                sh['E20'] = layout
                sh['G20'] = film.visual(layout, table)
                sh['H20'] = film.visual_price(visual, layout, payment, table)
        else:
            sh['F21'] = 1
            sh['G21'] = piqlconnect_price
            sh['H21'] = piqlconnect_price
            if offline != 0:
                sh['F19'] = offline
                sh['G19'] = film.digital(offline, table)
                sh['H19'] = digital_pr
            if visual != 0:
                sh['F20'] = visual
                sh['E20'] = layout
                sh['G20'] = film.visual(layout, table)
                sh['H20'] = film.visual_price(visual, layout, payment, table)
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
            sh['H27'] = five * reel * 5
        if storage == '10':
            sh['G27'] = ten
            sh['H27'] = ten * reel * 10
        if storage == '25':
            sh['G27'] = twentyfive
            sh['H27'] = twentyfive * reel * 25

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

    wb.save(my_order)


folder = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(folder, 'static/calc/piql_prices.xlsx')
wb = xl.load_workbook(my_file)
sheet = wb['prices']

table = {}
pr.price_table(table, sheet) # create a dictionary with prices/per service

