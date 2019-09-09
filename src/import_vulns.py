"""Module that allow the import of a cvss file with the first line as the title of the columns."""

# coding=utf-8

from collections import OrderedDict
from csv import DictReader
from json import dumps
from conf.report import LANGUAGES
from conf.db import DB_VULNS

HEADERS = ["category", "sub_category", "name", "labelNeg", "labelPos"]
CVSS = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]
HISTORIES = ["reco", "observ", "risk"]


def main(args):
    """Main process."""
    input_file = args[1]

    input_value = input(
        "This will remove your vulnerabilities.json file, make sure you have a copy of it.\n"
        + "In addition to that, you may consider closing repator because the tabs won't refresh.\n"
        + "Enter y to continue : ")

    if not (input_value in {'y', 'Y'}):
        exit(1)

    field_names = list(HEADERS)
    for history in HISTORIES:
        field_names.append(history)
        field_names.append(history + "History")
    field_names += CVSS

    list_fields = ["LANGUAGES"] + \
        [history + "History" for history in HISTORIES]

    res_dict = OrderedDict()

    with open(input_file, newline='') as csvfile:
        data = DictReader(csvfile)

        for row in data:
            for field in list_fields:
                row[field] = row[field][2:-2].split("\', \'")

            if LANGUAGES != row["LANGUAGES"]:
                print("IMPORT FAILED : Please make sure your LANGUAGES in conf/report.py are" +
                      "the same as the LANGUAGES used when your CSV file was created")
                exit(1)
            ident = row["id"]

            del row["LANGUAGES"]
            del row["id"]
            for field in dict(row):
                if not field in field_names and not row[field]:
                    del row[field]
            res_dict[ident] = row
    jsondb = "{\"_default\":" + dumps(res_dict, sort_keys=True) + "}"
    with open(DB_VULNS, 'w') as output:
        output.write(jsondb)
