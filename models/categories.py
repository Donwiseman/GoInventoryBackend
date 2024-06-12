"""This define the various item categories"""
from . import Base
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid


class Category(Base):
    """Defines the Category class which stores variou"""
    __tablename__ = "categories"
    id = Column(String(60), primary_key=True)
    name = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True))
    description = Column(String(128))
    organization_id = Column(String(128), ForeignKey("organizations.id"),
                             nullable=False)
    organization = relationship("Organization", back_populates="categories")
    items = relationship("Item", back_populates="category")

    def __init__(self, **kwargs):
        """Initializes the class"""
        self.id = str(uuid.uuid4())
        self.name = kwargs.get("name", None)
        self.description = kwargs.get("description", None)
        self.organization_id = kwargs.get("organization_id", None)
        self.created_at = kwargs.get("time")
