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
VULNS["sub_category0"] = {"class":QLabel,
                          "arg":"Sub Category",
                          "col":2}
VULNS["name0"] = {"class":QLabel,
                  "arg":"Vulnerability",
                  "col":3}
VULNS["isVuln0"] = {"class":QLabel,
                    "arg":"Status",
                    "col":4}

def addVuln(lst, doc_id, vuln):
    lst["id-"+str(doc_id)] = {"class":QLabel,
                              "arg":str(doc_id),
                              "col":0}
    lst["category-"+str(doc_id)] = {"class":QLineEdit,
                                    "signal":"textChanged",
                                    "signalFct":"updateVuln",
                                    "arg":vuln["category"],
                                    "setLength":32,
                                    "col":1}
    lst["sub_category-"+str(doc_id)] = {"class":QLineEdit,
                                        "signal":"textChanged",
                                        "signalFct":"updateVuln",
                                        "arg":vuln["sub_category"],
                                        "setLength":32,
                                        "col":2}
    lst["name-"+str(doc_id)] = {"class":QLineEdit,
                                "signal":"textChanged",
                                "signalFct":"updateVuln",
                                "arg":vuln["name"],
                                "col":3}
    lst["isVuln-"+str(doc_id)] = {"class":QComboBox,
                                  "signal":"currentTextChanged",
                                  "signalFct":"enableRow",
                                  "items":("NA", "TODO", "Not Vulnerable", "Vulnerable"),
                                  "col":4}
    lst["edit-"+str(doc_id)] = {"class":QPushButton,
                                "clicked":"editVuln",
                                "arg":"Edit",
                                "col":5}
