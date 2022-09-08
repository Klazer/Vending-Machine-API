import pip._vendor.requests

BASE = "http://127.0.0.1:5000/" #My localhost IP, please change as you see fit

#PLEASE ENSURE THAT THE SERVER HAS RESTARTED BEFORE EXECUTING THIS PYTEST SCRIPT
#To do so, simply re-execute the webserver by running the vending_api script again!

def test_get_inventory():
    '''Test function so that users can see all of the inventory for the vending machine'''
    
    response = pip._vendor.requests.get(BASE + "inventory")
    assert response.json()["inventory"] == [5, 5, 5]
    # print(response.json()["inventory"])
    
def test_get_inventory_item():
    '''Test that users can actually retrieve current quantities of a drink'''
    
    response0 = pip._vendor.requests.get(BASE + "inventory/0")
    response1 = pip._vendor.requests.get(BASE + "inventory/1")
    response2 = pip._vendor.requests.get(BASE + "inventory/2")
    response3 = pip._vendor.requests.get(BASE + "inventory/3")
    
    assert response0.json()["item_0_quantity"] == 5
    assert response1.json()["item_1_quantity"] == 5
    assert response2.json()["item_2_quantity"] == 5
    
    assert response3.json()["message"] == "Item of id 3 not found. Please try again" #Test for item out of bounds
    assert response3.status_code == 404
    
    
def test_put_and_delete_coins():
    '''Test function to check the addition of coins and deletion of them. Ensures
    that coins were added properly as the number of added coins should be returned during
    the DELETE method'''
    
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    response = pip._vendor.requests.delete(BASE)
    assert int(response.headers["X-Coins"]) == 3
    
def test_buy_items():
    '''Test function to make sure users can buy a single drink and get
    their coins returned to them at the end of the function. Also ensures
    that the inventory for that drink has changed in the array'''
    
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    response = pip._vendor.requests.put(BASE + "inventory/1")
    
    assert int(response.json()["quantity"]) == 1
    assert int(response.headers["X-Coins"]) == 1
    assert int(response.headers["1-Inventory-Remaining"]) == 4
    
def test_invalid_id_buying():
    '''Test function to make sure status code is 404 when trying to buy an item out of the range
    of the index or not in the inventory'''
    
    pip._vendor.requests.delete(BASE)
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    response = pip._vendor.requests.put(BASE + "inventory/445")
    
    assert response.status_code == 404
    assert int(response.headers["X-Coins"]) == 2
    
def test_not_enough_coins():
    '''Test function to test if there are not enough coins to make a purchase.
    Should return the X-coins header representing how many coins are currently in the machine
    and a 403 status code'''
    
    pip._vendor.requests.delete(BASE)
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    response = pip._vendor.requests.put(BASE + "inventory/2")
    
    assert response.status_code == 403
    assert int(response.headers["X-Coins"]) == 1 or int(response.headers["X-Coins"]) == 0


# response = pip._vendor.requests.get(BASE + "inventory")
# print(response.json())
# time.sleep(2.4)
# response = pip._vendor.requests.put(BASE, json = data)
# print(response.json())
# time.sleep(2.5)
# response = pip._vendor.requests.put(BASE + "inventory/2")
# print(response.json())
# response = pip._vendor.requests.delete(BASE)
# print(response.json())
