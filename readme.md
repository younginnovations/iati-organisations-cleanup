### IATI Organisations Cleanup

Scrapper prepares `organisation.data.xml.csv` from publishers' organisation XML files and `publishers.data.scrapping.csv` from publishers information from the IATI Registry.

For each organisation data, the script checks (see `OrganisationCollection>checkAndUpdate`)
* whether the organisation-list part of the identifier is valid or not based on the [org-id.guide](data/org-id.guide.csv)
* whether the organisation identifier is present in [IATI organisation codelist](iati-identifiers.csv) or not
* if the identifer already exists, then the metadata is updated if there's a change
* if the name already exists, it ignores that organisation and uses the initial identifier that has been saved
* else the data is added to the csv list for importing to the database

### Usage

#### Data Cleanup

* source are in `src/cleanup`
* Run `python initial_cleanup.py` to cleanup organisation data

It reads [data/organisation.data.xml.csv](data/organisation.data.xml.csv) and [data/publishers.data.scrapping.csv](data/publishers.data.scrapping.csv) and generates `out/organisations-clean.csv` containing valid organisations information.

The `organisations-clean.csv` is cleaned-up manually if needed.

#### Data Dump

* source are in `src/dump`
* copy `config.py.bak` to `config.py`
* create mysql database and update `config.py` with mysql credentials
* Run `python dump.py` which reads `organisations-clean.csv` and dumps the data into the database you have just created

