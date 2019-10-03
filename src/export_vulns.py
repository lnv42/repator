"""Module that allow the export of a cvss file with the first line as the title of the columns."""

# coding=utf-8

from json import JSONDecoder,dumps
from collections import OrderedDict
from csv import DictWriter
from conf.report import LANGUAGES
from conf.db import DB_VULNS,DB_VULNS_DEFAULT

MONOLANGFIELDS = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]

def _help(args):
    print("Exports your vulnerabilities.json database to a CSV file.")
    print("Usage: python3 " + args[0] + " output_file.csv")


def main(args):
    """Main process."""
    if len(args) < 2:
        _help(args)
        return
    if args[1] == '-h' or args[1] == "--help":
        _help(args)
        return

    field_names_lang = list(DB_VULNS_DEFAULT.keys())
    for field in MONOLANGFIELDS:
        field_names_lang.remove(field)

    field_names = ["id", "LANGUAGES"] + list(DB_VULNS_DEFAULT.keys())
    if len(LANGUAGES) > 1:
        for lang in LANGUAGES:
            field_names += [
                field + lang for field in field_names_lang]

    output_file = args[1]
    with open(DB_VULNS, 'r') as input_file:
        input_file = input_file.read()
        dictionary = JSONDecoder(object_pairs_hook=OrderedDict).decode(
            input_file)["_default"]

    with open(output_file, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for ident in dictionary:
            dic = OrderedDict(dictionary[ident])
            dic["id"] = ident
            dic["LANGUAGES"] = LANGUAGES
            for field in field_names:
                if not field in dic:
                    dic[field] = ''
                if not isinstance(dic[field], str):
                    dic[field] = dumps(dic[field])
            writer.writerow(dic)
