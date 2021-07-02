import peewee

from app import settings


mysql_db = peewee.MySQLDatabase(
    settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASS, host=settings.DB_HOST, port=settings.DB_PORT
)


class BaseModel(peewee.Model):
    class Meta:
        database = mysql_db


class User(BaseModel):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    email = peewee.CharField(unique=True)
    phone_number = peewee.CharField(unique=True)
    notify_by_sms = peewee.BooleanField()
    notify_by_email = peewee.BooleanField()


class RetailerInfo(BaseModel):
    name = peewee.CharField()
    username = peewee.CharField()
    password = peewee.CharField()
    user = peewee.ForeignKeyField(User, backref="retailer_info")


class ConsolePreference(BaseModel):
    username = peewee.CharField()
    password = peewee.CharField()
    email = peewee.CharField()
    phone_number = peewee.CharField()
    notify_by_sms = peewee.BooleanField()
    notify_by_email = peewee.BooleanField()
    retailer_info = peewee.ForeignKeyField(RetailerInfo, backref="console_preferences")
