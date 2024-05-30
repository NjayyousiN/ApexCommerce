from sqlalchemy.orm import Session
from db.models import Customer, Seller, Item, Order
from typing import Optional

# Create a new customer
def create_customer(session: Session, name: str, email: str, phoneNumber: str, address: str, password: str) -> Customer:
    new_customer = Customer(name=name, email=email, phoneNumber=phoneNumber, address=address, password=password)
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer

# Create a new seller
def create_seller(session: Session, name: str, email: str, phone_number: str, address: str) -> Seller:
    new_seller = Seller(name=name, email=email, phone_number=phone_number, address=address)
    session.add(new_seller)
    session.commit()
    session.refresh(new_seller)
    return new_seller

# Create a new item
def create_item(session: Session, rating: float, category: str, item_desc: str, stock: int, item_pic: str, reviews: str, seller_id: int) -> Item:
    new_item = Item(rating=rating, category=category, item_desc=item_desc, stock=stock, item_pic=item_pic, reviews=reviews, seller_id=seller_id)
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item

# Create a new order
def create_order(session: Session, order_number: str, status: str, delivery_date: str, items: str, customer_id: int) -> Order:
    new_order = Order(order_number=order_number, status=status, delivery_date=delivery_date, items=items, customer_id=customer_id)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

# Read all customers
def read_customers(session: Session) -> list[Customer]:
    return session.query(Customer).all()

# Read all sellers
def read_sellers(session: Session) -> list[Seller]:
    return session.query(Seller).all()

# Read all items
def read_items(session: Session) -> list[Item]:
    return session.query(Item).all()

# Read all orders
def read_orders(session: Session) -> list[Order]:
    return session.query(Order).all()

# Read a customer by ID
def read_customer_by_id(session: Session, id: int) -> Optional[Customer]:
    return session.query(Customer).filter(Customer.id == id).first()

# Read a seller by ID
def read_seller_by_id(session: Session, id: int) -> Optional[Seller]:
    return session.query(Seller).filter(Seller.id == id).first()

# Read a customer by email
def read_customer_by_email(session: Session, email: str) -> Optional[Customer]:
    return session.query(Customer).filter(Customer.email == email).first()

# Read a seller by email
def read_seller_by_email(session: Session, email: str) -> Optional[Seller]:
    return session.query(Seller).filter(Seller.email == email).first()

# Read an item by ID
def read_item_by_id(session: Session, item_id: int) -> Optional[Item]:
    return session.query(Item).filter(Item.id == item_id).first()

# Read an order by ID
def read_order_by_id(session: Session, order_id: int) -> Optional[Order]:
    return session.query(Order).filter(Order.id == order_id).first()

# Update a customer by ID
def update_customer_by_id(session: Session, id: int, name: Optional[str] = None, email: Optional[str] = None, phoneNumber: Optional[str] = None, address: Optional[str] = None) -> Optional[Customer]:
    customer = session.query(Customer).filter(Customer.id == id).first()
    if customer:
        if name: customer.name = name
        if email: customer.email = email
        if phoneNumber: customer.phoneNumber = phoneNumber
        if address: customer.address = address
        session.commit()
        session.refresh(customer)
    return customer

# Update a seller by ID
def update_seller_by_id(session: Session, id: int, name: Optional[str] = None, email: Optional[str] = None, phone_number: Optional[str] = None, address: Optional[str] = None) -> Optional[Seller]:
    seller = session.query(Seller).filter(Seller.id == id).first()
    if seller:
        if name: seller.name = name
        if email: seller.email = email
        if phone_number: seller.phone_number = phone_number
        if address: seller.address = address
        session.commit()
        session.refresh(seller)
    return seller

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

# Delete a customer by ID
def delete_customer_by_id(session: Session, id: int) -> Optional[Customer]:
    customer = session.query(Customer).filter(Customer.id == id).first()
    if customer:
        session.delete(customer)
        session.commit()
    return customer

# Delete a seller by ID
def delete_seller_by_id(session: Session, id: int) -> Optional[Seller]:
    seller = session.query(Seller).filter(Seller.id == id).first()
    if seller:
        session.delete(seller)
        session.commit()
    return seller

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
