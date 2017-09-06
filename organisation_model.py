from peewee import *
import datetime
from config import *

database = MySQLDatabase(MYSQL_DATABASE, user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, charset='utf8')

class TblOrganisation(Model):
    id = PrimaryKeyField()
    identifier = CharField(unique=True)
    type = IntegerField()
    country = CharField()
    is_org_file = BooleanField(default = False)
    is_publisher = BooleanField(default = False)
    last_updated = DateTimeField(default = datetime.datetime.now().strftime('%Y-%m-%d'))
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
    knownheader = ["name", "identifier", "type", "country", "is_org_file", "is_publisher"]
    languages = []
    for key in row.keys():
        key = key.strip()
        if not key in knownheader and not key in languages:
            languages.append(key)
    return languages
