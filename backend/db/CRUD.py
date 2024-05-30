from sqlalchemy.orm import Session
from db.models import User, Item, Order
from typing import Optional

# Create a new user
def create_user(session: Session, name: str, email: str, phoneNumber: str, address: str, password: str) -> User:
    new_user = User(name=name, email=email, phoneNumber=phoneNumber, address=address, password=password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# Create a new item
def create_item(session: Session, rating: float, category: str, item_desc: str, stock: int, item_pic: str, reviews: str, seller_id: int) -> Item:
    new_item = Item(rating=rating, category=category, item_desc=item_desc, stock=stock, item_pic=item_pic, reviews=reviews, seller_id=seller_id)
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item

# Create a new order
def create_order(session: Session, order_number: str, status: str, delivery_date: str, items: str, user_id: int) -> Order:
    new_order = Order(order_number=order_number, status=status, delivery_date=delivery_date, items=items, user_id=user_id)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

# Read all users
def read_users(session: Session) -> list[User]:
    return session.query(User).all()

# Read all items
def read_items(session: Session) -> list[Item]:
    return session.query(Item).all()

# Read all orders
def read_orders(session: Session) -> list[Order]:
    return session.query(Order).all()

# Read a user by ID
def read_user_by_id(session: Session, id: int) -> Optional[User]:
    return session.query(User).filter(User.id == id).first()

# Read a user by email
def read_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.query(User).filter(User.email == email).first()

# Read an item by ID
def read_item_by_id(session: Session, item_id: int) -> Optional[Item]:
    return session.query(Item).filter(Item.id == item_id).first()

# Read an order by ID
def read_order_by_id(session: Session, order_id: int) -> Optional[Order]:
    return session.query(Order).filter(Order.id == order_id).first()

# Update a user by ID
def update_user_by_id(session: Session, id: int, name: Optional[str] = None, email: Optional[str] = None, phoneNumber: Optional[str] = None, address: Optional[str] = None) -> Optional[User]:
    user = session.query(User).filter(User.id == id).first()
    if user:
        if name: user.name = name
        if email: user.email = email
        if phoneNumber: user.phoneNumber = phoneNumber
        if address: user.address = address
        session.commit()
        session.refresh(user)
    return user

# Update an item by ID
def update_item_by_id(session: Session, item_id: int, rating: Optional[float] = None, category: Optional[str] = None, item_desc: Optional[str] = None, stock: Optional[int] = None, item_pic: Optional[str] = None, reviews: Optional[str] = None) -> Optional[Item]:
    item = session.query(Item).filter(Item.id == item_id).first()
    if item:
        if rating: item.rating = rating
        if category: item.category = category
        if item_desc: item.item_desc = item_desc
        if stock: item.stock = stock
        if item_pic: item.item_pic = item_pic
        if reviews: item.reviews = reviews
        session.commit()
        session.refresh(item)
    return item

# Update an order by ID
def update_order_by_id(session: Session, order_id: int, order_number: Optional[str] = None, status: Optional[str] = None, delivery_date: Optional[str] = None, items: Optional[str] = None) -> Optional[Order]:
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        if order_number: order.order_number = order_number
        if status: order.status = status
        if delivery_date: order.delivery_date = delivery_date
        if items: order.items = items
        session.commit()
        session.refresh(order)
    return order

# Delete a user by ID
def delete_user_by_id(session: Session, id: int) -> Optional[User]:
    user = session.query(User).filter(User.id == id).first()
    if user:
        session.delete(user)
        session.commit()
    return user

# Delete an item by ID
def delete_item_by_id(session: Session, item_id: int) -> Optional[Item]:
    item = session.query(Item).filter(Item.id == item_id).first()
    if item:
        session.delete(item)
        session.commit()
    return item

# Delete an order by ID
def delete_order_by_id(session: Session, order_id: int) -> Optional[Order]:
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        session.delete(order)
        session.commit()
    return order