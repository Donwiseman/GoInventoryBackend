"""This defines the items class which represent a product"""
from . import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, \
    Boolean
from sqlalchemy.orm import relationship
import uuid


class Item(Base):
    """Defines the Item class"""
    __tablename__ = "items"
    id = Column(String(60), primary_key=True)
    name = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    category_id = Column(String(128), ForeignKey("categories.id"))
    created_by = Column(String(128))
    image = Column(String(512))
    unit = Column(String(128))
    cost_price = Column(Float)
    sale_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    discount = Column(Float, default=0)
    alert_level = Column(Integer, default=0)
    organization_id = Column(String(128), ForeignKey("organizations.id"),
                             nullable=False)
    obsolete = Column(Boolean, default=False)
    organization = relationship("Organization", back_populates="items")
    category = relationship("Category", back_populates="items")
    purchase_history = relationship("Purchase", back_populates="item")
    sale_history = relationship("Sale", back_populates="item")

    def __init__(self, **kwargs):
        """Initializes the class """
        self.id = str(uuid.uuid4())
        self.name = kwargs.get("name", None)
        self.category_id = kwargs.get("category_id", None)
        self.created_by = kwargs.get("user_name", None)
        self.image = kwargs.get("image", None)
        self.unit = kwargs.get("unit", None)
        self.cost_price = kwargs.get("cost_price", None)
        self.sale_price = kwargs.get("sale_price", None)
        self.quantity = kwargs.get("quantity", None)
        self.alert_level = kwargs.get("alert_level", None)
        self.organization_id = kwargs.get("organization_id", None)

    def add(self, quantity: int, purchase_cost: float, time, description: str,
            user_name):
        """Adds more unit of an item and returns a purchase object"""
        from database import storage
        from .purchases import Purchase
        self.quantity += quantity
        self.updated_at = time
        trans = {
            "date": time,
            "user_name": user_name,
            "organization_id": self.organization_id,
            "item_id": self.id,
            "details": description,
            "quantity": quantity,
            "total_cost": purchase_cost,
            "new_item_total": self.quantity
        }
        new_purchase = Purchase(**trans)
        storage.add(new_purchase)
        storage.save()
        return new_purchase

    def remove(self, quantity: int, time, user_name: str,
               description: str = None, sale: float = None):
        """removes some unit of an item and returns a sale object"""
        from database import storage
        from .sales import Sale
        if self.quantity < quantity:
            raise ValueError(f"{self.name} quantity is too low for operation")
        self.quantity -= quantity
        if not sale:
            sale = self.sale_price * quantity
        trans = {
            "date": time,
            "user_name": user_name,
            "organization_id": self.organization_id,
            "item_id": self.id,
            "details": description,
            "quantity": quantity,
            "total_cost": sale,
            "new_item_total": self.quantity
        }
        self.updated_at = time
        new_sale = Sale(**trans)
        storage.add(new_sale)
        storage.save()
        return new_sale

    def recent_purchase(self) -> list:
        """Returns a list containing last 10 recent purchase transactions"""
        pur = []
        purchases = self.purchase_history
        purchases.sort(reverse=True, key=lambda p: p.date)
        for tr in purchases:
            pur.append(tr.transaction())
        return pur[:10]

    def recent_sale(self) -> list:
        """Returns a list containing last 10 recent purchase transactions"""
        sal = []
        sales = self.purchase_history
        sales.sort(reverse=True, key=lambda p: p.date)
        for tr in sales:
            sal.append(tr.transaction())
        return sal[:10]

    def to_dict(self):
        """Returns a dict representation of object"""
        date = self.organization.localize(self.updated_at)
        item_dict = {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "unit": self.unit,
            "cost_price": self.cost_price,
            "sale_price": self.sale_price,
            "image": self.image,
            "category_id": self.category_id,
            "last_updated": date,
            "recent_purchases": self.recent_purchase(),
            "recent_sales": self.recent_sale()
        }
        return item_dict
