from sqlalchemy import Column, String, Integer
from db.base import get_base


Base= get_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)

