import random
import time
from datetime import datetime
import json
import os

PRODUCTS = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "USB Drive"]
CITIES = ["New York", "Austin", "Seattle", "Chicago", "Miami", "Denver", "Boston"]

PRICE_RANGE = {
    "Laptop": (600, 1500),
    "Mouse": (15, 50),
    "Keyboard": (40, 120),
    "Monitor": (150, 400),
    "Headphones": (50, 200),
    "Webcam": (40, 150),
    "USB Drive": (10, 60)
}

SALES_QUEUE_FILE = "sales_queue.json"

def add_sale_to_queue(product, price, city):
    """Add sale to queue file for dashboard to read"""
    if os.path.exists(SALES_QUEUE_FILE):
        with open(SALES_QUEUE_FILE, 'r') as f:
            sales = json.load(f)
    else:
        sales = []
    
    sales.append({
        'product': product,
        'price': price,
        'city': city,
        'timestamp': datetime.now().isoformat()
    })
    
    with open(SALES_QUEUE_FILE, 'w') as f:
        json.dump(sales, f)

def get_weather_effect(city):
    """Get weather effect on sales"""
    import random
    # Simulate different weather conditions
    weather_types = ['Clear', 'Rain', 'Heatwave', 'Cold', 'Storm']
    weather = random.choice(weather_types)
    
    if weather == 'Rain':
        return 1.2, f"🌧️ RAIN ALERT: {city} - Sales +20%"
    elif weather == 'Heatwave':
        return 0.8, f"🔥 HEAT ALERT: {city} - Sales -20%"
    elif weather == 'Cold':
        return 1.15, f"❄️ COLD ALERT: {city} - Sales +15%"
    elif weather == 'Storm':
        return 1.3, f"⛈️ STORM ALERT: {city} - Sales +30%"
    return 1.0, None

print("=" * 60)
print("🔴 LIVE REVENUE PULSE - SALES GENERATOR")
print("=" * 60)
print("Generating fake sales every 30 seconds...")
print("Weather effects will impact prices")
print("Press Ctrl+C to stop\n")

sale_count = 0
weather_alerts = []

try:
    while True:
        product = random.choice(PRODUCTS)
        base_price = random.randint(*PRICE_RANGE[product])
        city = random.choice(CITIES)
        
        # Get weather effect
        weather_effect, alert = get_weather_effect(city)
        adjusted_price = int(base_price * weather_effect)
        
        # Add to queue
        add_sale_to_queue(product, adjusted_price, city)
        sale_count += 1
        
        # Display alert if weather is affecting sales
        if alert:
            print(f"\n⚠️ {alert}")
            weather_alerts.append(alert)
            if len(weather_alerts) > 5:
                weather_alerts.pop(0)
        
        # Display sale info
        effect_symbol = "📈" if weather_effect > 1 else "📉" if weather_effect < 1 else "➡️"
        weather_icon = "☀️" if weather_effect == 1.0 else "🌧️" if weather_effect > 1 else "🔥"
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {weather_icon} Sale #{sale_count}: {product:12} ${adjusted_price:6,} in {city:12} {effect_symbol}")
        
        time.sleep(30)  # One sale every 30 seconds
        
except KeyboardInterrupt:
    print(f"\n\n✅ Generator stopped. Total sales generated: {sale_count}")
    print("\nRecent weather alerts:")
    for alert in weather_alerts[-5:]:
        print(f"  • {alert}")
    print("\nYou can close this window or restart with: python generator.py")