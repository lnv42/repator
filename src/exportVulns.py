
from conf.db import *
from src.dbhandler import *

def main(args) :
    dbv = DBHandler.Vulns()
    vulnData = dbv.get_all()
    vulns = DB_VULNS_DEFAULT
    vulnKeys = []
    for key in vulns.keys():
        if type(vulns[key]) is str:
            print(key, end="; ")
            vulnKeys.append(key)
    print()
    for vuln in vulnData:
        for key in vulnKeys:
            print('"'+vuln[key]+'"', end="; ")
        print()
