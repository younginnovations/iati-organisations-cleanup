import re
import os
import csv

SRC_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../"

def getListnameFromIdentifier(identifier):
    m = re.search("([^-]*)-([^-]*)-(.*)", identifier)
    registration_agency = None
    if m:
        registration_agency = "{}-{}".format(m.group(1), m.group(2))
    return registration_agency

class OrgTypeCodelist:
    def __init__(self, filepath = SRC_DIR + "data/codelist-organisation-type.csv"):
        self.types = {}
        with open(filepath, "rb") as fp:
            reader = csv.reader(fp)
            reader.next()
            for row in reader:
                self.types[row[1].lower()] = row[0]

    def getCode(self, name):
        if name.lower() in self.types.keys():
            return self.types[name.lower()]
        return name

class OrgIdGuideList:
    def __init__(self, filepath = SRC_DIR  + "data/org-id.guide.csv"):
        self.codes = {}
        with open(filepath, "rb") as fp:
            reader = csv.reader(fp)
            reader.next()
            for row in reader:
                self.codes[row[0].lower()] = row[10]

    def isValidList(self, listname):
        return listname and listname.lower() in self.codes.keys()


class IATIOrgIdCodelist:
    def __init__(self, filepath = SRC_DIR + "data/iati-identifiers.csv"):
        self.codes = {}
        with open(filepath, "rb") as fp:
            reader = csv.reader(fp)
            for row in reader:
                self.codes[row[0].lower()] = row[1]

    def isValidIdentifier(self, identifier):
        return identifier.lower() in self.codes.keys()

class CountryCodelist:
    def __init__(self, filepath = SRC_DIR + "data/codelist-country.csv"):
        self.types = {}
        with open(filepath, "rb") as fp:
            reader = csv.reader(fp)
            reader.next()
            for row in reader:
                self.types[row[1].lower()] = row[0]

    def getCode(self, name):
        if name.lower() in self.types.keys():
            return self.types[name.lower()]
        else:
            return self.tryNameVariation(name)
        return name

    def tryNameVariation(self, name):
        if "{} (THE)".format(name).lower() in self.types.keys():
            return self.types["{} (THE)".format(name).lower()]
        if name.lower() == "united kingdom":
            name = "UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)"
            return self.types[name.lower()]
        if name.lower() == "united states":
            name = "UNITED STATES OF AMERICA (THE)"
            return self.types[name.lower()]

