from database import add_sale
import random
import time

# Products and their price ranges
PRODUCTS = {
    "Laptop": (600, 1500),
    "Mouse": (15, 50),
    "Keyboard": (40, 120),
    "Monitor": (150, 400),
    "Headphones": (50, 200),
    "Webcam": (40, 150),
    "USB Drive": (10, 60)
}

CITIES = ["New York", "Seattle", "Austin", "Chicago", "Miami", "Denver", "Boston"]

print("=" * 50)
print("INSERTING 100 SALES...")
print("=" * 50)

for i in range(100):
    # Random product
    product = random.choice(list(PRODUCTS.keys()))
    # Random price within range
    min_price, max_price = PRODUCTS[product]
    price = random.randint(min_price, max_price)
    # Random city
    city = random.choice(CITIES)
    
    # Add to database
    add_sale(product, price, city)
    
    # Show progress every 10 sales
    if (i + 1) % 10 == 0:
        print(f"✅ {i+1} sales inserted...")
    
    # Small delay to avoid overwhelming
    time.sleep(0.1)

print("=" * 50)
print(f"✅ COMPLETE! 100 sales added!")
print("Check your dashboard - it will update automatically!")
print("=" * 50)