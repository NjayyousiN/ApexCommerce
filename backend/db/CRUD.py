import json
from sqlalchemy.orm import Session
from db.models import User, Item, Order, user_item_association
from typing import Optional


# Create a new user
def create_user(
    session: Session,
    name: str,
    email: str,
    phoneNumber: str,
    address: str,
    password: str,
) -> User:
    new_user = User(
        name=name,
        email=email,
        phoneNumber=phoneNumber,
        address=address,
        password=password,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


# Create a new item
def create_item(
    session: Session,
    item_name: str,
    category: str,
    itemDesc: str,
    stock: int,
    itemPic: str,
    reviews: Optional[str] = None,
    rating: Optional[float] = None,
) -> Item:
    new_item = Item(
        item_name=item_name,
        rating=rating,
        category=category,
        itemDesc=itemDesc,
        stock=stock,
        itemPic=itemPic,
        reviews=reviews,
    )
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item


# Create a new order
def create_order(session: Session, userId: int, items: list) -> Order:
    for item in items:
        # Check if every item exists in the items table
        if not session.query(Item).filter(Item.itemId == item["itemId"]).first():
            return None
    # Convert the items list to a JSON string
    items_to_json = json.dumps(items)
    new_order = Order(items=items_to_json, userId=userId)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order


# Add an item to a user
def add_item_to_user(session: Session, id: int, itemId: int) -> Optional[User]:
    user = session.query(User).filter(User.id == id).first()
    item = session.query(Item).filter(Item.itemId == itemId).first()
    if (user and item) and (item not in user.items):
        user.items.append(item)
        session.commit()
        session.refresh(user)
        return user
    else:
        return None


# Add an item to an order
def add_item_to_order(session: Session, orderId: int, itemId: int) -> Optional[Order]:
    order = session.query(Order).filter(Order.orderId == orderId).first()
    chosenItem = session.query(Item).filter(Item.itemId == itemId).first()
    items_as_dict = json.loads(order.items)
    # Check if the order and item exist
    if not (order and chosenItem):
        return None

    for item in items_as_dict:
        if item["itemId"] == itemId:
            # Item already exists in the order
            return None

    items_as_dict.append(
        {
            "itemId": chosenItem.itemId,
            "item_name": chosenItem.item_name,
            "rating": chosenItem.rating,
            "category": chosenItem.category,
            "itemDesc": chosenItem.itemDesc,
            "stock": chosenItem.stock,
            "itemPic": chosenItem.itemPic,
            "reviews": chosenItem.reviews,
        }
    )
    order.items = json.dumps(items_as_dict)
    session.commit()
    session.refresh(order)
    return order


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
def read_item_by_id(session: Session, itemId: int) -> Optional[Item]:
    return session.query(Item).filter(Item.itemId == itemId).first()


# Read all items by userId
def read_item_by_userId(session: Session, userId: int) -> list[Item]:
    user = session.query(User).filter(User.id == userId).first()

    if user:
        # Join the User and Item models using the user_item_association table
        items = (
            session.query(Item)
            .join(user_item_association, Item.itemId == user_item_association.c.item_id)
            .filter(user_item_association.c.user_id == userId)
            .all()
        )
        return items
    else:
        return []


# Read items by category
def read_item_by_category(session: Session, category: str) -> list[Item]:
    return session.query(Item).filter(Item.category == category).all()


# Read an order by ID
def read_order_by_id(session: Session, orderId: int) -> Optional[Order]:
    return session.query(Order).filter(Order.orderId == orderId).first()


# Read an order by userId
def read_order_by_userId(session: Session, userId: int) -> Optional[Order]:
    return session.query(Order).filter(Order.userId == userId).first()


# Update a user by ID
def update_user_by_id(
    session: Session,
    id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phoneNumber: Optional[str] = None,
    address: Optional[str] = None,
) -> Optional[User]:
    user = session.query(User).filter(User.id == id).first()
    if user:
        if name:
            user.name = name
        if email:
            user.email = email
        if phoneNumber:
            user.phoneNumber = phoneNumber
        if address:
            user.address = address
        session.commit()
        session.refresh(user)
    return user


# Update an item by ID
def update_item_by_id(
    session: Session,
    item_name: str,
    itemId: int,
    rating: Optional[float] = None,
    category: Optional[str] = None,
    itemDesc: Optional[str] = None,
    stock: Optional[int] = None,
    itemPic: Optional[str] = None,
    reviews: Optional[str] = None,
) -> Optional[Item]:
    item = session.query(Item).filter(Item.itemId == itemId).first()
    if item:
        if item_name:
            item.item_name = item_name
        if rating:
            item.rating = rating
        if category:
            item.category = category
        if itemDesc:
            item.itemDesc = itemDesc
        if stock:
            item.stock = stock
        if itemPic:
            item.itemPic = itemPic
        if reviews:
            item.reviews = reviews
        session.commit()
        session.refresh(item)
    return item


# Delete a user by ID
def delete_user_by_id(session: Session, id: int) -> Optional[User]:
    user = session.query(User).filter(User.id == id).first()
    if user:
        session.delete(user)
        session.commit()
    return user


# Delete an item by ID
def delete_item_by_id(session: Session, itemId: int) -> Optional[Item]:
    item = session.query(Item).filter(Item.itemId == itemId).first()
    if item:
        session.delete(item)
        session.commit()
    return item


# Delete an order by ID
def delete_order_by_id(session: Session, orderId: int) -> Optional[Order]:
    order = session.query(Order).filter(Order.orderId == orderId).first()
    if order:
        session.delete(order)
        session.commit()
    return order
