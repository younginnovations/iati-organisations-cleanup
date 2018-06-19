import logging
import csv
from organisation_model import *


#TODO: check if the database exists or not
database.connect()
if TblName.table_exists():
    database.drop_tables([TblName,TblOrganisation])
database.create_tables([TblName, TblOrganisation])

OUT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/out/"

filepath = OUT_DIR + "registry_publishers.csv"

#TODO: error handling

with open(filepath, "rb") as fp:
    reader = csv.DictReader(fp)
    languages = []
    org_count = 0
    for row in reader:
        #get the list of languages from the row dict
        if len(languages) == 0:
            languages = getLanguages(row)
        org_count += 1
        organisation = TblOrganisation.create(
            identifier = row["identifier"],
            type = row["type"] if row["type"] else 0,
            country = row["countrycode"],
            is_org_file = row["is_org_file"] if "is_org_file" in row else 0,
            is_publisher = 1 if "is_publisher" in row and row["is_publisher"] else 1,
            last_updated = row["last_updated"] if "last_updated" in row and row["last_updated"] else None
        )
        print org_count, row["identifier"]
        enName = row["name"]
        TblName.create(
            organisation = organisation,
            name = enName,
            language = "en"
        )
