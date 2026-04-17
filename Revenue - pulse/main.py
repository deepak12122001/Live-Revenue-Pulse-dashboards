import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time
import random

# Page configuration
st.set_page_config(
    page_title="Live Revenue Pulse | War Room",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for War Room look
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0c10 0%, #14161c 100%);
    }
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
    }
    [data-testid="stMetricValue"] {
        color: #00ffcc !important;
        font-size: 2.2rem !important;
        font-weight: bold !important;
        font-family: 'Courier New', monospace !important;
    }
    [data-testid="stMetricLabel"] {
        color: #888 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    .weather-alert {
        background: rgba(255, 51, 102, 0.15);
        border-left: 4px solid #ff3366;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ff3366;
        font-weight: bold;
    }
    .live-badge {
        background: #ff3366;
        color: white;
        padding: 0.3rem 1.2rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        animation: blink 1.5s infinite;
        text-align: center;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .status-bar {
        background: rgba(0, 0, 0, 0.5);
        padding: 0.8rem;
        border-radius: 5px;
        margin-top: 1rem;
        font-size: 0.8rem;
        color: #888;
        text-align: center;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── DATA CONFIG ───────────────────────────────────────────────
PRODUCTS = [
    "Premium Coffee", "Energy Drink", "Protein Bar", "Green Tea",
    "Sports Water", "Vitamin Pack", "Cold Brew", "Smoothie"
]
CITIES = ["New York", "Chicago", "Los Angeles", "Houston",
          "Seattle", "Miami", "Denver", "Austin"]
PRICES = {
    "Premium Coffee": 8.50, "Energy Drink": 4.99, "Protein Bar": 6.75,
    "Green Tea": 5.25, "Sports Water": 3.50, "Vitamin Pack": 12.99,
    "Cold Brew": 7.25, "Smoothie": 9.50
}

# ─── SESSION STATE: Persistent fake sales data ──────────────────
if "sales_data" not in st.session_state:
    # Generate 50 past sales on first load
    past_sales = []
    now = datetime.now()
    for i in range(50):
        product = random.choice(PRODUCTS)
        past_sales.append({
            "timestamp": now - timedelta(minutes=random.randint(1, 1440)),
            "product": product,
            "price": PRICES[product] * random.randint(1, 5),
            "city": random.choice(CITIES)
        })
    st.session_state.sales_data = past_sales
    st.session_state.last_update = now

# Add 1-3 new sales every refresh
new_count = random.randint(1, 3)
for _ in range(new_count):
    product = random.choice(PRODUCTS)
    st.session_state.sales_data.append({
        "timestamp": datetime.now(),
        "product": product,
        "price": PRICES[product] * random.randint(1, 5),
        "city": random.choice(CITIES)
    })

# Keep only last 24h of data
cutoff = datetime.now() - timedelta(hours=24)
st.session_state.sales_data = [
    s for s in st.session_state.sales_data if s["timestamp"] > cutoff
]

df_all = pd.DataFrame(st.session_state.sales_data)

# ─── HEADER ────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("<h1 style='color: #00ffcc; margin-bottom: 0;'>🔴 LIVE REVENUE PULSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-top: 0;'>War Room Command Center | Real-time Sales Monitoring</p>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='live-badge' style='float: right;'>● LIVE STREAMING</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: right; color: #00ffcc; font-size: 0.8rem;'>+{new_count} new sales</p>", unsafe_allow_html=True)

st.markdown("---")

# ─── WEATHER ALERT ─────────────────────────────────────────────
weather_scenarios = [
    ("🌧️", "Heavy rain in Seattle", "Online sales up 20%"),
    ("🔥", "Heatwave in Austin", "Cold drink sales up 35%"),
    ("❄️", "Cold front in Chicago", "Hot beverage sales up 15%"),
    ("🌪️", "Storm in Miami", "Emergency supply sales +30%"),
    ("☀️", "Heat advisory in Phoenix", "Indoor activity sales +10%"),
    ("🌨️", "Snow storm in Denver", "Delivery sales +25%")
]
icon, title, effect = random.choice(weather_scenarios)
st.markdown(f"""
<div class='weather-alert'>
    ⚠️ WEATHER IMPACT: {icon} {title} - {effect}
</div>
""", unsafe_allow_html=True)

# ─── KPI METRICS ───────────────────────────────────────────────
total_revenue = df_all["price"].sum()
order_volume = len(df_all)
avg_order = df_all["price"].mean() if order_volume > 0 else 0
active_cities = df_all["city"].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 TOTAL REVENUE (24h)", f"${total_revenue:,.0f}", "+5%")
with col2:
    st.metric("📦 ORDER VOLUME", f"{order_volume:,}")
with col3:
    st.metric("💵 AVG ORDER VALUE", f"${avg_order:,.2f}")
with col4:
    st.metric("🌍 ACTIVE CITIES", active_cities)

st.markdown("---")

# ─── CHARTS ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='color: #00ffcc;'>📊 SALES BY CITY</h3>", unsafe_allow_html=True)
    city_df = df_all.groupby("city").size().reset_index(name="Orders").sort_values("Orders", ascending=False)
    fig = px.bar(city_df, x="city", y="Orders", color="Orders",
                 color_continuous_scale="Viridis", text="Orders")
    fig.update_traces(textposition="outside")
    fig.update_layout(
        paper_bgcolor="rgba(30,31,46,0)", plot_bgcolor="rgba(30,31,46,0.3)",
        font_color="#e0e0e0", showlegend=False, height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<h3 style='color: #00ffcc;'>📈 TOP PRODUCTS</h3>", unsafe_allow_html=True)
    product_df = df_all.groupby("product").size().reset_index(name="Units Sold").sort_values("Units Sold", ascending=True)
    fig = px.bar(product_df, x="Units Sold", y="product", orientation="h",
                 color="Units Sold", color_continuous_scale="Plasma", text="Units Sold")
    fig.update_traces(textposition="outside")
    fig.update_layout(
        paper_bgcolor="rgba(30,31,46,0)", plot_bgcolor="rgba(30,31,46,0.3)",
        font_color="#e0e0e0", showlegend=False, height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ─── RECENT TRANSACTIONS ───────────────────────────────────────
st.markdown("<h3 style='color: #00ffcc;'>📋 RECENT TRANSACTIONS</h3>", unsafe_allow_html=True)

recent = df_all.sort_values("timestamp", ascending=False).head(20).copy()
recent["🕐 Time"] = recent["timestamp"].dt.strftime("%H:%M:%S")
recent["📦 Product"] = recent["product"]
recent["💰 Price"] = recent["price"].apply(lambda x: f"${x:,.2f}")
recent["📍 City"] = recent["city"]

st.dataframe(
    recent[["🕐 Time", "📦 Product", "💰 Price", "📍 City"]],
    use_container_width=True,
    hide_index=True
)

# ─── STATUS BAR ────────────────────────────────────────────────
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='status-bar'>🔄 Auto-refreshing every 3 seconds</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='status-bar'>📊 Total sales (24h): {order_volume}</div>", unsafe_allow_html=True)
with col3:
    current_time = datetime.now().strftime('%H:%M:%S')
    st.markdown(f"<div class='status-bar'>⏱️ Last update: {current_time}</div>", unsafe_allow_html=True)

# ─── AUTO REFRESH ──────────────────────────────────────────────
time.sleep(3)
st.rerun()
