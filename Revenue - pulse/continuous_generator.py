from database import add_sale
import random
import time

PRODUCTS = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"]
PRICE_RANGE = {
    "Laptop": (600, 1500),
    "Mouse": (15, 50),
    "Keyboard": (40, 120),
    "Monitor": (150, 400),
    "Headphones": (50, 200)
}
CITIES = ["New York", "Seattle", "Austin", "Chicago", "Miami"]

print("Continuous Generator - Adding 100 sales with 2 second intervals")
print("Press Ctrl+C to stop early\n")

for i in range(100):
    product = random.choice(PRODUCTS)
    min_price, max_price = PRICE_RANGE[product]
    price = random.randint(min_price, max_price)
    city = random.choice(CITIES)
    
    add_sale(product, price, city)
    
    print(f"[{i+1}/100] Added: {product} - ${price} in {city}")
    time.sleep(2)  # Wait 2 seconds between sales

print("\n✅ Completed 100 sales!")