import openpyxl

workbook = openpyxl.load_workbook('inventory.xlsx')

product_list=workbook['Sheet1']

products_per_supplier = {}

for product_row in range(2, product_list.max_row + 1):
    supplier_name = product_list.cell(product_row, 4).value
    inventory = product_list.cell(product_row, 2).value

    if supplier_name in products_per_supplier:
        current_inventory = products_per_supplier[supplier_name]
        products_per_supplier[supplier_name] = current_inventory + inventory
    else:
        products_per_supplier[supplier_name] = inventory



print(products_per_supplier)


product_inventory_below_threshold = []

for product_row in range(2, product_list.max_row + 1):
    
    inventory = product_list.cell(product_row, 2).value
    product_No= product_list.cell(product_row, 1).value

    if inventory < 10:
        product_inventory_below_threshold.append(product_No)

print(product_inventory_below_threshold)



company_inventory = {} 

for product_row in range(2, product_list.max_row + 1):
    company_name = product_list.cell(product_row, 4).value
    inventory_value = product_list.cell(product_row, 3).value

    if company_name in company_inventory:
        current_inventory = company_inventory[company_name]
        company_inventory[company_name] = current_inventory + inventory_value
    else:
        company_inventory[company_name] = inventory_value

print(company_inventory)

product_list.cell(1, 5).value = 'Inventory Value'

for product_row in range(2, product_list.max_row + 1):
    inventory = product_list.cell(product_row, 2).value
    price= product_list.cell(product_row, 3).value

    inventory_price = inventory * price

    product_list.cell(product_row, 5).value = inventory_price

workbook.save('inventory_solution.xlsx')
