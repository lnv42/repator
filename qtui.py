#!/usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, Qt
import sys
import json
import collections

from logichandler import *

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
        self._parent = parent

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

    def changeValue(self, string=None):
        sender = self.sender()
        field = sender.accessibleName()

        if string is None:
            string = sender
        if "toString" in dir(string):
            string = string.toString()
        if "toHtml" in dir(string):
            string = string.toHtml()

        self.values[field] = string

    def updateVuln(self, string=None):
        sender = self.sender()
        fieldName = sender.accessibleName()

        fieldTab = fieldName.split('-')

        if string is None:
            string = sender
        if "toString" in dir(string):
            string = string.toString()
        if "toHtml" in dir(string):
            string = string.toHtml()

        vh = VulnHandler()

        vh.update_vuln(int(fieldTab[1]), fieldTab[0], string)
        self.values[fieldName] = string

        self.updateCvss(fieldTab[1])

    def updateCvss(self, docId):
        if "CVSS-"+str(docId) in self.fields:
            cvss, imp, exp, rLvl, iLvl, eLvl = cvssFromValues(self.values, docId)
            self.values["CVSS-"+str(docId)] = cvss
            self.fields["CVSS-"+str(docId)].setText(str(cvss))
            self.values["CVSSimp-"+str(docId)] = imp
            self.fields["CVSSimp-"+str(docId)].setText(str(imp))
            self.values["CVSSexp-"+str(docId)] = exp
            self.fields["CVSSexp-"+str(docId)].setText(str(exp))

            self.values["riskLvl-"+str(docId)] = rLvl
            self.fields["riskLvl-"+str(docId)].setText(rLvl)
            self.values["impLvl-"+str(docId)] = iLvl
            self.fields["impLvl-"+str(docId)].setText(iLvl)
            self.values["expLvl-"+str(docId)] = eLvl
            self.fields["expLvl-"+str(docId)].setText(eLvl)

    def updateAuditor(self, string=None):
        sender = self.sender()
        fieldName = sender.accessibleName()

        fieldTab = fieldName.split('-')

        if string is None:
            string = sender
        if "toString" in dir(string):
            string = string.toString()
        if "toHtml" in dir(string):
            string = string.toHtml()

        ah = AuditorHandler()

        ah.update_auditor(int(fieldTab[1]), fieldTab[0], string)
        self.values[fieldName] = string

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

    def editVuln(self):
        sender = self.sender()
        docId = sender.accessibleName().split("-")[1]
        vh = VulnHandler()
        vuln = vh.search_vuln_by_id(int(docId))
        lst = vulnEditing(docId, vuln)
        self._parent.addTab(str(docId), lst)
        self._parent.tabs[str(docId)].updateCvss(docId)

    def addVuln(self):
        vh = VulnHandler()
        docId = vh.add_vuln()
        lst = collections.OrderedDict()
        addVuln(lst, docId)
        self.parseLst(lst)
        for ident, field in lst.items():
            self.lst[ident] = field

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
                            ah.del_auditor(idDoc)
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
                if "signalFct" in field:
                    getattr(w, field["signal"]).connect(getattr(self, field["signalFct"]))
                else:
                    getattr(w, field["signal"]).connect(self.changeValue)
                if "arg" in field:
                    try:
                        getattr(w, field["signal"]).emit(field["arg"])
                    except:
                        pass

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

            if "setCurrentText" in field:
                w.setCurrentText(field["setCurrentText"])

            if "selectionMode" in field:
                w.setSelectionMode(field["selectionMode"])

            if "label" in field:
                l = QLabel(field["label"])
                self.grid.addWidget(l,self.row,0)
                self.grid.addWidget(w,self.row,1, 1, -1)
            elif "col" in field:
                if field["col"] > 0:
                    self.row -= 1
                if "colspan" in field:
                    self.grid.addWidget(w,self.row+1,field["col"], 1, field["colspan"])
                else:
                    self.grid.addWidget(w,self.row+1,field["col"])
            else:
                self.grid.addWidget(w,self.row,0,1,2)

            self.row += 1

