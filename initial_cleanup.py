# coding: utf-8
import csv
import re
from helper import getListnameFromIdentifier, OrgTypeCodelist, IATIOrgIdCodelist, OrgIdGuideList
from organisation import OrganisationMetadata, OrganisationCollection

orgidGuideList = OrgIdGuideList()
iatiOrgidCodelist = IATIOrgIdCodelist()

ORG = OrganisationMetadata
organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist)

class OrganisationCSVColumn:
    VERSION = 0
    LANGUAGE = 1
    IDENTIFIER = 2
    NAME = 3
    FILEPATH = 4
    REPORTINGORG_ID = 5
    REPORTINGORG_TYPE = 6
    REPORTINGORG_NAME = 7
    LASTUPDATED = 8

class PublisherCSVColumn:
    NAME = 0
    TYPE = 1
    IDENTIFIER = 2
    COUNTRY = 3

ORGCSV = OrganisationCSVColumn()
PUBCSV = PublisherCSVColumn()

filepath = "data/organisation.data.xml.csv"
with open(filepath, "rb") as fp:
    reader = csv.reader(fp)
    reader.next()
    for row in reader:
        identifier = row[ORGCSV.IDENTIFIER].strip()
        if identifier == "":
            # not interested for blank identifiers
            continue
        organisations.checkAndUpdate({
            ORG.IDENTIFIER: identifier,
            ORG.NAME: row[ORGCSV.NAME].strip(),
            ORG.TYPE: "",
            ORG.COUNTRY: "",
            ORG.LANGUAGE: row[ORGCSV.LANGUAGE].strip(),
            ORG.IS_ORG_FILE: "true",
            ORG.IS_PUBLISHER: "false",
        })
        if row[ORGCSV.REPORTINGORG_ID].strip() == "":
            continue
        # update reporting_organisation information as well
        organisations.checkAndUpdate({
            ORG.IDENTIFIER: row[ORGCSV.REPORTINGORG_ID].strip(),
            ORG.NAME: row[ORGCSV.REPORTINGORG_NAME].strip(),
            ORG.TYPE: row[ORGCSV.REPORTINGORG_TYPE].strip(),
            ORG.LANGUAGE: row[ORGCSV.LANGUAGE].strip(),
            ORG.IS_PUBLISHER: "true",
        })

orgTypeCodelist = OrgTypeCodelist()

filepath = "data/publishers.data.scrapping.csv"
with open(filepath, "rb") as fp:
    reader = csv.reader(fp)
    reader.next()
    for row in reader:
        identifier = row[PUBCSV.IDENTIFIER].strip()
        if identifier == "":
            # not interested for blank identifiers
            continue
        organisations.checkAndUpdate({
            ORG.IDENTIFIER: row[PUBCSV.IDENTIFIER].strip(),
            ORG.NAME: row[PUBCSV.NAME].strip(),
            ORG.LANGUAGE: "",
            ORG.TYPE: orgTypeCodelist.getCode(row[PUBCSV.TYPE].strip()),
            ORG.COUNTRY: row[PUBCSV.COUNTRY].strip(),
            ORG.IS_ORG_FILE: "",
            ORG.IS_PUBLISHER: "true",
        })

print organisations.export2csv("out/organisations-new2.csv")
