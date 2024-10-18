from passlib.context import CryptContext
from fastapi import HTTPException
from starlette import status


class PasswordHashing:
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes= ["bcrypt"], deprecated= "auto")

    def hashPassword(self, password: str):
        return self.pwd_context.hash(password)
    
    def verifyPassword(self, hashedPassword: str, userPassword: str):
        try:
            return self.pwd_context.verify(userPassword, hashedPassword)
        except Exception as e:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= f"Password verification failed: {str(e)}")