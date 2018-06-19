"""
Pulls the list of publishers information from https://iatiregistry.org/publisher and creates a CSV file for further processing
"""
import requests
import os
import time
import csv
from bs4 import BeautifulSoup

scrape_flag = False
DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"
OUT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/out/"
publishers_filename = os.path.join(DATA_DIR,"registry_publishers.html")
if time.time() - os.path.getctime(publishers_filename) > (60*60*24):
    # only scrape file if the file is older than 24 hours old
    scrape_flag = True
if scrape_flag:
    print("scraping")
    r = requests.get("https://iatiregistry.org/publisher")
    if r.status_code == 200:
        with open(publishers_filename, "w") as filehandler:
            filehandler.write(r.text.encode("utf-8"))

class OrgTypeCodelist:
    def __init__(self, filepath = DATA_DIR + "codelist-organisation-type.csv"):
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

class CountryCodelist:
    def __init__(self, filepath = DATA_DIR + "codelist-country.csv"):
        self.types = {}
        with open(filepath, "rb") as fp:
            reader = csv.reader(fp)
            reader.next()
            for row in reader:
                self.types[row[1].lower()] = row[0]

    def getCode(self, name):
        if name.lower() in self.types.keys():
            return self.types[name.lower()]
        code = self.tryNameVariation(name)
        if not code:
            code = self.tryRegion(name)
            if code == "NIL":
                code = ""
        if not code:
            return ""
        return code

    def tryNameVariation(self, name):
        if "{} (THE)".format(name).lower() in self.types.keys():
            return self.types["{} (THE)".format(name).lower()]
        if name.lower() == "united kingdom":
            name = "UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)"
            return self.types[name.lower()]
        if name.lower() == "united states":
            name = "UNITED STATES OF AMERICA (THE)"
            return self.types[name.lower()]
        if name.lower() == "korea, republic of":
            name = "KOREA (REPUBLIC OF)"
            return self.types[name.lower()]
        return False

    def tryRegion(self, name):
        if name.lower() == "(no country assigned)":
            return "NIL"
        if name.lower() == "bilateral, unspecified":
            return "NIL"
        if name.lower() == "africa, regional":
            return "NIL"
        if name.lower() == "asia, regional":
            return "NIL"
        if name.lower() == "europe, regional":
            return "NIL"

orgTypeCodelist = OrgTypeCodelist()
countryCodelist = CountryCodelist()
# prepare csv file from the html
publishers_csv = os.path.join(OUT_DIR,"registry_publishers.csv")
with open(publishers_filename, "r") as filehandler:
    content = filehandler.read()
    soup = BeautifulSoup(content, 'html.parser')
    with open(publishers_csv, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name","identifier", "type", "typename", "countrycode", "country"])
        for tr in soup.find_all("tr")[1:]:
            tds = tr.find_all("td")
            tds = list(tds)
            name = tds[0].text.strip().encode("utf-8")
            identifier = tds[1].text
            type = tds[2].text
            type_code = orgTypeCodelist.getCode(type)
            country = tds[3].text.encode("utf-8")
            country_code = countryCodelist.getCode(country)
            # a = tds[0].find_all("a")[0]
            writer.writerow([name, identifier, type_code, type, country_code, country])

