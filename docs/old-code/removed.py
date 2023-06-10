# Loops over user_order items list and gets values from each dictionary

for dict in user_order.items:
    for key, value in dict.items():
        print(f"{value.get('Quantity')} X {value.get('Coffee')} with {value.get('Milk')} milk: £{value.get('Price')}")