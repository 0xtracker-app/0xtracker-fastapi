from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class UserRecords(Base):
    __tablename__ = "user_data"

    #id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    farm = Column(String)
    farm_network = Column(String)
    wallet = Column(String, primary_key=True)
    dollarvalue = Column(Integer)
    farmnetwork = Column(String)