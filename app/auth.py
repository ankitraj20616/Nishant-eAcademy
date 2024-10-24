import jwt
from fastapi import HTTPException
from starlette import status
from config import setting
from datetime import datetime, timedelta, timezone

class JWTAuth:
    def __init__(self):
        self.secret_key = setting.SECRET_KEY
        self.jwt_algoritm = setting.ALGORITHM
        self.token_expire_minutes = setting.ASCESS_TOKEN_EXPIRE_MINUTES

    def generateAccessToken(self, data: dict, expires_time: timedelta | None = None):
        data_to_encode = data.copy()
        if expires_time:
            expires_time = datetime.now(timezone.utc) + expires_time
        else:
            expires_time = datetime.now(timezone.utc) + timedelta(minutes= self.token_expire_minutes)
        
        data_to_encode.update({"exp": expires_time})
        encoded_jwt = jwt.encode(data_to_encode, self.secret_key, algorithm= self.jwt_algoritm)
        return encoded_jwt
    
    def verifyToken(self, token: str):
        try:
            payload: dict = jwt.decode(token, self.secret_key, algorithms= [self.jwt_algoritm])
            phone_num: str = payload.get("phone_num")
            if phone_num is None:
                raise HTTPException(status_code= status.HTTP_502_BAD_GATEWAY, detail= "JWT Token Error.")
            return payload
        except:
            return None
