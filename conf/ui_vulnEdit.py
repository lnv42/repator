# coding=utf-8


from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QTextEdit
import collections

from src.ui.richTextEdit import RichTextEdit


def vulnEditing(doc_id, vuln, lang=""):
    # to avoid the crash when editing a new vuln or a partial vuln loaded from db
    vuln = collections.defaultdict(lambda: "", vuln)

    lst = collections.OrderedDict()
    lst["id-" + str(doc_id)] = {
        "class": QLabel,
        "label": "ID",
        "arg": str(doc_id)
    }
    lst["category"+lang+"-" + str(doc_id)] = {
        "class": QLabel,
        "label": "Category",
        "arg": vuln["category"+lang] if vuln["category"+lang] else vuln["category"]
    }
    lst["sub_category"+lang+"-" + str(doc_id)] = {
        "class": QLabel,
        "label": "Sub Category",
        "arg": vuln["sub_category"+lang] if vuln["sub_category"+lang] else vuln["sub_category"]
    }
    lst["name"+lang+"-" + str(doc_id)] = {
        "class": QLabel,
        "label": "Vulnerability",
        "arg": vuln["name"+lang] if vuln["name"+lang] else vuln["name"]
    }
    lst["labelNeg"+lang+"-" + str(doc_id)] = {
        "class": QLineEdit,
        "label": "Negative Label",
        "signal": "textChanged",
        "signalFct": "updateVuln",
        "arg": vuln["labelNeg"+lang] if vuln["labelNeg"+lang] else vuln["labelNeg"]
    }
    lst["labelPos"+lang+"-" + str(doc_id)] = {
        "class": QLineEdit,
        "label": "Positive Label",
        "signal": "textChanged",
        "signalFct": "updateVuln",
        "arg": vuln["labelPos"+lang] if vuln["labelPos"+lang] else vuln["labelPos"]
    }
    lst["observHistory"+lang+"-" + str(doc_id)] = {
        "class": QComboBox,
        "label": "Observation History",
        "signal": "currentTextChanged",
        "signalFct": "loadHistory",
        "items": vuln["observHistory"+lang] if vuln["observHistory"+lang] else vuln["observHistory"]
    }
    lst["observ"+lang+"-" + str(doc_id)] = {
        "class": RichTextEdit,
        "label": "Observation",
        "signal": "textChanged",
        "signalFct": "updateVuln",
        "arg": vuln["observ"+lang].replace("\n", "<br/>") if vuln["observ"+lang] else vuln["observ"].replace("\n", "<br/>")
    }
    lst["riskHistory"+lang+"-" + str(doc_id)] = {
        "class": QComboBox,
        "label": "Risk History",
        "signal": "currentTextChanged",
        "signalFct": "loadHistory",
        "items": vuln["riskHistory"+lang] if vuln["riskHistory"+lang] else vuln["riskHistory"]
    }
    lst["risk"+lang+"-" + str(doc_id)] = {
        "class": RichTextEdit,
        "label": "Risk",
        "signal": "textChanged",
        "signalFct": "updateVuln",
        "arg": vuln["risk"+lang].replace("\n", "<br/>") if vuln["risk"+lang] else vuln["risk"].replace("\n", "<br/>")
    }
    lst["recoHistory"+lang+"-" + str(doc_id)] = {
        "class": QComboBox,
        "label": "Recommandation History",
        "signal": "currentTextChanged",
        "signalFct": "loadHistory",
        "items": vuln["recoHistory"+lang] if vuln["recoHistory"+lang] else vuln["recoHistory"]
    }
    lst["reco"+lang+"-" + str(doc_id)] = {
        "class": RichTextEdit,
        "label": "Recommandation",
        "signal": "textChanged",
        "signalFct": "updateVuln",
        "arg": vuln["reco"+lang].replace("\n", "<br/>") if vuln["reco"+lang] else vuln["reco"].replace("\n", "<br/>")
    }
    lst["CVSS"] = {"class": QLabel,
                   "col": 0}
    lst["AV0"] = {"class": QLabel,
                  "arg": "Attack Vector",
                  "col": 1}
    lst["AC0"] = {"class": QLabel,
                  "arg": "Attack Complexity",
                  "col": 2}
    lst["PR0"] = {"class": QLabel,
                  "arg": "Privileges Required",
                  "col": 3}
    lst["UI0"] = {"class": QLabel,
                  "arg": "User Interaction",
                  "col": 4}
    lst["S0"] = {"class": QLabel,
                 "arg": "Scope",
                 "col": 5}
    lst["C0"] = {"class": QLabel,
                 "arg": "Confidentiality",
                 "col": 6}
    lst["I0"] = {"class": QLabel,
                 "arg": "Integrity",
                 "col": 7}
    lst["A0"] = {"class": QLabel,
                 "arg": "Availability",
                 "col": 8}
    lst["CVSS0"] = {"class": QLabel,
                    "arg": "CVSSv3 metrics",
                    "col": 0}
    lst["AV-" + str(doc_id)] = {"class": QComboBox,
                                "signal": "currentTextChanged",
                                "signalFct": "updateVuln",
                                "setCurrentText": vuln["AV"],
                                "items": ("Network", "Adjacent", "Local", "Physical"),
                                "col": 1}
    lst["AC-" + str(doc_id)] = {"class": QComboBox,
                                "signal": "currentTextChanged",
                                "signalFct": "updateVuln",
                                "setCurrentText": vuln["AC"],
                                "items": ("Low", "High"),
                                "col": 2}
    lst["PR-" + str(doc_id)] = {"class": QComboBox,
                                "signal": "currentTextChanged",
                                "signalFct": "updateVuln",
                                "setCurrentText": vuln["PR"],
                                "items": ("None", "Low", "High"),
                                "col": 3}
    lst["UI-" + str(doc_id)] = {"class": QComboBox,
                                "signal": "currentTextChanged",
                                "signalFct": "updateVuln",
                                "setCurrentText": vuln["UI"],
                                "items": ("None", "Required"),
                                "col": 4}
    lst["S-" + str(doc_id)] = {"class": QComboBox,
                               "signal": "currentTextChanged",
                               "signalFct": "updateVuln",
                               "setCurrentText": vuln["S"],
                               "items": ("Unchanged", "Changed"),
                               "col": 5}
    lst["C-" + str(doc_id)] = {"class": QComboBox,
                               "signal": "currentTextChanged",
                               "signalFct": "updateVuln",
                               "setCurrentText": vuln["C"],
                               "items": ("None", "Low", "High"),
                               "col": 6}
    lst["I-" + str(doc_id)] = {"class": QComboBox,
                               "signal": "currentTextChanged",
                               "signalFct": "updateVuln",
                               "setCurrentText": vuln["I"],
                               "items": ("None", "Low", "High"),
                               "col": 7}
    lst["A-" + str(doc_id)] = {"class": QComboBox,
                               "signal": "currentTextChanged",
                               "signalFct": "updateVuln",
                               "setCurrentText": vuln["A"],
                               "items": ("None", "Low", "High"),
                               "col": 8}

    lst["CVSS1"] = {"class": QLabel,
                    "col": 0}
    lst["CVSS11"] = {"class": QLabel,
                     "arg": "Base score",
                     "col": 1}
    lst["CVSS12"] = {"class": QLabel,
                     "arg": "Impact score",
                     "col": 2}
    lst["CVSS13"] = {"class": QLabel,
                     "arg": "Exploitability score",
                     "col": 3}

    lst["CVSS2"] = {"class": QLabel,
                    "arg": "CVSSv3 score",
                    "col": 0}
    lst["CVSS-" + str(doc_id)] = {"class": QLabel,
                                  "arg": "0",
                                  "col": 1}
    lst["CVSSimp-" + str(doc_id)] = {"class": QLabel,
                                     "arg": "0",
                                     "col": 2}
    lst["CVSSexp-" + str(doc_id)] = {"class": QLabel,
                                     "arg": "0",
                                     "col": 3}
    lst["CVSS3"] = {"class": QLabel,
                    "col": 0}
    lst["CVSS31"] = {"class": QLabel,
                     "arg": "Risk level",
                     "col": 1}
    lst["CVSS32"] = {"class": QLabel,
                     "arg": "Impact level",
                     "col": 2}
    lst["CVSS33"] = {"class": QLabel,
                     "arg": "Exploitability level",
                     "col": 3}

    lst["CVSS4"] = {"class": QLabel,
                    "arg": "Risk analysis",
                    "col": 0}
    lst["riskLvl-" + str(doc_id)] = {"class": QLabel,
                                     "arg": "Low",
                                     "col": 1}
    lst["impLvl-" + str(doc_id)] = {"class": QLabel,
                                    "arg": "Low",
                                    "col": 2}
    lst["expLvl-" + str(doc_id)] = {"class": QLabel,
                                    "arg": "Very Easy",
                                    "col": 3}

    return lst
