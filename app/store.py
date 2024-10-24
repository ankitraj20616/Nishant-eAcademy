from database import Base
from sqlalchemy import Column, Integer, String, Text

class Users(Base):
    __tablename__ = "Users"
    phone_num = Column(String(15), primary_key= True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    password = Column(String(255))
    confirm_password = Column(String(255))
    state = Column(String(255))
    role = Column(String(255), default= "Student")

class OTPStore(Base):
    __tablename__ = "otp_store"
    phone_num = Column(String(15), primary_key= True)
    otp = Column(String(6))


class Courses(Base):
    __tablename__ = "courses_details"
    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String(255))
    cost = Column(Integer)
    validity = Column(String(255))
    description = Column(Text)
    features = Column(Text)
    content = Column(Text)
    content_language = Column(String(255))