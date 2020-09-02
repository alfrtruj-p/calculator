
def price_table(table, sheet):  # create a price table for all services
    for row in range(2, sheet.max_row + 1):
        cellname = sheet.cell(row, 1)
        cell = sheet.cell(row, 2)
        table[cellname.value] = cell.value
    return table


def price(table, option):  # get an specific price from the price table
    for i in table.keys():
        if option == i in table.keys():
            price = table.get(i)
            return price


def cost_table(table_cost, sheet):  # create a cost table for all services
    for row in range(2, sheet.max_row + 1):
        cellname = sheet.cell(row, 1)
        cell = sheet.cell(row, 3)
        table_cost[cellname.value] = cell.value
    return table_cost


def cost(table_cost, option):  # get an specific cost from the cost table
    for i in table_cost.keys():
        if option == i in table_cost.keys():
            price = table_cost.get(i)
            return price









