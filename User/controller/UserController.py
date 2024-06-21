from ..models import User
import json
from Auth.controller.AuthController import AuthController


class UserController:
    def __init__(self, email: str = '', username: str = '') -> None:
        self.user = None
        self.exists = False
        if email:
            self.initFromEmail(email)
        elif username:
            self.initFromUsername(username)

    @property
    def userExists(self) -> bool:
        return self.exists

    def initFromEmail(self, email: str) -> None:
        dbUserQuerySet = User.objects.filter(email=email)
        if dbUserQuerySet.exists():
            dbUser = dbUserQuerySet.first()
            self.exists = True
            self.user = dbUser

    def initFromUsername(self, username: str) -> None:
        dbUserQuerySet = User.objects.filter(username=username)
        if dbUserQuerySet.exists():
            dbUser = dbUserQuerySet.first()
            self.exists = True
            self.user = dbUser

    def deleteUser(self):
        self.user.delete()

    @staticmethod
    def toDict(user: User) -> dict:
        return {
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'profile_picture': user.profile_picture,
        }

    @staticmethod
    def serialize(user: User):
        dataDict = UserController.toDict(user)
        return json.dumps(dataDict)

    @staticmethod
    def fetchAllUsers():
        users = User.objects.all()
        userList = [UserController.toDict(user) for user in users]
        return json.dumps(userList)

    def updateUserField(self, field: str, value) -> bool:
        if field == 'username':
            self.user.username = value
        elif field == 'email':
            self.user.email = value
        elif field == 'password':
            self.user.password = AuthController.hashPassword(value)
        elif field == 'profile_picture':
            self.user.profile_picture = value
        else:
            return False

        # self.user.save()
        return True

    def updateUser(self, update: dict) -> bool:
        for key, value in update.items():
            res = self.updateUserField(key, value)
            if not res:
                return False

        self.user.save()
        return True
