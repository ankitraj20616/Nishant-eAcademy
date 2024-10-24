from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from database import get_db
from sqlalchemy.orm import Session
from schemas import UserSignUp, UserLogin, CourseSchema
from store import Users, OTPStore, Courses as CourseTable
from starlette import status
from utils import PasswordHashing
from random import randint
from config import setting
from twilio.rest import Client
from auth import JWTAuth
from datetime import timedelta
from typing import Annotated


router = APIRouter()
password_operations = PasswordHashing()
jwt_authentication = JWTAuth()

TWILIO_ACC_SID = setting.TWILIO_ACC_SID
TWILIO_AUTH_TOKEN = setting.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = setting.TWILIO_PHONE_NUMBER

twilio_client = Client(TWILIO_ACC_SID, TWILIO_AUTH_TOKEN)



@router.post("/jwt_token")
async def loginJWTToken(login_data: UserLogin, db: Session = Depends(get_db)):
    students = db.query(Users).all()
    for student in students:
        if student.phone_num == login_data.phone_num and password_operations.verifyPassword(student.password, login_data.password):
            expire_time = timedelta(minutes= setting.ASCESS_TOKEN_EXPIRE_MINUTES)
            jwt_token = jwt_authentication.generateAccessToken({"phone_num": student.phone_num, 
                                                                "role": student.role}, 
                                                                expire_time)
            return jwt_token
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                        detail= "Incorrect Phone number or Password")

@router.post("/routeProtected/{token}")
def routeProtected(jwt_token: str = Cookie(None)):
    payload: dict = jwt_authentication.verifyToken(jwt_token)
    if not payload or not payload.get("phone_num"):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid token!")
    return {"message": f"Hello, {payload.get('phone_num')}. You have accessed a protected route."}

@router.post("/login")
async def logIn(response: Response, login_data: UserLogin, db: Session = Depends(get_db)):
    login_data.phone_num = "+91" + login_data.phone_num
    token = await loginJWTToken(login_data= login_data, db= db)
    response.set_cookie(
        key="jwt_token",
        value= token,
        httponly= True
    )
    message = routeProtected(token)
    return {"access_token": token, "message": message}


@router.post("/signUp")
async def signUp(new_student: UserSignUp,db: Session = Depends(get_db)):
    new_student.phone_num = "+91" + new_student.phone_num
    is_already_registered = db.query(Users).filter(new_student.phone_num == Users.phone_num).first()
    if is_already_registered:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "This phone number has be registered!")
    elif new_student.password != new_student.confirm_password:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Password and confirm password not matching")
    
    new_student.password = password_operations.hashPassword(new_student.password)
    new_student.confirm_password = password_operations.hashPassword(new_student.confirm_password)
    new_student = Users(
        phone_num = new_student.phone_num,
        first_name =  new_student.first_name,
        last_name = new_student.last_name,
        password = new_student.password,
        confirm_password = new_student.confirm_password,
        state = new_student.state,
        role = new_student.role
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


@router.get("/fetch-courses-details")
async def fetchAllCourses(db: Session = Depends(get_db)):
    return db.query(CourseTable).all()



@router.post("/add-new-course", response_model=CourseSchema)
async def addNewCourse(course_details: CourseSchema, db: Session = Depends(get_db)
                       , jwt_token: str = Cookie(None)):
    
    if not jwt_token:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid token!")
    payload = jwt_authentication.verifyToken(jwt_token)
    if not payload or not payload.get("phone_num"):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Invalid token, payload error")
    role = payload.get("role")
    if role != "instructor" and role != "admin":
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Access denied, Only instructors/admin can add new courses.")
    try:
        new_course = CourseTable(
            name = course_details.name,
            cost = course_details.cost,
            validity = course_details.validity,
            description = course_details.description,
            features = course_details.features,
            content = course_details.content,
            content_language = course_details.content_language 
        )
        db.add(new_course)
        db.commit()
        return course_details
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"Error occured:- {e}")
    
@router.get("/course/{name}")
async def searchCourseByName(name: str, db: Session = Depends(get_db)):
    all_courses = await fetchAllCourses(db = db)
    if not all_courses:
        return {"message": "No courses available."}
    for course in all_courses:
        if course.name.lower() == name.lower():
            return course
    return {"message": f"{name} course not available."}

@router.get("/course/{id}")
async def searchCourseById(id: int, db: Session = Depends(get_db)):
    all_courses = await fetchAllCourses(db = db)
    if not all_courses:
        return {"message": "No courses available."}
    for course in all_courses:
        if course.id == id:
            return course
    return {"message": f"Course with {id} not available."}