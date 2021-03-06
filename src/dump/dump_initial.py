import logging
import csv
from organisation_model import *


#TODO: check if the database exists or not
database.connect()
if TblName.table_exists():
    database.drop_table(TblName)
if TblOrganisation.table_exists():
    database.drop_table(TblOrganisation)

if not TblOrganisation.table_exists():
    database.create_table(TblOrganisation)
if not TblName.table_exists():
    database.create_table(TblName)

filepath = SRC_DIR + "out/organisations-clean.csv"

#TODO: error handling

with open(filepath, "rb") as fp:
    reader = csv.DictReader(fp)
    languages = []
    for row in reader:
        #get the list of languages from the row dict
        if len(languages) == 0:
            languages = getLanguages(row)
        organisation = TblOrganisation.create(
            identifier = row["identifier"],
            type = row["type"] if row["type"] else 0,
            country = row["countrycode"],
            is_org_file = 1 if row["is_org_file"] else 0,
            is_publisher = 1 if row["is_publisher"] else 0,
            last_updated = row["last_updated"] if row["last_updated"] else None
        )
        enName = row["en"].strip()
        if enName:
            TblName.create(
                organisation = organisation,
                name = enName,
                language = "en"
            )
        for lang in languages:
            if lang is not "en":
                name = row[lang].strip()
                if name != "" and enName != name:
                    TblName.create(
                        organisation = organisation,
                        name = name,
                        language = lang
                    )
