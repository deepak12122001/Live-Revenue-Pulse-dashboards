from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()
engine = create_engine('sqlite:///sales.db', echo=False)
Session = sessionmaker(bind=engine)

class Sale(Base):
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    product = Column(String(50))
    price = Column(Float)
    city = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)

def add_sale(product, price, city):
    """Add a new sale to database"""
    session = Session()
    try:
        sale = Sale(product=product, price=price, city=city)
        session.add(sale)
        session.commit()
        return sale.id
    finally:
        session.close()

def get_recent_sales(hours=24):
    """Get sales from last X hours"""
    session = Session()
    try:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        sales = session.query(Sale).filter(Sale.timestamp >= cutoff).order_by(Sale.timestamp.desc()).all()
        return sales
    finally:
        session.close()

def get_sales_summary():
    """Get aggregated metrics"""
    sales = get_recent_sales(24)
    
    if not sales:
        return {
            'total_revenue': 0,
            'order_volume': 0,
            'avg_order_value': 0,
            'sales_by_city': {},
            'sales_by_product': {}
        }
    
    total_revenue = sum(s.price for s in sales)
    order_volume = len(sales)
    
    sales_by_city = {}
    sales_by_product = {}
    
    for sale in sales:
        sales_by_city[sale.city] = sales_by_city.get(sale.city, 0) + 1
        sales_by_product[sale.product] = sales_by_product.get(sale.product, 0) + 1
    
    return {
        'total_revenue': round(total_revenue, 2),
        'order_volume': order_volume,
        'avg_order_value': round(total_revenue / order_volume, 2) if order_volume > 0 else 0,
        'sales_by_city': sales_by_city,
        'sales_by_product': sales_by_product
    }