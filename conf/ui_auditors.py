from PyQt5.QtWidgets import QLabel,QLineEdit,QPushButton,QCheckBox
import collections

AUDITORS = collections.OrderedDict()
AUDITORS["add"] = {"class":QPushButton,
                   "arg":"Add",
                   "clicked":"addAuditor",
                   "col":0}
AUDITORS["delete"] = {"class":QPushButton,
                      "arg":"Delete",
                      "clicked":"delAuditor",
                      "col":1}

AUDITORS["checkLabel"] = {"class":QLabel,
                          "arg":"Present",
                          "col":0}
AUDITORS["full_nameLabel"] = {"class":QLabel,
                              "arg":"Full name",
                              "col":1}
AUDITORS["phoneLabel"] = {"class":QLabel,
                          "arg":"Phone number",
                          "col":2}
AUDITORS["emailLabel"] = {"class":QLabel,
                          "arg":"Email",
                          "col":3}
AUDITORS["rolesLabel"] = {"class":QLabel,
                          "arg":"Role",
                          "col":4}

def addAuditor(lst, doc_id, full_name="", phone="", email="", role=""):
    lst["check-"+str(doc_id)] = {"class":QCheckBox,
                                 "signal":"stateChanged",
                                 "col":0}
    lst["full_name-"+str(doc_id)] = {"class":QLineEdit,
                                     "signal":"textChanged",
                                     "signalFct":"updateAuditor",
                                     "arg":full_name,
                                     "col":1}
    lst["phone-"+str(doc_id)] = {"class":QLineEdit,
                                 "signal":"textChanged",
                                 "signalFct":"updateAuditor",
                                 "arg":phone,
                                 "setLength":20,
                                 "col":2}
    lst["email-"+str(doc_id)] = {"class":QLineEdit,
                                 "signal":"textChanged",
                                 "signalFct":"updateAuditor",
                                 "arg":email,
                                 "col":3}
    lst["role-"+str(doc_id)] = {"class":QLineEdit,
                                "signal":"textChanged",
                                "signalFct":"updateAuditor",
                                "arg":role,
                                "setLength":30,
                                "col":4}
