""" Handles ORM with SqlAlchemy for all classes. """
from models import Base
from models.users import User
from models.organizations import Organization
from models.association import OrgUserAssociation
from models.items import Item
from models.categories import Category
from models.purchases import Purchase
from models.sales import Sale
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


# db_uri = "sqlite:///a.db"
# db_uri = "postgresql+psycopg2://stan:Dinobi_11@localhost:5432/inventorydb"
db_uri = "postgresql+psycopg2://inventory:password@localhost:5432/inventorydb"

if os.getenv('DEBUG') == 'False':
    db_uri = (
            "postgresql+psycopg2://" +
            f"{os.getenv('DB_USER')}:" +
            f"{os.getenv('DB_PASSWD')}" +
            f"@{os.getenv('DB_HOST')}/" +
            f"{os.getenv('DB_NAME')}")


class Database:
    """Defines the SQL databse ORM"""

    def __init__(self) -> None:
        self.__engine = create_engine(db_uri, echo=False)
        Base.metadata.create_all(self.__engine)
        self.__session = None

    def start_session(self):
        """Creates a session to manage ORM operations"""
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=True)
        self.__session = scoped_session(session_factory)

    def end_session(self):
        """Ends the current session"""
        self.__session.remove()

    def add(self, obj: object):
        """Adds an object to the session"""
        self.__session.add(obj)

    def save(self):
        """Saves all saved transaction"""
        self.__session.commit()

    def delete(self, obj: object):
        """Deletes the obj from storage"""
        self.__session.delete(obj)

    def register_user(self, **kwargs) -> User:
        """Registers a user to the database."""
        new_user = User(**kwargs)
        self.__session.add(new_user)
        self.__session.commit()
        return new_user

    def get_category_by_id(self, category_id: str) -> Category:
        """"Retrieves the specified category object based on it's id"""
        category = self.__session.query(Category).filter(Category.id ==
                                                         category_id).first()
        if category:
            return category
        else:
            return None

    def get_user_by_id(self, user_id: str) -> User:
        """returns a user based on the id"""
        user = self.__session.query(User).filter(User.id == user_id).first()
        if user:
            return user
        else:
            return None

    def create_organization(self,  **kwargs) -> Organization:
        """Creates an organization by an admin user"""
        user = self.get_user_by_id(kwargs.get("user_id"))
        org = Organization(**kwargs)
        self.__session.add(org)
        asso = OrgUserAssociation(org.id, user.id, "Admin")
        self.__session.add(asso)
        self.__session.commit()
        return org

    def get_item_by_id(self, item_id: str) -> Item:
        """returns the item based on the id"""
        item = self.__session.query(Item).filter(Item.id == item_id).first()
        if item:
            return item
        else:
            return None

    def get_org_by_id(self, org_id: str) -> Organization:
        """returns an organization based on the id"""
        org = self.__session.query(Organization).filter(
            Organization.id == org_id).first()
        if org:
            return org
        else:
            return None

    def get_org_by_name(self, name: str) -> Organization:
        """returns an organization based on the name"""
        org = self.__session.query(Organization).filter(
            Organization.name == name).first()
        if org:
            return org
        else:
            return None

    def get_user_by_email(self, email: str) -> User:
        """returns a user based on the image"""
        user = self.__session.query(User).filter(User.email == email).first()
        if user:
            return user
        else:
            return None

    def get_user_by_mobile(self, mobile: str) -> User:
        """returns a user based on the mobile"""
        user = self.__session.query(User).filter(User.mobile == mobile).first()
        if user:
            return user
        else:
            return None
