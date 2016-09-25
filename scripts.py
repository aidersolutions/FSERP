#unused files
def find_inventory(name):
    inventory_list=Inventory.find()
    for i in inventory_list:
        for j in i.lines:
            if j.product.template.name==name:
                print i.batch_number,j.quantity
