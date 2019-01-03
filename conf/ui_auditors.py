# coding=utf-8


import collections

from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QCheckBox

PEOPLE = collections.OrderedDict()
PEOPLE["add"] = {"class": QPushButton,
                 "arg": "Add",
                 "clicked": "addAuditor",
                 "col": 0}
PEOPLE["delete"] = {"class": QPushButton,
                    "arg": "Delete",
                    "clicked": "delAuditor",
                    "col": 1}

PEOPLE["checkLabel"] = {"class": QLabel,
                        "arg": "Present",
                        "col": 0}
PEOPLE["full_nameLabel"] = {"class": QLabel,
                            "arg": "Full name",
                            "col": 1}
PEOPLE["phoneLabel"] = {"class": QLabel,
                        "arg": "Phone number",
                        "col": 2}
PEOPLE["emailLabel"] = {"class": QLabel,
                        "arg": "Email",
                        "col": 3}
PEOPLE["rolesLabel"] = {"class": QLabel,
                        "arg": "Role",
                        "col": 4}


def addPeople(lst, doc_id, people):
    lst["check-" + str(doc_id)] = {"class": QCheckBox,
                                   "signal": "stateChanged",
                                   "signalFct": "enableRow",
                                   "col": 0}
    lst["full_name-" + str(doc_id)] = {"class": QLineEdit,
                                       "signal": "textChanged",
                                       "signalFct": "updateAuditor",
                                       "arg": people["full_name"],
                                       "col": 1}
    lst["phone-" + str(doc_id)] = {"class": QLineEdit,
                                   "signal": "textChanged",
                                   "signalFct": "updateAuditor",
                                   "arg": people["phone"],
                                   "setLength": 20,
                                   "col": 2}
    lst["email-" + str(doc_id)] = {"class": QLineEdit,
                                   "signal": "textChanged",
                                   "signalFct": "updateAuditor",
                                   "arg": people["email"],
                                   "col": 3}
    lst["role-" + str(doc_id)] = {"class": QLineEdit,
                                  "signal": "textChanged",
                                  "signalFct": "updateAuditor",
                                  "arg": people["role"],
                                  "setLength": 30,
                                  "col": 4}
