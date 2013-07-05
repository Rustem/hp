from mongolite import Document, Connection
import datetime
from django.conf import settings

STATUSES = (PENDING, IN_PROGRESS, DONE) = range(3)


@settings.MONGO_CONNECTION.register
class BallTaskDocument(Document):
    __database__ = settings.MONGO_DB

    skeleton = {
        "title": unicode,
        "body": unicode,
        "create_date": datetime.datetime,
        "due_date": datetime.datetime,
        "status": int,
        "init_rad": int,
        "deadline_rad": int,
        "lazy_periods": list,
        "hp_periods": list,
    }

    default_values = {
        'create_date': datetime.datetime.utcnow,
        'status': PENDING
    }

    @property
    def left_days(self):
        pass


collection = settings.MONGO_DB["ball"]
BallTask = collection.BallTaskDocument
