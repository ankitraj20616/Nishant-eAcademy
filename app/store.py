from database import Base
from sqlalchemy import Column, Integer, String

class Students(Base):
    __tablename__ = "Students"
    phone_num = Column(Integer, primary_key= True, index= True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    password = Column(String(255))
    state = Column(String(255))
