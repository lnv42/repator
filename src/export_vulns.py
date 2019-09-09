"""Module that allow the export of a cvss file with the first line as the title of the columns."""

# coding=utf-8

from json import JSONDecoder
from collections import OrderedDict
from csv import DictWriter
from conf.report import LANGUAGES

HEADERS = ["category", "sub_category", "name", "labelNeg", "labelPos"]
CVSS = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]
HISTORIES = ["reco", "observ", "risk"]


def main(args):
    """Main process."""
    if args[1] == '-h' or args[1] == "--help":
        print("Exports your vulnerabilities.json database to a CSV file.\nUsage: python" +
              args[0] + "output_file")

    field_names_lang = list(HEADERS)
    for history in HISTORIES:
        field_names_lang.append(history)
        field_names_lang.append(history + "History")
    field_names = ["id", "LANGUAGES"] + field_names_lang + CVSS
    if len(LANGUAGES) > 1:
        for lang in LANGUAGES:
            field_names += [
                field + lang for field in field_names_lang]

    output_file = args[1]
    with open("db/vulnerabilities.json", 'r') as input_file:
        input_file = input_file.read()
        dictionary = JSONDecoder(object_pairs_hook=OrderedDict).decode(
            input_file)["_default"]

    with open(output_file, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for ident in dictionary:
            dic = dict(dictionary[ident])
            dic["id"] = ident
            dic["LANGUAGES"] = LANGUAGES
            for field in field_names:
                if not field in dic:
                    dic[field] = ''
            writer.writerow(dic)
