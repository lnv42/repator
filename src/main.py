# coding=utf-8

import sys
from copy import copy

from src.qtui import *


def main(args):
    tabLst = collections.OrderedDict()
    tabLst["Mission"] = copy(MISSION)
    tabLst["Auditors"] = dict(lst=copy(PEOPLE), db=DBHandler.Auditors(), addFct=addPeople)
    tabLst["Clients"] = dict(lst=copy(PEOPLE), db=DBHandler.Clients(), addFct=addPeople)
    tabLst["Vulns"] = dict(vulns={"class": Vulns, "arg": (copy(VULNS), DBHandler.Vulns(), addVuln)})

    app = QApplication(args)
    window = Window('Repator', tabLst)

    window.loadJson('{"Mission": {"dateStart": "lun. avr. 23 2018", "dateEnd": "ven. avr. 27 2018", "client": "feafe", "environment": "pr\u00e9-production"}, "Auditors": {}, "Vulns": {"AV1": "P"}}')
    window.showMaximized()

    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
