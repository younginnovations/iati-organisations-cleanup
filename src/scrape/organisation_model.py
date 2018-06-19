from peewee import *
import datetime
from config import *

database = PostgresqlDatabase(POSTGRES_DATABASE, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST)

class TblOrganisation(Model):
    id = PrimaryKeyField()
    identifier = CharField(unique=True)
    type = IntegerField()
    country = CharField()
    is_org_file = BooleanField(default=False)
    is_publisher = BooleanField(default=False)
    last_updated = DateTimeField(null=True, default=datetime.datetime.now().strftime('%Y-%m-%d'))
    class Meta:
        db_table = "organisations"
        database = database

class TblName(Model):
    organisation = ForeignKeyField(TblOrganisation, to_field="id", related_name='names')
    name = TextField()
    language = CharField()
    class Meta:
        db_table = "names"
        database = database

def getLanguages(row):
    knownheader = ["name", "identifier", "type", "country", "countrycode", "is_org_file", "is_publisher", "last_updated"]
    languages = []
    for key in row.keys():
        key = key.strip()
        if not key in knownheader and not key in languages:
            languages.append(key)
    return languages
