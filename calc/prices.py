
def price_table(service_prices, sheet):  # create a price table for a service (dictionary)
    for row in range(2, sheet.max_row + 1):
        cellname = sheet.cell(row, 1)
        cell = sheet.cell(row, 2)
        service_prices[cellname.value] = cell.value
    return service_prices


def price_calculation(service, option):
    for i in service.keys():
        if option == i in service.keys():
            price = service.get(i)
            return price


def cost_table(service_cost, sheet):  # create a price table for a service (dictionary)
    for row in range(2, sheet.max_row + 1):
        cellname = sheet.cell(row, 1)
        cell = sheet.cell(row, 3)
        service_cost[cellname.value] = cell.value
    return service_cost


def cost_calculation(service, option):
    for i in service.keys():
        if option == i in service.keys():
            price = service.get(i)
            return price