class Vulns(QWidget):
    def __init__(self, lst, parent):
        super().__init__(parent)

        #self.lst = lst
        #self.values = parent.values
        #self.fields = parent.fields

        #self.grid = QGridLayout()
        #self.grid.setSpacing(5)
        #self.grid.setContentsMargins(5,5,5,5)
        #self.grid.setAlignment(Qt.AlignTop)

        #Tab.parseLst(self)

        #self.setLayout(self.grid)

        self.tabw = QTabWidget()
        self.tabw.setTabsClosable(True)
        self.tabw.tabCloseRequested.connect(self.closeTab)
        self.tabs = {}

        tabLst = collections.OrderedDict()
        tabLst["All"] = lst

        for label, lst in tabLst.items():
            self.addTab(label, lst)

        #saveBtn = QPushButton("Save", self)
        #saveBtn.clicked.connect(self.save)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5,5,5,5)

        self.grid.addWidget(self.tabw)
        #self.grid.addWidget(saveBtn)

        self.setLayout(self.grid)

    def addTab(self, label, lst):
        if label in self.tabs:
            self.tabw.setCurrentWidget(self.tabs[label])
        else:
            self.tabs[label] = Tab(self, lst)
            self.tabw.addTab(self.tabs[label], label)
            self.tabw.setCurrentWidget(self.tabs[label])

    def closeTab(self, index):
        del self.tabs[self.tabw.tabText(index)]
        self.tabw.removeTab(index)

    def changeValue(self,string):
        return Tab.changeValue(self, string)

    #def addItem(self):
    #    return Tab.addItem(self)

    #def delItem(self):
    #    return Tab.delItem(self)


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
auditors["rolesLabel"] = {"class":QLabel,
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
                                "col":4}

auditorHandler= AuditorHandler()
auditorData =auditorHandler.get_auditors()


for auditor in auditorData:
    print(auditor)

    addAuditor(auditors, auditor.doc_id, auditor["full_name"], auditor["phone"], auditor["email"])

vulns = collections.OrderedDict()
vulns["add"] = {"class":QPushButton,
                "arg":"Add",
                "clicked":"addVuln",
                "col":0}
vulns["id0"] = {"class":QLabel,
                 "arg":"ID",
                 "col":0}
vulns["category0"] = {"class":QLabel,
                 "arg":"Category",
                 "col":1}
vulns["name0"] = {"class":QLabel,
                  "arg":"Vulnerability",
                  "col":2}
vulns["isVuln0"] = {"class":QLabel,
                    "arg":"Status",
                    "col":3}
