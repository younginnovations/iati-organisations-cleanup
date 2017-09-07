from helper import getListnameFromIdentifier
import logging
import csv

class OrganisationMetadata:
    IDENTIFIER = 1
    NAMELIST = 20
    NAME = 2
    LANGUAGE = 3
    TYPE = 4
    COUNTRY = 5
    IS_PUBLISHER = 10
    IS_ORG_FILE = 11

ORG = OrganisationMetadata

class OrganisationCollection:
    def __init__(self, orgidGuideList, iatiOrgidCodelist):
        self.logger = logging.getLogger("iati-organisation")
        self.orgidGuideList = orgidGuideList
        self.iatiOrgidCodelist = iatiOrgidCodelist
        self.orgs = {}
        self.names = {}
        self.languages = []

    def checkIdentifier(self, identifier):
        if self.orgidGuideList.isValidList(getListnameFromIdentifier(identifier)) \
        or self.iatiOrgidCodelist.isValidIdentifier(identifier):
            return True
        return False

    def checkAndUpdate(self, data):
        data[ORG.IDENTIFIER] = data[ORG.IDENTIFIER].strip()
        if not self.checkIdentifier(data[ORG.IDENTIFIER]):
            # print "Couldn't use ",data[ORG.IDENTIFIER]
            # if invalid identifier, ignore
            self.logger.error("Invalid identifier for '%s' [%s]", data[ORG.NAME], data[ORG.IDENTIFIER])
            return
        if data[ORG.IDENTIFIER] in self.orgs.keys():
            # if existing identifier, see if other data could be updated
            self.updateOtherMetadata(data)
            self.logger.debug("Updated metadata for '%s' [%s]", data[ORG.NAME], data[ORG.IDENTIFIER])
            return
        if data[ORG.NAME] in self.names:
            # if name is existing, then that's case of different identifier,
            #   need a mechanism to report this issue
            self.existingOrgName(data)
            self.logger.error("Duplicate Name '%s' for [%s] and [%s]", data[ORG.NAME], data[ORG.IDENTIFIER], self.names[data[ORG.NAME]])
            return
        # add new organisation data to the collection
        self.addNewValidOrg(data)

    def isCountryValid(self, countryname):
        return countryname.strip() != "(No country assigned)"

    """
    checks whether the name of existing organisation is to be stored or not
    """
    def isOrgNameNew(self, data):
        org = self.orgs[data[ORG.IDENTIFIER]]
        newLanguage = True
        for name in org[ORG.NAMELIST]:
            if data[ORG.LANGUAGE] and name[ORG.LANGUAGE] == data[ORG.LANGUAGE]:
                newLanguage = False
            if name[ORG.NAME] == data[ORG.NAME]:
                newLanguage = False
        if newLanguage:
            #new Language means this name is to be stored
            return True
        existingName = ""
        for name in org[ORG.NAMELIST]:
            if data[ORG.LANGUAGE] and name[ORG.LANGUAGE] == data[ORG.LANGUAGE]:
                existingName = name[ORG.NAME]
                break
        if existingName.strip() == "":
            return True
        elif existingName == data[ORG.NAME]:
            return False
        else:
            # if name already exists and the given name is long then 100 char, ignore.
            if len(data[ORG.NAME])>100:
                return False

    def updateOtherMetadata(self, data):
        org = self.orgs[data[ORG.IDENTIFIER]]
        if ORG.IS_PUBLISHER in data and data[ORG.IS_PUBLISHER]:
            org[ORG.IS_PUBLISHER] = data[ORG.IS_PUBLISHER]
        if ORG.IS_ORG_FILE in data and data[ORG.IS_ORG_FILE]:
            org[ORG.IS_ORG_FILE] = data[ORG.IS_ORG_FILE]
        if ORG.COUNTRY in data and data[ORG.COUNTRY] and self.isCountryValid(data[ORG.COUNTRY]):
            org[ORG.COUNTRY] = data[ORG.COUNTRY]
        if ORG.TYPE in data and data[ORG.TYPE]:
            org[ORG.TYPE] = data[ORG.TYPE]
        if self.isOrgNameNew(data):
            org[ORG.NAMELIST].append({
                ORG.NAME: data[ORG.NAME],
                ORG.LANGUAGE: self.getLanguage(data[ORG.LANGUAGE])
            })

    def existingOrgName(self, data):
        # report error that the identifier is different
        pass

    def getLanguage(self, language):
        language = language.lower()
        if language == "en-gb":
            language = "en"
        if not language:
            language = "en"
        if not language in self.languages:
            self.languages.append(language)
        return language

    def addNewValidOrg(self, data):
        org = {}
        org[ORG.IDENTIFIER] = data[ORG.IDENTIFIER]
        org[ORG.NAMELIST] = []
        org[ORG.NAMELIST].append({
            ORG.NAME: data[ORG.NAME],
            ORG.LANGUAGE: self.getLanguage(data[ORG.LANGUAGE])
        })
        if ORG.TYPE in data:
            org[ORG.TYPE] = data[ORG.TYPE]
        if ORG.IS_PUBLISHER in data:
            org[ORG.IS_PUBLISHER] = data[ORG.IS_PUBLISHER]
        if ORG.IS_ORG_FILE in data:
            org[ORG.IS_ORG_FILE] = data[ORG.IS_ORG_FILE]
        if ORG.COUNTRY in data and self.isCountryValid(data[ORG.COUNTRY]):
            org[ORG.COUNTRY] = data[ORG.COUNTRY]
        self.orgs[org[ORG.IDENTIFIER]] = org
        self.names[data[ORG.NAME]] = data[ORG.IDENTIFIER]
        self.logger.debug("New organisation added: '%s' [%s]", data[ORG.NAME], data[ORG.IDENTIFIER])

    def export2csv(self, outfilename):
        countRows = 0
        with open(outfilename, 'wb') as f:
            w = csv.writer(f)
            header = []
            # if multiple language for the same organisation, then show the languages in separate columns
            for lang in self.languages:
                header.append(lang)
            header += [
                "name",
                "identifier",
                "type",
                "country",
                "is_org_file",
                "is_publisher",
            ]
            w.writerow(header)
            for identifier in self.orgs:
                if identifier:
                    countRows += 1
                    org = self.orgs[identifier]
                    data = []
                    names = {}
                    for name in org[ORG.NAMELIST]:
                        names[name[ORG.LANGUAGE]] = name[ORG.NAME]
                    name = ""
                    for lang in self.languages:
                        if lang in names:
                            name = names[lang]
                            data.append(names[lang])
                        else:
                            data.append("")

                    data += [
                        name,
                        org[ORG.IDENTIFIER],
                        org[ORG.TYPE],
                        org[ORG.COUNTRY] if ORG.COUNTRY in org else "",
                        org[ORG.IS_ORG_FILE] if ORG.IS_ORG_FILE in org else "",
                        org[ORG.IS_PUBLISHER],
                    ]
                    w.writerow(data)
