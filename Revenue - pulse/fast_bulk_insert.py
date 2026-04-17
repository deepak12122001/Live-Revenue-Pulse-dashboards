from database import add_sale
import random

PRODUCTS = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "USB Drive"]
PRICES = [50, 80, 120, 350, 500, 750, 1000, 1200, 1500]
CITIES = ["New York", "Seattle", "Austin", "Chicago", "Miami", "Denver", "Boston"]

print("Inserting 100 sales instantly...")

for i in range(100):
    product = random.choice(PRODUCTS)
    price = random.choice(PRICES)
    city = random.choice(CITIES)
    add_sale(product, price, city)

print(f"✅ Added 100 sales!")
print(f"Total revenue should be around ${random.randint(50000, 100000)}")