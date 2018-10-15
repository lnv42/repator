import csv
import sys

from conf.db import *
from src.dbhandler import *

def main(args) :
    dbv = DBHandler.Vulns()
    vulnData = dbv.get_all()
    vulns = DB_VULNS_DEFAULT
    vulnKeys = []
    for key in vulns.keys():
        if type(vulns[key]) is str:
            vulnKeys.append(key)

    writer = csv.DictWriter(sys.stdout, vulnKeys, extrasaction='ignore')
    writer.writeheader()

    for vuln in vulnData:
        writer.writerow(vuln)
