"""This defines the purchase transaction class"""
from . import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
import uuid


class Purchase(Base):
    """Records all item purchases or returns processed
       by the organization. """
    __tablename__ = "purchases"
    id = Column(String(60), primary_key=True)
    date = Column(DateTime(timezone=True), nullable=False)
    organization_id = Column(String(128), ForeignKey("organizations.id"),
                             nullable=False)
    done_by = Column(String(128), nullable=False)
    item_id = Column(String(128), ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_cost = Column(Float, nullable=False)
    total_items_in_store = Column(Integer)
    details = Column(String(256))
    organization = relationship("Organization", back_populates="purchases")
    item = relationship("Item", back_populates="purchase_history")

    def __init__(self, **kwargs):
        """Initializes the class"""
        self.id = str(uuid.uuid4())
        self.date = kwargs.get("date")
        self.organization_id = kwargs.get("organization_id")
        self.done_by = kwargs.get("user_name")
        self.item_id = kwargs.get("item_id")
        self.quantity = kwargs.get("quantity")
        self.purchase_cost = kwargs.get("total_cost")
        self.total_items_in_store = kwargs.get("new_item_total")
        self.details = kwargs.get("details")

    def transaction(self) -> dict:
        """returns a dict representation of the transaction"""
        date = self.organization.localize(self.date)
        tr = {
            "product_name": self.item.name,
            "Product_id": self.item_id,
            "transaction_id": self.id,
            "transaction_time": date,
            "transaction_type": "Purchase",
            "quantity": self.quantity,
            "total_cost": self.purchase_cost,
            "products_in_store": self.total_items_in_store,
            "transaction_done_by": self.done_by
        }
        return tr
