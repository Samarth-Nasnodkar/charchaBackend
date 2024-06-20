from ..models import User
import json
from Auth.controller.AuthController import AuthController


class UserController:
    def __init__(self, email: str = '') -> None:
        self.user = None
        self.exists = False
        self.initUser(email)

    @property
    def userExists(self) -> bool:
        return self.exists

    def initUser(self, email: str) -> None:
        dbUserQuerySet = User.objects.filter(email=email)
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
        # print('userlist = ', userList)
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
