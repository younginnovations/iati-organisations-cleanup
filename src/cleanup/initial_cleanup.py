# coding: utf-8
import csv
import re
import logging
from helper import getListnameFromIdentifier, OrgTypeCodelist, IATIOrgIdCodelist, OrgIdGuideList, CountryCodelist, SRC_DIR
from organisation import OrganisationMetadata, OrganisationCollection


logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("iati-organisation")
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler(SRC_DIR + 'out/initialcleanup-processing.log')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

orgidGuideList = OrgIdGuideList()
iatiOrgidCodelist = IATIOrgIdCodelist()
countryCodelist = CountryCodelist()

ORG = OrganisationMetadata
organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist, countryCodelist)

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

filepath = SRC_DIR + "data/organisation.data.xml.csv"
logger.info("Processing organisation xml data from %s", filepath)
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
            ORG.LAST_UPDATED: row[ORGCSV.LASTUPDATED].strip()
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

filepath = SRC_DIR + "data/publishers.data.scrapping.csv"
logger.info("Processing scrapped publishers data from %s", filepath)
with open(filepath, "rb") as fp:
    reader = csv.reader(fp)
    reader.next()
    for row in reader:
        identifier = row[PUBCSV.IDENTIFIER].strip() if row else ""
        if identifier == "":
            # not interested if identifier is blank
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

organisations.export2csv(SRC_DIR + "out/organisations-clean.csv")
logger.info("Valid organiations count: %d", len(organisations.orgs))
