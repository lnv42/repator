from PyQt5.QtWidgets import QPushButton,QLabel,QLineEdit,QComboBox
import collections

VULNS = collections.OrderedDict()
VULNS["add"] = {"class":QPushButton,
                "arg":"Add",
                "clicked":"addVuln",
                "col":0}
VULNS["id0"] = {"class":QLabel,
                 "arg":"ID",
                 "col":0}
VULNS["category0"] = {"class":QLabel,
                 "arg":"Category",
                 "col":1}
VULNS["name0"] = {"class":QLabel,
                  "arg":"Vulnerability",
                  "col":2}
VULNS["isVuln0"] = {"class":QLabel,
                    "arg":"Status",
                    "col":3}

def addVuln(lst, doc_id, vuln):
    lst["id-"+str(doc_id)] = {"class":QLabel,
                              "arg":str(doc_id),
                              "col":0}
    lst["category-"+str(doc_id)] = {"class":QLineEdit,
                                    "signal":"textChanged",
                                    "signalFct":"updateVuln",
                                    "arg":vuln["category"],
                                    "setLength":40,
                                    "col":1}
    lst["name-"+str(doc_id)] = {"class":QLineEdit,
                                "signal":"textChanged",
                                "signalFct":"updateVuln",
                                "arg":vuln["name"],
                                "col":2}
    lst["isVuln-"+str(doc_id)] = {"class":QComboBox,
                                  #"signal":"currentTextChanged",
                                  #"signalFct":"updateVuln",
                                  "items":("NA", "Vulnerable", "Not Vulnerable", "TODO"),
                                  "col":3}
    lst["edit-"+str(doc_id)] = {"class":QPushButton,
                                "clicked":"editVuln",
                                "arg":"Edit",
                                "col":4}