def addVuln(lst, doc_id, category="", name=""):
    lst["id-"+str(doc_id)] = {"class":QLabel,
                              "arg":str(doc_id),
                              "col":0}
    lst["category-"+str(doc_id)] = {"class":QLineEdit,
                                    "signal":"textChanged",
                                    "signalFct":"updateVuln",
                                    "arg":category,
                                    "col":1}
    lst["name-"+str(doc_id)] = {"class":QLineEdit,
                                "signal":"textChanged",
                                "signalFct":"updateVuln",
                                "arg":name,
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

vulnHandler= VulnHandler()
vulnData =vulnHandler.get_vulns()


for vuln in vulnData:
    print(vuln)

    addVuln(vulns, vuln.doc_id, vuln["category"], vuln["name"])

def vulnEditing(doc_id, vuln):
    lst = collections.OrderedDict()
    lst["id-"+str(doc_id)] = {"class":QLabel,
                              "label": "ID",
                              "arg":str(doc_id)}
    lst["category-"+str(doc_id)] = {"class":QLineEdit,
                                    "label":"Category",
                                    "signal":"textChanged",
                                    "signalFct":"updateVuln",
                                    "arg":vuln["category"]}
    lst["name-"+str(doc_id)] = {"class":QLineEdit,
                                "label":"Vulnerability",
                                "signal":"textChanged",
                                "signalFct":"updateVuln",
                                "arg":vuln["name"]}
    lst["isVuln-"+str(doc_id)] = {"class":QComboBox,
                                  "label":"Status",
                                  #"signal":"currentTextChanged",
                                  #"signalFct":"updateVuln",
                                  "items":("NA", "Vulnerable", "Not Vulnerable", "TODO")}
    lst["observ-"+str(doc_id)] = {"class":QTextEdit,
                                  "label":"Observation",
                                  "signal":"textChanged",
                                  "signalFct":"updateVuln",
                                  "arg":vuln["observ"]}
    lst["risk-"+str(doc_id)] = {"class":QTextEdit,
                                "label":"Risk",
                                "signal":"textChanged",
                                "signalFct":"updateVuln",
                                "arg":vuln["risk"]}
    lst["CVSS"] = {"class":QLabel,
                     "col":0}
    lst["AV0"] = {"class":QLabel,
                  "arg":"Attack Vector",
                  "col":1}
    lst["AC0"] = {"class":QLabel,
                  "arg":"Attack Complexity",
                  "col":2}
    lst["PR0"] = {"class":QLabel,
                  "arg":"Privileges Required",
                  "col":3}
    lst["UI0"] = {"class":QLabel,
                  "arg":"User Interaction",
                  "col":4}
    lst["S0"] = {"class":QLabel,
                 "arg":"Scope",
                 "col":5}
    lst["C0"] = {"class":QLabel,
                 "arg":"Confidentiality",
                 "col":6}
    lst["I0"] = {"class":QLabel,
                 "arg":"Integrity",
                 "col":7}
    lst["A0"] = {"class":QLabel,
                 "arg":"Availability",
                 "col":8}
    lst["CVSS0"] = {"class":QLabel,
                      "arg":"CVSSv3 metrics",
                      "col":0}
    lst["AV-"+str(doc_id)] = {"class":QComboBox,
                              "signal":"currentTextChanged",
                              "signalFct":"updateVuln",
                              "setCurrentText":vuln["AV"],
                              "items":("Network", "Adjacent Network", "Local", "Physical"),
                              "col":1}
    lst["AC-"+str(doc_id)] = {"class":QComboBox,
                              "signal":"currentTextChanged",
                              "signalFct":"updateVuln",
                              "setCurrentText":vuln["AC"],
                              "items":("Low", "High"),
                              "col":2}
    lst["PR-"+str(doc_id)] = {"class":QComboBox,
                              "signal":"currentTextChanged",
                              "signalFct":"updateVuln",
                              "setCurrentText":vuln["PR"],
                              "items":("None", "Low", "High"),
                              "col":3}
    lst["UI-"+str(doc_id)] = {"class":QComboBox,
                              "signal":"currentTextChanged",
                              "signalFct":"updateVuln",
                              "setCurrentText":vuln["UI"],
                              "items":("None", "Required"),
                              "col":4}
    lst["S-"+str(doc_id)] = {"class":QComboBox,
                             "signal":"currentTextChanged",
                             "signalFct":"updateVuln",
                             "setCurrentText":vuln["S"],
                             "items":("Unchanged", "Changed"),
                             "col":5}
    lst["C-"+str(doc_id)] = {"class":QComboBox,
                             "signal":"currentTextChanged",
                             "signalFct":"updateVuln",
                             "setCurrentText":vuln["C"],
                             "items":("None", "Low", "High"),
                             "col":6}
    lst["I-"+str(doc_id)] = {"class":QComboBox,
                             "signal":"currentTextChanged",
                             "signalFct":"updateVuln",
                             "setCurrentText":vuln["I"],
                             "items":("None", "Low", "High"),
                             "col":7}
    lst["A-"+str(doc_id)] = {"class":QComboBox,
                             "signal":"currentTextChanged",
                             "signalFct":"updateVuln",
                             "setCurrentText":vuln["A"],
                             "items":("None", "Low", "High"),
                             "col":8}

    lst["CVSS1"] = {"class":QLabel,
                      "col":0}
    lst["CVSS11"] = {"class":QLabel,
                       "arg":"Base score",
                       "col":1}
    lst["CVSS12"] = {"class":QLabel,
                       "arg":"Impact score",
                       "col":2}
    lst["CVSS13"] = {"class":QLabel,
                       "arg":"Exploitability score",
                       "col":3}

    lst["CVSS2"] = {"class":QLabel,
                      "arg":"CVSSv3 score",
                      "col":0}
    lst["CVSS-"+str(doc_id)] = {"class":QLabel,
                                  "arg":"0",
                                  "col":1}
    lst["CVSSimp-"+str(doc_id)] = {"class":QLabel,
                                   "arg":"0",
                                   "col":2}
    lst["CVSSexp-"+str(doc_id)] = {"class":QLabel,
                                   "arg":"0",
                                   "col":3}
    lst["CVSS3"] = {"class":QLabel,
                      "col":0}
    lst["CVSS31"] = {"class":QLabel,
                       "arg":"Risk level",
                       "col":1}
    lst["CVSS32"] = {"class":QLabel,
                       "arg":"Impact level",
                       "col":2}
    lst["CVSS33"] = {"class":QLabel,
                       "arg":"Exploitability level",
                       "col":3}

    lst["CVSS4"] = {"class":QLabel,
                      "arg":"Risk analysis",
                      "col":0}
    lst["riskLvl-"+str(doc_id)] = {"class":QLabel,
                                  "arg":"Low",
                                  "col":1}
    lst["impLvl-"+str(doc_id)] = {"class":QLabel,
                                   "arg":"Low",
                                   "col":2}
    lst["expLvl-"+str(doc_id)] = {"class":QLabel,
                                   "arg":"Very Easy",
                                   "col":3}

    return lst

def cvssFromValues(v, doc_id):
    av = v["AV-"+str(doc_id)]
    ac = v["AC-"+str(doc_id)]
    pr = v["PR-"+str(doc_id)]
    ui = v["UI-"+str(doc_id)]
    s = v["S-"+str(doc_id)]
    c = v["C-"+str(doc_id)]
    i = v["I-"+str(doc_id)]
    a = v["A-"+str(doc_id)]
    cvss, imp, exp = cvssv3(av, ac, pr, ui, s, c, i, a)
    rLvl, iLvl, eLvl = riskLevel(av, ac, pr, ui, s, c, i, a)
    return cvss, imp, exp, rLvl, iLvl, eLvl

def cvssv3(av, ac, pr, ui, s, c, i, a):
    AV = {"Network": 0.85, "Adjacent Network": 0.62, "Local": 0.55, "Physical": 0.2}
    AC = {"Low": 0.77, "High": 0.44}
    if s == "Changed":
        PR = {"None": 0.85, "Low": 0.68, "High": 0.5}
    else:
        PR = {"None": 0.85, "Low": 0.62, "High": 0.27}
    UI = {"None": 0.85, "Required": 0.62}
    CIA = {"None": 0, "Low": 0.22, "High": 0.56}
    av = AV[av]
    ac = AC[ac]
    pr = PR[pr]
    ui = UI[ui]
    c = CIA[c]
    i = CIA[i]
    a = CIA[a]
    exp = 8.22 * av * ac * pr * ui
    imp = 1-((1-c)*(1-i)*(1-a))
    if s == "Changed":
        imp = 7.52*(imp-0.029) - 3.25*(imp-0.02)**15
        score = 1.08 * (imp+exp)
    else:
        imp = 6.42 * imp
        score = imp + exp
    if imp <= 0:
        score = 0
    if score > 10:
        score = 10
    return score, imp, exp

def riskLevel(av, ac, pr, ui, s, c, i, a):
    CIA = {"None": 0, "Low": 1, "High": 2}
    S = {"Unchanged": False, "Changed": True}
    c = CIA[c]
    i = CIA[i]
    a = CIA[a]
    s = S[s]

    if c == 2 or i == 2 or (c*2+i*2+a >= 5 and s):
        iLvl = 4
    elif a == 2 or c*2+i*2+a >= 5 or (c*2+i*2+a >= 3 and s):
        iLvl = 3
    elif c*2+i*2+a >= 3 or s:
        iLvl = 2
    else:
        iLvl = 1

    AV = {"Network": 1, "Adjacent Network": 2, "Local": 3, "Physical": 4}
    AC = {"Low": 1, "High": 2}
    PR = {"None": 0, "Low": 1, "High": 2}
    UI = {"None": False, "Required": True}
    av = AV[av]
    ac = AC[ac]
    pr = PR[pr]
    ui = UI[ui]

    if av == 4 or pr == 2 or (av == 3 and pr == 1 and ui) or (ac == 2 and (av == 3 or pr == 1 or ui)):
        eLvl = 1
    elif ac == 2 or av == 3 or (av == 2 and (pr == 1 or ui)) or (pr == 1 and ui):
        eLvl = 2
    elif av == 2 or pr == 1 or ui:
        eLvl = 3
    else:
        eLvl = 4

    if (iLvl == 1 and eLvl <= 2) or (eLvl == 1 and iLvl <= 2):
        rLvl = 1
    elif (iLvl <= 3 and eLvl <= 2) or iLvl == 1:
        rLvl = 2
    elif (iLvl <= 4 and eLvl <= 2) or (iLvl <= 3 and eLvl <= 3) or iLvl == 2:
        rLvl = 3
    else:
        rLvl = 4

    RLVL = {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}
    ILVL = {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}
    ELVL = {1:"Dificult", 2:"Medium", 3:"Easy", 4:"Very Easy"}

    return RLVL[rLvl], ILVL[iLvl], ELVL[eLvl]

vulnsClass = collections.OrderedDict()
vulnsClass["vulns"] = {"class":Vulns,
                       "arg":vulns}

tabLst = collections.OrderedDict()
tabLst["Mission"] = missionLst
tabLst["Auditors"] = auditors
tabLst["Vulns"] = vulnsClass

def main(args) :
    app=QApplication(args)
    window = Window('Repator', tabLst)

    window.loadJson('{"Mission": {"dateStart": "lun. avr. 23 2018", "dateEnd": "ven. avr. 27 2018", "client": "feafe", "environment": "pr\u00e9-production"}, "Auditors": {}, "Vulns": {"AV1": "P"}}')
    window.showMaximized()

    app.exec_()

if __name__ == "__main__" :
    main(sys.argv)
