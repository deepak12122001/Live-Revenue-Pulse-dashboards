import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import json
import os
from database import get_recent_sales, get_sales_summary, add_sale

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
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0c10 0%, #14161c 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
    }
    
    /* KPI Cards */
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
    
    [data-testid="stMetricDelta"] {
        color: #00ffcc !important;
    }
    
    /* Alert box */
    .weather-alert {
        background: rgba(255, 51, 102, 0.15);
        border-left: 4px solid #ff3366;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ff3366;
        font-weight: bold;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Live badge */
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
    
    /* Status bar */
    .status-bar {
        background: rgba(0, 0, 0, 0.5);
        padding: 0.8rem;
        border-radius: 5px;
        margin-top: 1rem;
        font-size: 0.8rem;
        color: #888;
        text-align: center;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-family: 'Courier New', monospace !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Process queued sales
SALES_QUEUE_FILE = "sales_queue.json"

def process_sales_queue():
    """Read and add queued sales to database"""
    if os.path.exists(SALES_QUEUE_FILE):
        try:
            with open(SALES_QUEUE_FILE, 'r') as f:
                sales = json.load(f)
            
            if sales:
                for sale in sales:
                    add_sale(sale['product'], sale['price'], sale['city'])
                
                # Clear queue after processing
                with open(SALES_QUEUE_FILE, 'w') as f:
                    json.dump([], f)
                
                return len(sales)
        except Exception as e:
            pass
    return 0

# Process pending sales
new_sales = process_sales_queue()

# Header Section
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("<h1 style='color: #00ffcc; margin-bottom: 0;'>🔴 LIVE REVENUE PULSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-top: 0;'>War Room Command Center | Real-time Sales Monitoring</p>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='live-badge' style='float: right;'>● LIVE STREAMING</div>", unsafe_allow_html=True)
    if new_sales > 0:
        st.markdown(f"<p style='text-align: right; color: #00ffcc; font-size: 0.8rem;'>+{new_sales} new sales</p>", unsafe_allow_html=True)

st.markdown("---")

# Generate random weather alert (simulating real-time weather)
import random
weather_scenarios = [
    ("🌧️", "Heavy rain detected in Seattle", "Online sales increased by 20%", "positive"),
    ("🔥", "Heatwave warning in Austin", "Sales decreased by 20%", "negative"),
    ("❄️", "Cold front in Chicago", "Hot beverage sales up 15%", "positive"),
    ("🌪️", "Storm approaching Miami", "Emergency supply sales +30%", "positive"),
    ("☀️", "Heat advisory in Phoenix", "Indoor activity sales +10%", "positive"),
    ("🌨️", "Snow storm in Denver", "Delivery sales +25%", "positive")
]

weather_icon, weather_title, weather_effect, weather_type = random.choice(weather_scenarios)
st.markdown(f"""
<div class='weather-alert'>
    ⚠️ WEATHER IMPACT: {weather_icon} {weather_title} - {weather_effect}
</div>
""", unsafe_allow_html=True)

# Get data
summary = get_sales_summary()

# KPI Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 TOTAL REVENUE (24h)",
        value=f"${summary['total_revenue']:,.0f}",
        delta="+5%" if summary['total_revenue'] > 0 else None
    )

with col2:
    st.metric(
        label="📦 ORDER VOLUME",
        value=f"{summary['order_volume']:,}",
        delta=None
    )

with col3:
    st.metric(
        label="💵 AVG ORDER VALUE",
        value=f"${summary['avg_order_value']:,.2f}",
        delta=None
    )

with col4:
    st.metric(
        label="🌍 ACTIVE CITIES",
        value=len(summary['sales_by_city']),
        delta=None
    )

st.markdown("---")

# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='color: #00ffcc;'>📊 SALES BY CITY</h3>", unsafe_allow_html=True)
    if summary['sales_by_city']:
        city_df = pd.DataFrame({
            'City': list(summary['sales_by_city'].keys()),
            'Orders': list(summary['sales_by_city'].values())
        }).sort_values('Orders', ascending=False)
        
        fig = px.bar(
            city_df, 
            x='City', 
            y='Orders', 
            color='Orders',
            color_continuous_scale='Viridis',
            text='Orders'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            paper_bgcolor='rgba(30,31,46,0)',
            plot_bgcolor='rgba(30,31,46,0.3)',
            font_color='#e0e0e0',
            title_font_color='#00ffcc',
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💤 No sales yet. Run generator.py in another terminal")

with col2:
    st.markdown("<h3 style='color: #00ffcc;'>📈 TOP PRODUCTS</h3>", unsafe_allow_html=True)
    if summary['sales_by_product']:
        product_df = pd.DataFrame({
            'Product': list(summary['sales_by_product'].keys()),
            'Units Sold': list(summary['sales_by_product'].values())
        }).sort_values('Units Sold', ascending=True)
        
        fig = px.bar(
            product_df, 
            x='Units Sold', 
            y='Product', 
            orientation='h',
            color='Units Sold',
            color_continuous_scale='Plasma',
            text='Units Sold'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            paper_bgcolor='rgba(30,31,46,0)',
            plot_bgcolor='rgba(30,31,46,0.3)',
            font_color='#e0e0e0',
            title_font_color='#00ffcc',
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💤 No sales yet. Run generator.py in another terminal")

st.markdown("---")

# Recent Sales Table
st.markdown("<h3 style='color: #00ffcc;'>📋 RECENT TRANSACTIONS</h3>", unsafe_allow_html=True)

sales_data = get_recent_sales(24)
if sales_data:
    # Create DataFrame
    df = pd.DataFrame([{
        '🕐 Time': sale.timestamp.strftime('%H:%M:%S'),
        '📦 Product': sale.product,
        '💰 Price': f"${sale.price:,.0f}",
        '📍 City': sale.city
    } for sale in sales_data[:20]])
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            '🕐 Time': st.column_config.TextColumn('🕐 Time', width='small'),
            '📦 Product': st.column_config.TextColumn('📦 Product', width='medium'),
            '💰 Price': st.column_config.TextColumn('💰 Price', width='small'),
            '📍 City': st.column_config.TextColumn('📍 City', width='medium')
        }
    )
else:
    st.info("💤 Waiting for sales data... Run 'python generator.py' in another terminal")

# Status Bar
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='status-bar'>🔄 Auto-refreshing every 3 seconds</div>", unsafe_allow_html=True)

with col2:
    total_sales = len(sales_data) if sales_data else 0
    st.markdown(f"<div class='status-bar'>📊 Total sales (24h): {total_sales}</div>", unsafe_allow_html=True)

with col3:
    current_time = datetime.now().strftime('%H:%M:%S')
    st.markdown(f"<div class='status-bar'>⏱️ Last update: {current_time}</div>", unsafe_allow_html=True)

# Auto-refresh
time.sleep(3)
st.rerun()