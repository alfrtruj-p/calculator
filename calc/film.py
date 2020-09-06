import math
from calc import prices as pr
import os
import openpyxl as xl


def piqlfilm(data, pages, layout):  # calculate the number of reels
    digital_reel = data / 120
    visual_reel = pages / int(layout) / 65000
    reel = math.ceil(digital_reel + visual_reel)
    return reel


def digital(data, table):  # piqlFilm digital prices per amount of GB
    if data == 0:
        digital_pr = 0
    else:
        if data < 120:
            service = 'offline_digital_less_reel'
        elif 120 <= data <= 1000:
            service = 'offline_digital_120gb_1000gb'
        elif 1000 < data <= 5000:
            service = 'offline_digital_1001gb_5000gb'
        else:
            service = 'offline_digital_more_5001gb'
        digital_pr = pr.price(table, service)
    return digital_pr


def visual(layout, table):  # piqlFilm visual prices per number of pages per frame
    vis = {
        "1": "offline_visual_1page_reel",
        "2": "offline_visual_2pages_reel",
        "3": "offline_visual_3pages_reel",
        "4": "offline_visual_4pages_reel",
        "6": "offline_visual_6pages_reel",
        "10": "offline_visual_8pages_up_reel"
    }
    service = 0
    for i in vis.keys():
        if layout == i in vis.keys():
            service = vis.get(i)
    visual_pr = pr.price(table, service)
    return visual_pr


def digital_price(data, payment, table):  # calculating piqlFilm digital price minus free reel due to piqlConnect
    free_reel = 0 if payment == 'only_piqlfilm' else 120
    film_dig_price = digital(data, table) if data < 120 else (data - free_reel) * digital(data, table)
    return film_dig_price


def visual_price(pages, layout, payment, table):  # calculating piqlFilm visual price minus free reel due to piqlConnect
    free_reel = 0 if payment == 'only_piqlfilm' else 65000 * int(layout)
    film_vis_price = pr.price(table, 'offline_visual_less_reel') if (pages / int(layout)) < 65000 else (pages - free_reel) * visual(layout, table)
    return film_vis_price


def offline(payment, type, data_offline, pages, layout, table):  # calculating total piqlFilm prices including all types
    dig = 0
    vis = 0
    if type == 'digital':
        dig = digital_price(data_offline, payment, table)
    elif type == 'visual':
        vis = visual_price(pages, layout, payment, table)
    else:
        dig = digital_price(data_offline, payment, table)
        vis = visual_price(pages, layout, payment, table)
        if payment == 'yearly' or payment == 'monthly':
            dig = dig + pr.price(table, 'offline_digital_less_reel')
    film_price = dig + vis
    return film_price, dig



