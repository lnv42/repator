# coding=utf-8


from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QComboBox
import collections
from src.ui.diffStatus import *

VULNS = collections.OrderedDict()
VULNS["add"] = {"class": QPushButton,
                "arg": "Add",
                "clicked": "addVuln",
                "col": 0,
                "colspan": 2}
VULNS["categorySort"] = {"class": QComboBox,
                 "items": {"All"},
                 "col": 2}
VULNS["sub_categorySort"] = {"class": QComboBox,
                 "items": {"All"},
                 "col": 3}
VULNS["nameSort"] = {"class": QComboBox,
                 "items": {"All"},
                 "col": 4}
VULNS["statusSort"] = {"class": QComboBox,
                 "items": ("All", "NA", "TODO", "Not Vulnerable", "Vulnerable"),
                 "col": 5}

VULNS["id0"] = {"class": QLabel,
                "arg": "ID",
                "col": 0,
                "colspan": 2}
VULNS["category0"] = {"class": QLabel,
                      "arg": "Category",
                      "col": 2}
VULNS["sub_category0"] = {"class": QLabel,
                          "arg": "Sub Category",
                          "col": 3}
VULNS["name0"] = {"class": QLabel,
                  "arg": "Vulnerability",
                  "col": 4}
VULNS["isVuln0"] = {"class": QLabel,
                    "arg": "Status",
                    "col": 5}


def addVuln(lst, doc_id, vuln):
    lst["id-" + str(doc_id)] = {"class": QLabel,
                                "arg": str(doc_id),
                                "col": 0}
    lst["diff-" + str(doc_id)] = {"class": DiffStatus,
                                  "col": 1}
    lst["category-" + str(doc_id)] = {"class": QLineEdit,
                                      "signal": "textChanged",
                                      "signalFct": "updateVuln",
                                      "arg": vuln["category"],
                                      "setLength": 32,
                                      "col": 2}
    lst["sub_category-" + str(doc_id)] = {"class": QLineEdit,
                                          "signal": "textChanged",
                                          "signalFct": "updateVuln",
                                          "arg": vuln["sub_category"],
                                          "setLength": 32,
                                          "col": 3}
    lst["name-" + str(doc_id)] = {"class": QLineEdit,
                                  "signal": "textChanged",
                                  "signalFct": "updateVuln",
                                  "arg": vuln["name"],
                                  "col": 4}
    lst["isVuln-" + str(doc_id)] = {"class": QComboBox,
                                    "signal": "currentTextChanged",
                                    "signalFct": "enableRow",
                                    "items": ("NA", "TODO", "Not Vulnerable", "Vulnerable"),
                                    "col": 5}
    lst["edit-" + str(doc_id)] = {"class": QPushButton,
                                  "clicked": "editVuln",
                                  "arg": "Edit",
                                  "col": 6}
    lst["delete-" + str(doc_id)] = {"class": QPushButton,
                                    "clicked": "delVuln",
                                    "arg": "Delete",
                                    "col": 7}
