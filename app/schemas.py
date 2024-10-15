from pydantic import BaseModel


class UserLogin(BaseModel):
    phone_num: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "phone_num": "Phone number of User",
                "password": "Password of user"
            }
        }

class UserSignUp(BaseModel):
    first_name: str
    last_name: str
    phone_num: str
    password: str
    confirm_password: str
    state: str

    class Config:
        json_schema_extra ={
            "example": {
                "first_name": "Your First Name",
                "last_name": "Your Last Name",
                "phone_num": "Your Phone Number",
                "password": "Password You Want To Set",
                "confirm_password": "Re Enter Same Password",
                "state": "Enter The State Name You Lived In"
            }
        }


