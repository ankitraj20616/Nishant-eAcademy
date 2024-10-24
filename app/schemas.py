from pydantic import BaseModel


class UserLogin(BaseModel):
    phone_num: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "phone_num": "Phone number of User",
                "password": "Password of user",
            }
        }

class UserSignUp(BaseModel):
    first_name: str
    last_name: str
    phone_num: str
    password: str
    confirm_password: str
    state: str
    role: str

    class Config:
        json_schema_extra ={
            "example": {
                "first_name": "Your First Name",
                "last_name": "Your Last Name",
                "phone_num": "Your Phone Number",
                "password": "Password You Want To Set",
                "confirm_password": "Re Enter Same Password",
                "state": "Enter The State Name You Lived In",
                "role": "Student/Instructor/Admin"
            }
        }


class CourseSchema(BaseModel):
    name: str
    cost: int
    validity: str
    description: str
    features: str
    content: str
    content_language: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Name of course",
                "cost": "Cost of course",
                "validity": "Course validity time duration.",
                "description": "Description of course",
                "features": "Features course contain",
                "content": "Overview of course content",
                "content_language": "Course content language"
            }
        }
    }

