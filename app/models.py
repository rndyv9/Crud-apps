from sqlalchemy import Column, String
from .database import Base

class Contact(Base):
    __tablename__ = "contacts"

    name = Column(String, primary_key=True, index=True)
    phone_number = Column(String)
