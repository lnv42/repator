#!/usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, Qt
import sys
import json
import collections

class Window(QWidget):
    def __init__(self, title, tabLst):
        super().__init__()

        self.setWindowTitle(title)
        self.setContentsMargins(0,0,0,0)

        tabw = QTabWidget()
        self.tabs = {}

        for label, lst in tabLst.items():
            self.tabs[label] = Tab(tabw, lst)
            tabw.addTab(self.tabs[label], label)

        saveBtn = QPushButton("Save", self)
        saveBtn.clicked.connect(self.save)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5,5,5,5)

        self.grid.addWidget(tabw)
        self.grid.addWidget(saveBtn)

        self.setLayout(self.grid)

    def loadJson(self, jsonStr):
        self.load(json.loads(jsonStr))

    def load(self, values):
        for tabname, tabval in values.items():
            self.tabs[tabname].load(tabval)

    def save(self):
        values = {}
        for tabname, tab in self.tabs.items():
            values[tabname] = tab.save()

        print(json.dumps(values))


class Tab(QWidget):
    def __init__(self, parrent, lst):
        super().__init__(parrent)

        self.lst = lst
        self.values = {}
        self.fields = {}

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5,5,5,5)
        self.grid.setAlignment(Qt.AlignTop)

        self.parseLst()

        self.setLayout(self.grid)

    def changeValue(self,string):
        sender = self.sender()
        field = sender.accessibleName()

        if "toString" in dir(string):
            self.values[field] = string.toString()
        else:
            self.values[field] = string

    def load(self, values):
        for name, value in values.items():
            if name in self.fields:
                field = self.fields[name]
                if "setText" in dir(field):
                    field.setText(value)
                if "setCurrentText" in dir(field):
                    field.setCurrentText(value)
                if "setDate" in dir(field):
                    print(value)
                    field.setDate(QDate.fromString(value))

    def save(self):
        if "list" in self.fields:
            lst = self.fields["list"]
            cpt = 0
            outLst = {}
            while cpt < lst.count():
                item = lst.item(cpt)

                if (item.flags() & Qt.ItemIsUserCheckable == Qt.ItemIsUserCheckable):
                    outLst[item.text()] = item.checkState()
                else:
                    outLst[item.text()] = True

                cpt += 1
            self.values["list"] = outLst

        return self.values

    def addItem(self):
        listOpt = self.lst["list"]["list"]
        li = listOpt["class"]("", self.fields["list"])
        if "flags" in listOpt:
            li.setFlags(listOpt["flags"])
        if "setData" in listOpt:
            for arg1, arg2 in listOpt["setData"].items():
                li.setData(arg1, arg2)

        li.setFlags(li.flags()|Qt.ItemIsEditable)

    def delItem(self):
        lst = self.fields["list"]
        for item in lst.selectedItems():
            lst.takeItem(lst.row(item))

    def parseLst(self):
        cpt = 0
        for ident, field in self.lst.items():
            if "arg" in field:
                w = field["class"](field["arg"])
            else:
                w = field["class"]()

            w.setAccessibleName(ident)
            self.fields[ident] = w

            if "help" in field:
                w.setToolTip(field["help"])

            if "signal" in field:
                getattr(w, field["signal"]).connect(self.changeValue)
                if "arg" in field:
                    getattr(w, field["signal"]).emit(field["arg"])

            if "clicked" in field:
                w.clicked.connect(getattr(self, field["clicked"]))

            if "list" in field:
                for line in field["list"]["lines"]:
                    li = field["list"]["class"](line, w)
                    if "flags" in field["list"]:
                        li.setFlags(field["list"]["flags"])
                    if "setData" in field["list"]:
                        for arg1, arg2 in field["list"]["setData"].items():
                            li.setData(arg1, arg2)

            if "items" in field:
                for item in field["items"]:
                    w.addItem(item)

            if "flags" in field:
                w.setFlags(field["flags"])

            if "setData" in field:
                for arg1, arg2 in field["setData"].items():
                    w.setData(arg1, arg2)

            if "selectionMode" in field:
                w.setSelectionMode(field["selectionMode"])

            if "label" in field:
                l = QLabel(field["label"])
                self.grid.addWidget(l,cpt,0)
                self.grid.addWidget(w,cpt,1)
            elif "col" in field:
                if field["col"] > 0:
                    cpt -= 1
                self.grid.addWidget(w,cpt+1,field["col"])
            else:
                self.grid.addWidget(w,cpt,0,1,2)

            cpt += 1




