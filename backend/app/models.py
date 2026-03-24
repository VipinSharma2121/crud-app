from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    address = Column(String)
    email = Column(String)
    password = Column(String)
    image = Column(LargeBinary)