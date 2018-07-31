from copy import copy
import sys
import collections

from conf.ui import *
from src.qtui import *
from src.dbhandler import *

def main(args) :
    auditors = copy(PEOPLES)
    dba = DBHandler.Auditors()
    auditorData = dba.get_all()
    for auditor in auditorData:
        addPeople(auditors, auditor.doc_id, auditor)

    clients = copy(PEOPLES)
    dbc = DBHandler.Clients()
    clientData = dbc.get_all()
    for client in clientData:
        addPeople(clients, client.doc_id, client)

    vulns = copy(VULNS)
    dbv = DBHandler.Vulns()
    vulnData = dbv.get_all()
    for vuln in vulnData:
        addVuln(vulns, vuln.doc_id, vuln)

    tabLst = collections.OrderedDict()
    tabLst["Mission"] = copy(MISSION)
    tabLst["Auditors"] = {"lst":auditors, "db":dba}
    tabLst["Clients"] = {"lst":clients, "db":dbc}
    tabLst["Vulns"] = {"vulns":{"class":Vulns,"arg":(vulns, dbv)}}

    app=QApplication(args)
    window = Window('Repator', tabLst)

    window.loadJson('{"Mission": {"dateStart": "lun. avr. 23 2018", "dateEnd": "ven. avr. 27 2018", "client": "feafe", "environment": "pr\u00e9-production"}, "Auditors": {}, "Vulns": {"AV1": "P"}}')
    window.showMaximized()

    app.exec_()

if __name__ == "__main__" :
    main(sys.argv)
