# coding=utf-8


import csv
from src.dbhandler import *


def main(args):
    vulns = DB_VULNS_DEFAULT
    vulnKeys = []
    for key in vulns.keys():
        if type(vulns[key]) is str:
            vulnKeys.append(key)

    with open(args[1], 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, skipinitialspace=True)

        newVuln = DB_VULNS_DEFAULT
        dbv = DBHandler.Vulns()
        dbv.purge()

        first = True
        for row in reader:
            if len(row[-1]) == 0:
                row = row[:-1]

            if first:
                first = False
                if vulnKeys != row:
                    print("Keys present in the csv are not matching db's keys")
                    print("Présent keys:")
                    print(row)
                    print("Exepected keys:")
                    print(vulnKeys)
                    break
                continue

            for key, value in zip(vulnKeys, row):
                newVuln[key] = value

            dbv.insert_record(newVuln)
