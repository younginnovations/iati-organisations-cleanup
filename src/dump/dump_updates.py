import csv
from organisation_model import *

from datetime import datetime
from dateutil import parser

filepath = SRC_DIR + "out/organisations-clean.csv"

def checkDatabaseIfUpdatesRequired(row, languages):
    print row

    tblOrganisation = TblOrganisation.select().where(
        TblOrganisation.identifier == row["identifier"])
    tblName = TblName.select().where(TblName.organisation == tblOrganisation)

    dt = parser.parse(row["last_updated"], ignoretz=True)
    print dt
    print tblOrganisation[0].last_updated

    if dt <= tblOrganisation[0].last_updated:
        return False
    print tblOrganisation[0].identifier
    print tblOrganisation[0].type
    print tblOrganisation[0].country

    print languages

    for lang in languages:
        if lang is not "en":
            name = row[lang].strip()
            if name != "" and enName != name:
                TblName.create(
                    organisation = organisation,
                    name = name,
                    language = lang
                )

    print tblName[0].name
    print tblName[0].language

row = {
        'fr': '', 'en': 'PAX', 'nl': '', 'it': '', 'da': '', 'ja': '',
        'identifier': 'NL-KVK-30214009',
        'type': '21',
        'name': 'PAX',
        'countrycode': 'NL',
        'country': 'Netherlands',
        'is_org_file': 'true',
        'is_publisher': 'true',
        'last_updated': '2017-07-24T10:00:00Z'
        }

languages = getLanguages(row)
checkDatabaseIfUpdatesRequired(row, languages)

# with open(filepath, "rb") as fp:
#     reader = csv.DictReader(fp)
#     languages = []
#     for row in reader:
#         if len(languages) == 0:
#             languages = getLanguages(row)
#         checkDatabaseIfUpdatesRequired(row, languages)
#         break





#         organisation = TblOrganisation.create(
#             identifier = row["identifier"],
#             type = row["type"] if row["type"] else 0,
#             country = row["countrycode"],
#             is_org_file = 1 if row["is_org_file"] else 0,
#             is_publisher = 1 if row["is_publisher"] else 0
#         )
#         enName = row["en"].strip()
#         if enName:
#             TblName.create(
#                 organisation = organisation,
#                 name = enName,
#                 language = "en"
#             )
#         for lang in languages:
#             if lang is not "en":
#                 name = row[lang].strip()
#                 if name != "" and enName != name:
#                     TblName.create(
#                         organisation = organisation,
#                         name = name,
#                         language = lang
#                     )

# def updateOrganisation(row):
#     tbl_organisation = TblOrganisation.select().where(TblOrganisation.identifier == row["identifier"])
#     print tbl_organisation[0].names
#     tblName = TblName.select().where(TblName.organisation == tbl_organisation)
#     for name in tblName:
#         print name.name



# # logger.info("Dumping cleaned organisations data from %s", filepath)
# with open(filepath, "rb") as fp:
#     reader = csv.DictReader(fp)
#     languages = []
#     for row in reader:
#         #get the list of languages from the row dict
#         if len(languages) == 0:
#             languages = getLanguages(row)
#         updateOrganisation(row)
#         break