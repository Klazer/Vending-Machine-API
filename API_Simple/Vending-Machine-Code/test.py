import pip._vendor.requests
import time

BASE = "http://127.0.0.1:5000/s"

data = {"coins": -2}
# headers = {"Content-Type": "application/json"}

response = pip._vendor.requests.get(BASE + "inventory")
print(response.json())
time.sleep(2.4)
response = pip._vendor.requests.put(BASE, json = data)
print(response.json())
time.sleep(2.5)
response = pip._vendor.requests.put(BASE + "inventory/2")
print(response.json())
response = pip._vendor.requests.delete(BASE)
print(response.json())