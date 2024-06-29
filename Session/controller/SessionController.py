from datetime import datetime, timedelta

from ..models import Session
import json
import pytz


class SessionController:
    def __init__(self, session_id):
        self.session_id = session_id

    def getUser(self):
        if self.session_id is None:
            return None

        dbSession = Session.objects.filter(self.session_id).first()
        if dbSession is None:
            return None

        dbUser = dbSession.user
        return dbUser

    def validateSession(self):
        if self.session_id is None:
            return None

        dbSession = Session.objects.filter(pk=self.session_id).first()
        if dbSession is None:
            return None

        utc = pytz.UTC
        if dbSession.created_at < utc.localize(datetime.now() - timedelta(days=3)):
            dbSession.delete()
            return None

        dbUser = dbSession.user
        dbSession.created_at = datetime.now()
        dbSession.save()
        return dbUser

    @staticmethod
    def newSession(user):
        dbSession = Session.objects.filter(user=user).first()
        if dbSession is None:
            dbSession = Session()
            dbSession.user = user
            dbSession.save()
            return dbSession

        dbSession.delete()
        newSession = Session()
        newSession.user = user
        newSession.save()
        return newSession

    @staticmethod
    def toDict(session):
        return {
            'session_id': str(session.session_id),
            'user': session.user.toDict(),
        }

    @staticmethod
    def serialize(session):
        return json.dumps(SessionController.toDict(session))
