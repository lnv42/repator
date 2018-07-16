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

    def changeValue(self,string):
        sender = self.sender()
        field = sender.accessibleName()

        if "toString" in dir(string):
            self.values[field] = string.toString()
        else:
            self.values[field] = string

    def updateVuln(self, string):
        sender = self.sender()
        fieldName = sender.accessibleName()

        fieldTab = fieldName.split('-')

        vh = VulnHandler()
        if "toString" in dir(string):
            vh.update_vuln(int(fieldTab[1]), fieldTab[0], string.toString())
            self.values[fieldName] = string.toString()
        else:
            print(fieldTab[0])
            vh.update_vuln(int(fieldTab[1]), fieldTab[0], string)
            self.values[fieldName] = string

    def updateAuditor(self, string):
        sender = self.sender()
        fieldName = sender.accessibleName()

        fieldTab = fieldName.split('-')

        ah = AuditorHandler()
        if "toString" in dir(string):
            ah.update_auditor(int(fieldTab[1]), fieldTab[0], string.toString())
            self.values[fieldName] = string.toString()
        else:
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
        lst = collections.OrderedDict()
        addVuln(lst, docId, vuln["category"], vuln["name"])
        help(self)
        help(self._parent)
        self._parent.addTab(str(docId), lst)

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
        self.tabs[label] = Tab(self, lst)
        self.tabw.addTab(self.tabs[label], label)

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
                                "signal":"clicked",
                                "signalFct":"editVuln",
                                "arg":"Edit",
                                "col":4}

vulnHandler= VulnHandler()
vulnData =vulnHandler.get_vulns()


for vuln in vulnData:
    print(vuln)

    addVuln(vulns, vuln.doc_id, vuln["category"], vuln["name"])


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
