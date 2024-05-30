from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, Text, ARRAY
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime, timedelta

# Possible order status values
class OrderStatus(enum.Enum):
    cancelled = "cancelled"
    delivered = "delivered"
    confirmed = "confirmed"

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    phoneNumber = Column(String)
    address = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Seller(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    rating = Column(Integer)
    phoneNumber = Column(String, nullable=False)
    address = Column(String)
    items = relationship("Item", back_populates="seller")

class Item(Base):
    __tablename__ = 'items'
    itemId = Column(Integer, primary_key=True, unique=True, nullable=False)
    rating = Column(Integer)
    category = Column(String, nullable=False)
    itemDesc = Column(Text, nullable=False)
    stock = Column(Integer, nullable=False)
    itemPic = Column(String, nullable=False)
    reviews = Column(ARRAY(String))
    sellerId = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    seller = relationship("Seller", back_populates="items")

class Order(Base):
    __tablename__ = 'orders'
    orderId = Column(Integer, primary_key=True, unique=True, nullable=False)
    orderNumber = Column(String, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.confirmed)
    deliveryDate = Column(Date, default=datetime.now() + timedelta(days=7))
    items = Column(ARRAY(Integer), nullable=False)
    customerId = Column(Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship("Customer")
