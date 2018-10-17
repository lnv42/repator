from copy import copy
import sys
import collections

from conf.ui import *
from src.qtui import *
from src.dbhandler import *

def main(args) :

    tabLst = collections.OrderedDict()
    tabLst["Mission"] = copy(MISSION)
    tabLst["Auditors"] = {"lst":copy(PEOPLES), "db":DBHandler.Auditors(),
                          "addFct":addPeople}
    tabLst["Clients"] = {"lst":copy(PEOPLES), "db":DBHandler.Clients(),
                         "addFct":addPeople}
    tabLst["Vulns"] = {"vulns":{"class":Vulns,"arg":(copy(VULNS),
                                                     DBHandler.Vulns(),
                                                     addVuln)}}

    app=QApplication(args)
    window = Window('Repator', tabLst)

    window.loadJson('{"Mission": {"dateStart": "lun. avr. 23 2018", "dateEnd": "ven. avr. 27 2018", "client": "feafe", "environment": "pr\u00e9-production"}, "Auditors": {}, "Vulns": {"AV1": "P"}}')
    window.showMaximized()

    app.exec_()

if __name__ == "__main__" :
    main(sys.argv)
