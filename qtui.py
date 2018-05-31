#!/usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, Qt
import sys
import json
import collections

from logichandler import AuditorHandler

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
    def __init__(self, parent, lst):
        super().__init__(parent)
        self.initTab(lst)

    def initTab(self, lst):
        self.row = 0
        self.lst = lst
        self.values = {}
        self.fields = {}

        self.grid = QGridLayout(self)
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5,5,5,5)
        self.grid.setAlignment(Qt.AlignTop)

        self.parseLst()

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

    def addAuditor(self):
        ah = AuditorHandler()
        docId = ah.add_auditor()
        lst = collections.OrderedDict()
        addAuditor(lst, docId)
        self.parseLst(lst)
        for ident, field in lst.items():
            self.lst[ident] = field

    def delAuditor(self):
        for ident, field in self.fields.items():
            selected = False
            if "isSelected" in dir(field):
                if field.isSelected():
                    selected = True

            if "isChecked" in dir(field):
                if field.isChecked():
                    selected = True

            if selected:
                for row in range(1, self.row+1):
                    if self.grid.itemAtPosition(row, 0) is not None:
                        if self.grid.itemAtPosition(row, 0).widget().accessibleName() == ident:
                            col = 0
                            while self.grid.itemAtPosition(row, col) is not None:
                                name = self.grid.itemAtPosition(row, col).widget().accessibleName()
                                self.grid.removeWidget(self.fields[name])
                                self.fields[name].deleteLater()

                                del self.values[name]
                                del self.fields[name]
                                del self.lst[name]
                                col += 1

                            idDoc = int(ident[ident.find('-')+1:])
                            ah = AuditorHandler()
                            sh.del_auditor(idDoc)
                            print(row)
                            print(idDoc)
                            print(ident)

                            self.delAuditor()

                            return

    def parseLst(self, lst=None):
        if lst == None:
            lst = self.lst

        for ident, field in lst.items():
            if "arg" in field:
                w = field["class"](field["arg"], self)
            else:
                w = field["class"](self)

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
                self.grid.addWidget(l,self.row,0)
                self.grid.addWidget(w,self.row,1)
            elif "col" in field:
                if field["col"] > 0:
                    self.row -= 1
                self.grid.addWidget(w,self.row+1,field["col"])
            else:
                self.grid.addWidget(w,self.row,0,1,2)

            self.row += 1




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
auditors["add"] = {"class":QPushButton,
                   "arg":"Add",
                   "clicked":"addAuditor",
                   "col":0}
auditors["delete"] = {"class":QPushButton,
                      "arg":"Delete",
                      "clicked":"delAuditor",
                      "col":1}

auditors["checkLabel"] = {"class":QLabel,
                       "arg":"Present",
                       "col":0}
auditors["full_nameLabel"] = {"class":QLabel,
                           "arg":"Full name",
                           "col":1}
auditors["phoneLabel"] = {"class":QLabel,
                       "arg":"Phone number",
                       "col":2}
auditors["emailLabel"] = {"class":QLabel,
                       "arg":"Email",
                       "col":3}

def addAuditor(lst, doc_id, full_name="", phone="", email=""):
    lst["check-"+str(doc_id)] = {"class":QCheckBox,
                                 "signal":"stateChanged",
                                 "col":0}
    lst["full_name-"+str(doc_id)] = {"class":QLineEdit,
                                     "signal":"textChanged",
                                     "arg":full_name,
                                     "col":1}
    lst["phone-"+str(doc_id)] = {"class":QLineEdit,
                                 "signal":"textChanged",
                                 "arg":phone,
                                 "col":2}
    lst["email-"+str(doc_id)] = {"class":QLineEdit,
                                 "signal":"textChanged",
                                 "arg":email,
                                 "col":3}

auditorHandler= AuditorHandler()
auditorData =auditorHandler.get_auditors()


for auditor in auditorData:
    print(auditor)

    addAuditor(auditors, auditor.doc_id, auditor["full_name"], auditor["phone"], auditor["email"])

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
