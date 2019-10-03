"""Module that allow the import of a cvss file with the first line as the title of the columns."""

# coding=utf-8
from collections import OrderedDict
from csv import DictReader
from json import JSONDecoder,dumps
from conf.report import LANGUAGES
from conf.db import DB_VULNS,DB_VULNS_DEFAULT
from src.dbhandler import DBHandler
from src.db_cleaner import clean_db

MONOLANGFIELDS = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]

def _help(args):
    print("Import vulnerabilities database from a CSV file.")
    print("/!\\ Your current database will be erased ! /!\\")
    print("Usage: python3 " + args[0] + " input_file.csv")


def main(args):
    """Main process."""
    if len(args) < 2:
        _help(args)
        return
    if args[1] == '-h' or args[1] == "--help":
        _help(args)
        return

    input_file = args[1]

    print("/!\\ Your current database will be erased ! /!\\")
    print("Please make sure you have a copy of it ;)")
    print("You may also consider closing repator because the tabs won't refresh automaticaly.")

    input_value = input("Enter y if you want to continue : ")
    print()
    
    if not (input_value in {'y', 'Y'}):
        print("exit")
        exit(1)

    field_names_lang = list(DB_VULNS_DEFAULT.keys())
    for field in MONOLANGFIELDS:
        field_names_lang.remove(field)

    field_names = ["id", "LANGUAGES"] + list(DB_VULNS_DEFAULT.keys())
    if len(LANGUAGES) > 1:
        for lang in LANGUAGES:
            field_names += [
                field + lang for field in field_names_lang]

    list_fields = ["LANGUAGES"]
    for key, value in DB_VULNS_DEFAULT.items():
        if isinstance(value, list):
            list_fields += [key]

    res_dict = OrderedDict()

    with open(input_file, newline='') as csvfile:
        data = DictReader(csvfile)

        for row in data:
            for field in field_names:
                try:
                    row[field] = JSONDecoder(object_pairs_hook=OrderedDict).decode(row[field])
                except:
                    pass

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
    jsondb = "{\"_default\":" + dumps(res_dict, ensure_ascii=False, sort_keys=True) + "}"
    with open(DB_VULNS, 'w') as output:
        output.write(jsondb)

    print("New database successfuly imported.")
    clean_db(DBHandler.vulns(), DB_VULNS_DEFAULT, LANGUAGES)
    print("New database successfuly cleaned.")