missionLst = collections.OrderedDict()
missionLst["client"] = {"label":"Client",
                        "class":QLineEdit,
                        "signal":"textChanged"}
missionLst["target"] = {"label":"Cible",
                        "class":QLineEdit,
                        "signal":"textChanged"}
missionLst["code"] = {"label":"Code",
                      "class":QLineEdit,
                      "signal":"textChanged"}
missionLst["dateStart"] = {"label":"Date de début",
                           "class":QDateEdit,
                           "signal":"dateChanged",
                           "arg":QDate.currentDate()}
missionLst["dateEnd"] = {"label":"Date de fin",
                         "class":QDateEdit,
                         "signal":"dateChanged",
                         "arg":QDate.currentDate()}
missionLst["environment"] = {"label":"Environment",
                             "class":QLineEdit,
                             "signal":"textChanged"}

auditors = collections.OrderedDict()
auditors["list"] = {"class":QListWidget,
                    "selectionMode":QAbstractItemView.ExtendedSelection,
                    "list":{"class":QListWidgetItem,
                            "lines":("John Doe", "Jack Palmer"),
                            "setData":{Qt.CheckStateRole:Qt.Checked},
                            "flags":Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsDragEnabled|Qt.ItemIsEditable}}
auditors["add"] = {"class":QPushButton,
                   "arg":"Add",
                   "clicked":"addItem"}
auditors["delete"] = {"class":QPushButton,
                      "arg":"Delete",
                      "clicked":"delItem"}

vulns = collections.OrderedDict()
vulns["cat0"] = {"class":QLabel,
                 "arg":"Category",
                 "col":0}
vulns["name0"] = {"class":QLabel,
                 "arg":"Vulnerability",
                 "col":0}
vulns["isVuln0"] = {"class":QLabel,
                   "arg":"Status",
                   "col":1}
vulns["Observation0"] = {"class":QLabel,
                        "arg":"Observation",
                         "col":2}
vulns["Risk0"] = {"class":QLabel,
                  "arg":"Risk",
                  "col":3}
vulns["AV0"] = {"class":QLabel,
                "arg":"AV",
                "col":4}
vulns["AC0"] = {"class":QLabel,
                "arg":"AC",
                "col":5}
vulns["PR0"] = {"class":QLabel,
                "arg":"PR",
                "col":6}
vulns["UI0"] = {"class":QLabel,
                "arg":"UI",
                "col":7}
vulns["S0"] = {"class":QLabel,
               "arg":"S",
               "col":8}
vulns["C0"] = {"class":QLabel,
               "arg":"C",
               "col":9}
vulns["I0"] = {"class":QLabel,
               "arg":"I",
               "col":10}
vulns["A0"] = {"class":QLabel,
               "arg":"A",
               "col":11}
vulns["name1"] = {"class":QLineEdit,
                 "signal":"textChanged",
                 "arg":"SQLi",
                 "col":0}
vulns["isVuln1"] = {"class":QComboBox,
                   "signal":"currentTextChanged",
                   "items":("NA", "Vulnerable", "Not Vulnerable", "TODO"),
                   "col":1}
vulns["Observation1"] = {"class":QLineEdit,
                        "signal":"textChanged",
                        "arg":"Some field are vulnerable to SQL injection.",
                         "col":2}
vulns["Risk1"] = {"class":QLineEdit,
                  "signal":"textChanged",
                  "arg":"SQL injection mean that data stored in the database can be leaked and may be editable. In some case code execution is possible.",
                  "col":3}
vulns["AV1"] = {"class":QComboBox,
                "signal":"currentTextChanged",
                "items":("N", "A", "L", "P"),
                "help":"Attack Vector\nN: Network\nA: Adjacent\nL: Local\nP: Physical",
                "col":4}
