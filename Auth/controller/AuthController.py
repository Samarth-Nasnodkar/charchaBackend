from User.models import User
import hashlib
from typing import Optional


class AuthController:
    @staticmethod
    def hashPassword(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def userExists(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def login(email: str, password: str) -> Optional[User]:
        dbUser = User.objects.get(email=email)
        hashedPassword = AuthController.hashPassword(password)
        if dbUser.password == hashedPassword:
            return dbUser
        return None

    @staticmethod
    def register(
            username: str,
            email: str,
            password: str,
            profile_picture_url: str
    ) -> Optional[User]:
        if AuthController.userExists(email):
            return None

        newUser = User(
            username=username,
            email=email,
            password=AuthController.hashPassword(password),
            profile_picture=profile_picture_url
        )
        newUser.save()
        return newUser
