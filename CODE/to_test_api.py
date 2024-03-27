import requests
ITEM_ID = 9
base_url = 'http://127.0.0.1:5000/api/grocery_items'

def print_response(response):
    print(response.status_code)
    print(response.json())


# #_____________Get all grocery items_____________#
# response = requests.get(base_url)
# print_response(response)

# #_____________Get a specific grocery item by ID_____________#
# response = requests.get(f'{base_url}/{ITEM_ID}')
# print_response(response)

# #_____________Create a new grocery item_____________#
# new_item_data = {
#     "name": "New NEWEST Item",
#     "price": 2.99,
#     "category": "Fruits",
#     "quantity": 10,
#     "key" : "admin"
# }
# response = requests.post(base_url, json=new_item_data)
# print_response(response)

# #_____________Update an existing grocery item_____________#
# item_id = ITEM_ID
# updated_item_data = {
#     "name": "Updated New Item",
#     "price": 4.99,
#     "category": "NEWEST Vegetables",
#     "quantity": 15,
#     "key" : "admin"
# }
# response = requests.put(f'{base_url}/{item_id}', json=updated_item_data)
# print_response(response)

#_____________Delete a grocery item_____________#
item_id = ITEM_ID
delete_item_data = {
    "key" : "admin"
}
response = requests.delete(f'{base_url}/{ITEM_ID}', json= delete_item_data)
print_response(response)



