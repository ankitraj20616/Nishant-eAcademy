from passlib.context import CryptContext


class PasswordHashing:
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes= ["bcrypt"], deprecated= "auto")

    def hashPassword(self, password: str):
        return self.pwd_context.hash(password)