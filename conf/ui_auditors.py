from PyQt5.QtWidgets import QLabel,QLineEdit,QPushButton,QCheckBox
import collections

PEOPLES = collections.OrderedDict()
PEOPLES["add"] = {"class":QPushButton,
                   "arg":"Add",
                   "clicked":"addAuditor",
                   "col":0}
PEOPLES["delete"] = {"class":QPushButton,
                      "arg":"Delete",
                      "clicked":"delAuditor",
                      "col":1}

PEOPLES["checkLabel"] = {"class":QLabel,
                          "arg":"Present",
                          "col":0}
PEOPLES["full_nameLabel"] = {"class":QLabel,
                              "arg":"Full name",
                              "col":1}
PEOPLES["phoneLabel"] = {"class":QLabel,
                          "arg":"Phone number",
                          "col":2}
PEOPLES["emailLabel"] = {"class":QLabel,
                          "arg":"Email",
                          "col":3}
PEOPLES["rolesLabel"] = {"class":QLabel,
                          "arg":"Role",
                          "col":4}

def addPeople(lst, doc_id, people):
    lst["check-"+str(doc_id)] = {"class":QCheckBox,
                                 "signal":"stateChanged",
                                 "signalFct":"enableRow",
                                 "col":0}
    lst["full_name-"+str(doc_id)] = {"class":QLineEdit,
                                     "signal":"textChanged",
                                     "signalFct":"updateAuditor",
                                     "arg":people["full_name"],
                                     "col":1}
    lst["phone-"+str(doc_id)] = {"class":QLineEdit,
                                 "signal":"textChanged",
                                 "signalFct":"updateAuditor",
                                 "arg":people["phone"],
                                 "setLength":20,
                                 "col":2}
    lst["email-"+str(doc_id)] = {"class":QLineEdit,
                                 "signal":"textChanged",
                                 "signalFct":"updateAuditor",
                                 "arg":people["email"],
                                 "col":3}
    lst["role-"+str(doc_id)] = {"class":QLineEdit,
                                "signal":"textChanged",
                                "signalFct":"updateAuditor",
                                "arg":people["role"],
                                "setLength":30,
                                "col":4}
