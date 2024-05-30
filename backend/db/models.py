from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Enum, Text, ARRAY
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime, timedelta

# Possible order status values
class OrderStatus(enum.Enum):
    cancelled = "cancelled"
    delivered = "delivered"
    confirmed = "confirmed"

Base = declarative_base()

user_item_association = Table(
    'user_item_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('item_id', Integer, ForeignKey('items.itemId'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    phoneNumber = Column(String)
    address = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    rating = Column(Integer)
    items = relationship("Item", secondary=user_item_association, back_populates="users")

class Item(Base):
    __tablename__ = 'items'
    itemId = Column(Integer, primary_key=True, unique=True, nullable=False)
    item_name = Column(String, nullable=False)
    rating = Column(Integer)
    category = Column(String, nullable=False)
    itemDesc = Column(Text, nullable=False)
    stock = Column(Integer, nullable=False)
    itemPic = Column(String, nullable=False)
    reviews = Column(ARRAY(String))
    users = relationship("User", secondary=user_item_association, back_populates="items")

class Order(Base):
    __tablename__ = 'orders'
    orderId = Column(Integer, primary_key=True, unique=True, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.confirmed)
    deliveryDate = Column(Date, default=datetime.now() + timedelta(days=7))
    items = Column(ARRAY(Integer), nullable=False)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)
