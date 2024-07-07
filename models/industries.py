"""This defines a list of business industry types."""
from . import Base
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid


class Industry(Base):
    """Defines the Type class which stores various business industry types"""
    __tablename__ = "industries"
    name = Column(String(128), nullable=False, primary_key=True)
    organizations = relationship("Organization", back_populates="industry")

    def __init__(self, name):
        """Initializes the class"""
        self.name = name    
