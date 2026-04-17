from database import add_sale
from datetime import datetime

print("=" * 50)
print("MANUAL SALE INSERTER")
print("=" * 50)
print("Enter sale details (or type 'quit' to exit)")
print()

sale_count = 0

while True:
    product = input("Product name (Laptop/Mouse/Keyboard/Monitor/Headphones): ")
    if product.lower() == 'quit':
        break
    
    price = float(input("Price ($): "))
    city = input("City (New York/Seattle/Austin/Chicago/Miami): ")
    
    add_sale(product, price, city)
    sale_count += 1
    
    print(f"✅ Sale #{sale_count} added: {product} - ${price} in {city}")
    print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    another = input("Add another sale? (y/n): ")
    if another.lower() != 'y':
        break

print(f"\n✅ Total sales added: {sale_count}")
print("Check your dashboard - it will update automatically!")