vulns["AC1"] = {"class":QComboBox,
                "signal":"currentTextChanged",
                "items":("L", "H"),
                "help":"Attack Complexity\nL: Low\nH: High",
                "col":5}
vulns["PR1"] = {"class":QComboBox,
                "signal":"currentTextChanged",
                "items":("N", "L", "H"),
                "help":"Privileges Required\nN: None\nL: Low\nH: High",
                "col":6}
vulns["UI1"] = {"class":QComboBox,
                "signal":"currentTextChanged",
                "items":("N", "R"),
                "help":"User Interaction\nN: None\nR: Required",
                "col":7}
vulns["S1"] = {"class":QComboBox,
               "signal":"currentTextChanged",
               "items":("U", "C"),
               "help":"Scope\nU: Unchanged\nC: Changed",
               "col":8}
vulns["C1"] = {"class":QComboBox,
               "signal":"currentTextChanged",
               "items":("N", "L", "H"),
               "help":"Confidentiality\nN: None\nL: Low\nH: High",
               "col":9}
vulns["I1"] = {"class":QComboBox,
               "signal":"currentTextChanged",
               "items":("N", "L", "H"),
               "help":"Integrity\nN: None\nL: Low\nH: High",
               "col":10}
vulns["A1"] = {"class":QComboBox,
               "signal":"currentTextChanged",
               "items":("N", "L", "H"),
               "help":"Availability\nN: None\nL: Low\nH: High",
               "col":11}

vulns["name2"] = {"class":QLineEdit,
                 "signal":"textChanged",
                 "arg":"XSS",
                 "col":0}
vulns["isVuln2"] = {"class":QComboBox,
                   "signal":"currentTextChanged",
                   "items":("NA", "Vulnerable", "Not Vulnerable", "TODO"),
                   "col":1}
vulns["Observation2"] = {"class":QLineEdit,
                        "signal":"textChanged",
                        "arg":"Some field are vulnerable to HTML code injection.",
                        "col":2}
vulns["Risk2"] = {"class":QLineEdit,
                  "signal":"textChanged",
                  "arg":"XSS mean that a malicious person can tricks a user to make him execute some arbitrary code.",
                  "col":3}
vulns["AV2"] = {"class":QComboBox,
                "signal":"currentTextChanged",
                "items":("N", "A", "L", "P"),
                "col":4}
vulns["AC2"] = {"class":QComboBox,
                "signal":"currentTextChanged",
                "items":("L", "H"),
                "col":5}
vulns["PR2"] = {"class":QComboBox,
                "signal":"currentTextChanged",
                "items":("N", "L", "H"),
                "col":6}
vulns["UI2"] = {"class":QComboBox,
                "signal":"currentTextChanged",
                "items":("N", "R"),
                "col":7}
vulns["S2"] = {"class":QComboBox,
               "signal":"currentTextChanged",
               "items":("U", "C"),
               "col":8}
vulns["C2"] = {"class":QComboBox,
               "signal":"currentTextChanged",
               "items":("N", "L", "H"),
               "col":9}
vulns["I2"] = {"class":QComboBox,
               "signal":"currentTextChanged",
               "items":("N", "L", "H"),
               "col":10}
vulns["A2"] = {"class":QComboBox,
               "signal":"currentTextChanged",
               "items":("N", "L", "H"),
               "col":11}

tabLst = collections.OrderedDict()
tabLst["Mission"] = missionLst
tabLst["Auditors"] = auditors
tabLst["Vulns"] = vulns

def main(args) :
    app=QApplication(args)
    window = Window('Repator', tabLst)

    window.loadJson('{"Mission": {"dateStart": "lun. avr. 23 2018", "dateEnd": "ven. avr. 27 2018", "client": "feafe", "environment": "pr\u00e9-production"}, "Auditors": {}, "Vulns": {"AV1": "P"}}')
    window.showMaximized()

    app.exec_()

if __name__ == "__main__" :
    main(sys.argv)
