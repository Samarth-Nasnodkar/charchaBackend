from django.db.models import QuerySet

from User.models import User
import hashlib
from typing import Optional

from Session.controller.SessionController import SessionController


class AuthController:
    """
    Handles authentication related operations.
    These operations include login, register, checking user existence.
    Also handles operations like hashing password
    """
    @staticmethod
    def hashPassword(password: str) -> str:
        """
        Returns the SHA256 hash of the given password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def userExists(email: str) -> bool:
        """
        Checks if the given user exists.
        """
        return User.objects.filter(email=email).exists()

    @staticmethod
    def loginWithEmail(email: str, password: str) -> Optional[User]:
        """
        Logs the given user in.
        Returns the user if login was successful.
        Returns None otherwise
        """
        try:
            # Fetching user from Database
            dbUser = User.objects.get(email=email)
        except User.DoesNotExist:
            # Returning None as user doesn't exist
            return None

        # Hashing the password
        hashedPassword = AuthController.hashPassword(password)
        if dbUser.password == hashedPassword:
            # Log-in successful
            return dbUser
        # log-in unsuccessful
        return None

    @staticmethod
    def loginWithUsername(username: str, password: str) -> Optional[User]:
        """
        Logs the given user in.
        Returns the user if login was successful.
        Returns None otherwise
        """
        try:
            # Fetching user from Database
            dbUser = User.objects.get(username=username)
        except User.DoesNotExist:
            # Returning None as user doesn't exist
            return None

        # Hashing the password
        hashedPassword = AuthController.hashPassword(password)
        if dbUser.password == hashedPassword:
            # Log-in successful
            return dbUser
        # log-in unsuccessful
        return None

    @staticmethod
    def register(
            username: str,
            email: str,
            password: str,
            profile_picture_url: str
    ) -> Optional[User]:
        """
        Registers the given user.
        Returns the user if registration was successful.
        Returns None otherwise
        """
        if AuthController.userExists(email):
            # User already exists with the email in the Database
            return None

        newUser = User(
            username=username,
            email=email,
            password=AuthController.hashPassword(password),
            profile_picture=profile_picture_url
        )

        # Saving the new user in the Database
        newUser.save()
        # Returning the new user
        return newUser
