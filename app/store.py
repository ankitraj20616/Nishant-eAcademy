from database import Base
from sqlalchemy import Column, Integer, String

class Students(Base):
    __tablename__ = "Students"
    phone_num = Column(String(15), primary_key= True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    password = Column(String(255))
    confirm_password = Column(String(255))
    state = Column(String(255))

class OTPStore(Base):
    __tablename__ = "otp_store"
    phone_num = Column(String(15), primary_key= True)
    otp = Column(String(6))