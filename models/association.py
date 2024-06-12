"""This defines the Organization class and it's mappingss to the DB"""
from . import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class OrgUserAssociation(Base):
    """Creates an association object between Users and Organizations"""
    __tablename__ = "org_user_association"
    org_id = Column(String(60), ForeignKey('organizations.id'),
                    primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'), primary_key=True)
    user_role = Column(String(60))
    organization = relationship('Organization',
                                back_populates='user_associations')
    user = relationship('User', back_populates='org_associations')

    def __init__(self, org_id, user_id, role):
        """Initializes association object"""
        self.org_id = org_id
        self.user_id = user_id
        self.user_role = role
