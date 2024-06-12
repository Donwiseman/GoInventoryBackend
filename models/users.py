"""This defines the User classs and it's mappingss to the DB"""
from . import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, \
        Table, Boolean, LargeBinary
from sqlalchemy.orm import relationship
import uuid
from bcrypt import hashpw, gensalt, checkpw


class User(Base):
    """defines User class"""
    __tablename__ = 'users'
    id = Column(String(60), primary_key=True)
    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    email = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)
    hashed_password = Column(LargeBinary, nullable=False)
    mobile = Column(String(60))
    email_verified = Column(Boolean, default=False)
    mobile_verified = Column(Boolean, default=False)
    active_token = Column(String(128))
    token_expiry = Column(DateTime)
    image = Column(String(512))
    org_associations = relationship("OrgUserAssociation",
                                    back_populates="user", cascade='delete')
    org_created = relationship('Organization', back_populates='creator')

    def __init__(self, **kwargs):
        """Constructor for the class"""
        self.id = str(uuid.uuid4())
        self.last_name = kwargs.get("last_name", None)
        self.first_name = kwargs.get("first_name", None)
        self.email = kwargs.get("email", None)
        self.hashed_password = self.__hash_password(kwargs.get("password"))
        self.mobile = kwargs.get("mobile", None)
        self.image = kwargs.get("image", None)

    def __hash_password(cls, password: str) -> bytes:
        """Hashes a given password."""
        salt = gensalt()
        encoded_pw = password.encode('utf-8')
        return hashpw(encoded_pw, salt)

    def validate_password(self, password: str) -> bool:
        """Validates password"""
        pw_bytes = password.encode('utf-8')
        return checkpw(pw_bytes, self.hashed_password)

    def set_password(self, password: str):
        """Sets a new user password"""
        from database import storage
        self.hashed_password = self.__hash_password(password)
        storage.save()

    def full_name(self):
        """Returns full name of user"""
        return f"{self.first_name} {self.last_name}"
