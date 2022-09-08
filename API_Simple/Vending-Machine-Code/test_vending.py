import pip._vendor.requests
import time

BASE = "http://127.0.0.1:5000/"

data = {"coins": -2}
# headers = {"Content-Type": "application/json"}

def test_get_inventory():
    response = pip._vendor.requests.get(BASE + "inventory")
    assert response.json()["inventory"] == [5, 5, 5]
    # print(response.json()["inventory"])
    
def test_get_inventory_item():
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
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    response = pip._vendor.requests.delete(BASE)
    assert int(response.headers["X-Coins"]) == 3
    
def test_buy_items():
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    pip._vendor.requests.put(BASE, json = {"coin": 1})
    response = pip._vendor.requests.put(BASE + "inventory/1")
    
    assert int(response.json()["quantity"]) == 1


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