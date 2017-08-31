import unittest
from organisation import ORG, OrganisationMetadata, OrganisationCollection
from helper import getListnameFromIdentifier, OrgTypeCodelist, IATIOrgIdCodelist, OrgIdGuideList

orgidGuideList = OrgIdGuideList()
iatiOrgidCodelist = IATIOrgIdCodelist()


class TestOrganisationCollection(unittest.TestCase):
    def setUp(self):
        pass

    def test_neworg(self):
        organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist)
        row1 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row1)

        expected_org = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAMELIST: [
                {ORG.LANGUAGE: "en", ORG.NAME: "YIPL"},
            ]
        }
        expected_orgs = {
            "NP-CRO-41009723": expected_org
        }
        assert(len(organisations.orgs) == 1)
        assert(organisations.orgs == expected_orgs)

    def test_invalid(self):
        organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist)
        row1 = {
            ORG.IDENTIFIER: "XX-XXX-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row1)
        assert(len(organisations.orgs) == 0)

    def test_existing_org_same_id(self):
        organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist)
        row1 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row1)
        assert(len(organisations.orgs) == 1)

        row2 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row2)
        assert(len(organisations.orgs) == 1)

    def test_2_neworg(self):
        organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist)
        row1 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row1)

        expected_org = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAMELIST: [
                {ORG.LANGUAGE: "en", ORG.NAME: "YIPL"},
            ]
        }
        expected_orgs = {
            "NP-CRO-41009723": expected_org
        }
        assert(len(organisations.orgs) == 1)
        assert(organisations.orgs == expected_orgs)

        row2 = {
            ORG.IDENTIFIER: "NP-CRO-41009723-1",
            ORG.NAME: "YIPL-1",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row2)

        expected_org2 = {
            ORG.IDENTIFIER: "NP-CRO-41009723-1",
            ORG.NAMELIST: [
                {ORG.LANGUAGE: "en", ORG.NAME: "YIPL-1"},
            ]
        }
        expected_orgs = {
            "NP-CRO-41009723": expected_org,
            "NP-CRO-41009723-1": expected_org2
        }
        assert(len(organisations.orgs) == 2)
        assert(organisations.orgs == expected_orgs)

    def test_different_id_same_name(self):
        organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist)
        row1 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row1)
        expected_org = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAMELIST: [
                {ORG.LANGUAGE: "en", ORG.NAME: "YIPL"},
            ]
        }
        expected_orgs = {
            "NP-CRO-41009723": expected_org
        }
        assert(organisations.orgs == expected_orgs)
        assert(len(organisations.orgs) == 1)

        row2 = {
            ORG.IDENTIFIER: "NP-CRO-41009723-1",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row2)
        assert(organisations.orgs == expected_orgs)
        assert(len(organisations.orgs) == 1)

    def test_update_country(self):
        organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist)
        row1 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row1)
        assert(not ORG.COUNTRY in organisations.orgs["NP-CRO-41009723"])
        assert(len(organisations.orgs) == 1)

        row2 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
            ORG.COUNTRY: "Nepal",
        }
        organisations.checkAndUpdate(row2)

        expected_org = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.COUNTRY: "Nepal",
            ORG.NAMELIST: [
                {ORG.LANGUAGE: "en", ORG.NAME: "YIPL"},
            ]
        }

        assert(len(organisations.orgs) == 1)
        assert(organisations.orgs["NP-CRO-41009723"] == expected_org)
        # assert(ORG.COUNTRY in organisations.orgs["NP-CRO-41009723"])
        # assert(organisations.orgs["NP-CRO-41009723"][ORG.COUNTRY] == "Nepal")

    def test_update_type(self):
        organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist)
        row1 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row1)

        expected_org = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAMELIST: [
                {ORG.LANGUAGE: "en", ORG.NAME: "YIPL"},
            ]
        }
        assert(len(organisations.orgs) == 1)
        assert(organisations.orgs["NP-CRO-41009723"] == expected_org)
        assert(not ORG.TYPE in organisations.orgs["NP-CRO-41009723"])

        row2 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
            ORG.TYPE: 20,
        }
        organisations.checkAndUpdate(row2)

        expected_org = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.TYPE: 20,
            ORG.NAMELIST: [
                {ORG.LANGUAGE: "en", ORG.NAME: "YIPL"},
            ]
        }

        assert(len(organisations.orgs) == 1)
        assert(organisations.orgs["NP-CRO-41009723"] == expected_org)
        assert(ORG.TYPE in organisations.orgs["NP-CRO-41009723"])
        assert(organisations.orgs["NP-CRO-41009723"][ORG.TYPE] == 20)

    def test_multiple_lang(self):
        organisations = OrganisationCollection(orgidGuideList, iatiOrgidCodelist)
        row1 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL",
            ORG.LANGUAGE: "en",
        }
        organisations.checkAndUpdate(row1)
        assert(not ORG.TYPE in organisations.orgs["NP-CRO-41009723"])
        assert(len(organisations.orgs) == 1)

        row2 = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.NAME: "YIPL-fr",
            ORG.LANGUAGE: "fr",
            ORG.TYPE: 20,
        }
        organisations.checkAndUpdate(row2)

        expected_org = {
            ORG.IDENTIFIER: "NP-CRO-41009723",
            ORG.TYPE: 20,
            ORG.NAMELIST: [
                {ORG.LANGUAGE: "en", ORG.NAME: "YIPL"},
                {ORG.LANGUAGE: "fr", ORG.NAME: "YIPL-fr"}
            ]
        }
        expected_orgs = {
            "NP-CRO-41009723": expected_org
        }
        assert(organisations.orgs == expected_orgs)
        assert(organisations.orgs["NP-CRO-41009723"] == expected_org)
        # assert(len(organisations.orgs["NP-CRO-41009723"][ORG.NAMELIST])==2)
        # assert(organisations.orgs["NP-CRO-41009723"][ORG.NAMELIST][0][ORG.LANGUAGE] == "en")
        # assert(organisations.orgs["NP-CRO-41009723"][ORG.NAMELIST][1][ORG.LANGUAGE] == "fr")

if __name__ == "__main__":
    unittest.main()