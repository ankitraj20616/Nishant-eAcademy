from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from schemas import UserSignUp, UserLogin
from store import Students, OTPStore
from starlette import status
from utils import PasswordHashing
from random import randint
from config import setting
from twilio.rest import Client


router = APIRouter()
password_operations = PasswordHashing()

TWILIO_ACC_SID = setting.TWILIO_ACC_SID
TWILIO_AUTH_TOKEN = setting.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = setting.TWILIO_PHONE_NUMBER

twilio_client = Client(TWILIO_ACC_SID, TWILIO_AUTH_TOKEN)


@router.post("/signUp")
async def signUp(new_student: UserSignUp,db: Session = Depends(get_db)):
    new_student.phone_num = "+91" + new_student.phone_num
    is_already_registered = db.query(Students).filter(new_student.phone_num == Students.phone_num).first()
    if is_already_registered:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "This phone number has be registered!")
    elif new_student.password != new_student.confirm_password:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Password and confirm password not matching")
    
    new_student.password = password_operations.hashPassword(new_student.password)
    new_student.confirm_password = password_operations.hashPassword(new_student.confirm_password)
    new_student = Students(
        phone_num = new_student.phone_num,
        first_name =  new_student.first_name,
        last_name = new_student.last_name,
        password = new_student.password,
        confirm_password = new_student.confirm_password,
        state = new_student.state
    )

    db.add(new_student)
    db.commit()
    return {
        "message": "Phone number registered sucessfully.",
    }

def sendOTP_via_twilio(user_phone_num: str, otp: str):
    try:
        message = twilio_client.messages.create(
            body = f"Your otp is {otp}. It will expire in 5 minutes.",
            to = user_phone_num,
            from_ = TWILIO_PHONE_NUMBER
        )
        return message.sid
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Unable to send otp check your phone number.")



@router.post("/send-otp/{phone_num}")
async def sendOTP(phone_num: str, db: Session= Depends(get_db)):
    phone_num = "+91" + phone_num
    try:
        is_otp_sent = db.query(OTPStore).filter(OTPStore.phone_num == phone_num).first()
        if is_otp_sent:
            db.delete(is_otp_sent)
            db.commit()
        current_opt = str(randint(100000, 999999))
        
        send_otp_status = sendOTP_via_twilio(phone_num, current_opt)

        if not send_otp_status:
            raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "Failed to send OTP! please try again later.")
        opt_entry = OTPStore(
            phone_num= phone_num,
            otp = current_opt
        )
        db.add(opt_entry)
        db.commit()
        return {

            "message": "OTP is send to your number."
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")
        
@router.post("/verify-otp")
async def verify_otp(phone_num: str, otp: str, db: Session = Depends(get_db)):
    phone_num = "+91" + phone_num
    verification_record = db.query(OTPStore).filter(OTPStore.phone_num == phone_num).first()
    if not verification_record:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Some issue occoured! try again.")
    if verification_record.otp != otp:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Invalid OTP!")
    db.delete(verification_record)
    db.commit()
    return True