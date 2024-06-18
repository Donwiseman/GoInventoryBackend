"""Defines an Invitation class that defines adding users to an organization"""
from . import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class Invite(Base):
    """Creates an association object between Users and Organizations"""
    __tablename__ = "invites"
    org_id = Column(String(60), ForeignKey('organizations.id'),
                    primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'), primary_key=True)
    role = Column(String(32))
    organization = relationship('Organization',
                                back_populates='invites')
    user = relationship('User', back_populates='invites')
    created_at = Column(DateTime(timezone=True), default=datetime.now(datetime.UTC))
    status = Column(String(32), default="pending")
    is_active = Column(Boolean, default=True)

    def __init__(self, org_id, user_id, role):
        """Initializes an Invite object"""
        self.org_id = org_id
        self.user_id = user_id
        self.user_role = role
