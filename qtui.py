#!/usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, Qt
from copy import copy
import sys
import json
import collections

from conf.ui import *
from dbhandler import *
from cvss import *
from reportgenerator import *

class Window(QWidget):
    def __init__(self, title, tabLst):
        super().__init__()

        self.setWindowTitle(title)
        self.setContentsMargins(0,0,0,0)

        tabw = QTabWidget()
        self.tabs = {}

        for label, tab in tabLst.items():
            if "db" in tab:
                self.tabs[label] = Tab(tabw, tab["lst"], tab["db"])
            else:
                self.tabs[label] = Tab(tabw, tab)
            tabw.addTab(self.tabs[label], label)

        saveBtn = QPushButton("Save", self)
        saveBtn.clicked.connect(self.save)
        generateBtn = QPushButton("Generate", self)
        generateBtn.clicked.connect(self.generate)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5,5,5,5)

        self.grid.addWidget(tabw, 0, 0, 1, 2)
        self.grid.addWidget(saveBtn, 1, 0)
        self.grid.addWidget(generateBtn, 1, 1)

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

    def generate(self):
        values = {}
        for tabname, tab in self.tabs.items():
            values[tabname] = tab.save()

        p = Generator.generate_json(values)
        doc = Document(docx="templates/template.docx")
        Generator.generate_docx(doc, p)
        doc.save("test.docx")


class Tab(QWidget):
    def __init__(self, parent, lst, db=None):
        super().__init__(parent)
        self.db = db
        self.initTab(lst)
        self._parent = parent

    def initTab(self, lst):
        self.row = 0
        self.lst = lst
        self.values = collections.OrderedDict()
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
        if "toPlainText" in dir(string):
            string = string.toPlainText()

        historyFieldName = fieldTab[0]+"History-"+fieldTab[1]

        if historyFieldName in self.fields:
            if self.fields[historyFieldName].currentText() != string:
                self.fields[historyFieldName].setCurrentIndex(0)

        self.db.update(int(fieldTab[1]), fieldTab[0], string)

        self.updateCvss(fieldTab[1])

    def loadHistory(self, string):
        sender = self.sender()
        if sender.currentIndex() != 0:
            historyFieldName = sender.accessibleName()
            fieldName = historyFieldName.replace("History", "")

            if fieldName in self.fields:
                self.fields[fieldName].setPlainText(string)

    def saveHistory(self, historyFieldName):
        if self.fields[historyFieldName].currentIndex() == 0:
            fieldTab = historyFieldName.split('-')
            fieldName = historyFieldName.replace("History", "")

            value = self.fields[fieldName].toPlainText()

            history = self.db.search_by_id(int(fieldTab[1]))[fieldTab[0]]

            if value not in history:
                history.append(value)

            self.db.update(int(fieldTab[1]), fieldTab[0], history)

    def saveHistories(self):
        for name in self.fields.keys():
            if name.find("History-") > 0:
                self.saveHistory(name)

    def updateCvss(self, docId):
        if "CVSS-"+str(docId) in self.fields:
            av = self.fields["AV-"+str(docId)].currentText()
            ac = self.fields["AC-"+str(docId)].currentText()
            pr = self.fields["PR-"+str(docId)].currentText()
            ui = self.fields["UI-"+str(docId)].currentText()
            s = self.fields["S-"+str(docId)].currentText()
            c = self.fields["C-"+str(docId)].currentText()
            i = self.fields["I-"+str(docId)].currentText()
            a = self.fields["A-"+str(docId)].currentText()

            cvss, imp, exp = cvssv3(av, ac, pr, ui, s, c, i, a)
            rLvl, iLvl, eLvl = riskLevel(av, ac, pr, ui, s, c, i, a)

            self.fields["CVSS-"+str(docId)].setText(str(cvss))
            self.fields["CVSSimp-"+str(docId)].setText(str(imp))
            self.fields["CVSSexp-"+str(docId)].setText(str(exp))

            self.fields["riskLvl-"+str(docId)].setText(rLvl)
            self.fields["impLvl-"+str(docId)].setText(iLvl)
            self.fields["expLvl-"+str(docId)].setText(eLvl)

    def enableRow(self, arg=None):
        sender = self.sender()
        docId = sender.accessibleName().split('-')[1]

        enable = False
        if "isSelected" in dir(sender):
            if sender.isSelected():
                enable = True

        if "isChecked" in dir(sender):
            if sender.isChecked():
                enable = True

        if "currentIndex" in dir(sender):
            if sender.currentIndex() >= 2:
                enable = True

        if enable:
            self.values[docId] = self.db.search_by_id(int(docId))
            if "currentText" in dir(sender):
                self.values[docId]["status"] = sender.currentText()
        else:
            if docId in self.values:
                del self.values[docId]

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

        self.db.update(int(fieldTab[1]), fieldTab[0], string)

    def load(self, values):
        for name, value in values.items():
            if name in self.fields:
                field = self.fields[name]
                if "setText" in dir(field):
                    field.setText(value)
                if "setCurrentText" in dir(field):
                    field.setCurrentText(value)
                if "setDate" in dir(field):
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

        if "vulns" in self.fields:
            self.values = self.fields["vulns"].save()

        return self.values

    def editVuln(self):
        sender = self.sender()
        docId = sender.accessibleName().split("-")[1]
        vuln = self.db.search_by_id(int(docId))
        lst = vulnEditing(docId, vuln)
        self._parent.addTab(str(docId), lst, self.db)
        self._parent.tabs[str(docId)].updateCvss(docId)

    def addVuln(self):
        docId = self.db.insert_record()
        lst = collections.OrderedDict()
        addVuln(lst, docId, self.db.search_by_id(docId))
        self.parseLst(lst)
        for ident, field in lst.items():
            self.lst[ident] = field

    def addAuditor(self):
        docId = self.db.insert_record()
        lst = collections.OrderedDict()
        addPeople(lst, docId, self.db.search_by_id(docId))
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

                                del self.fields[name]
                                del self.lst[name]
                                col += 1

                            idDoc = ident[ident.find('-')+1:]
                            self.db.delete(int(idDoc))

                            del self.values[idDoc]

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

            if "setLength" in field:
                charWidth = w.fontMetrics().averageCharWidth()*1.1
                w.setFixedWidth(int(charWidth*field["setLength"]))

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
    def __init__(self, args, parent):
        super().__init__(parent)

        lst = args[0]
        db = args[1]

        self.tabw = QTabWidget()
        self.tabw.setTabsClosable(True)
        self.tabw.tabCloseRequested.connect(self.closeTab)
        self.tabs = {}

        tabLst = collections.OrderedDict()
        tabLst["All"] = lst

        for label, lst in tabLst.items():
            self.addTab(label, lst, db)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5,5,5,5)

        self.grid.addWidget(self.tabw)

        self.setLayout(self.grid)

    def addTab(self, label, lst, db):
        if label in self.tabs:
            self.tabw.setCurrentWidget(self.tabs[label])
        else:
            self.tabs[label] = Tab(self, lst, db)
            self.tabw.addTab(self.tabs[label], label)
            self.tabw.setCurrentWidget(self.tabs[label])

    def closeTab(self, index):
        self.tabs[self.tabw.tabText(index)].saveHistories()
        del self.tabs[self.tabw.tabText(index)]
        self.tabw.removeTab(index)

    def save(self):
        return self.tabs["All"].save()

def main(args) :
    auditors = copy(PEOPLES)
    dba = DBHandler.Auditors()
    auditorData = dba.get_all()
    for auditor in auditorData:
        addPeople(auditors, auditor.doc_id, auditor)

    clients = copy(PEOPLES)
    dbc = DBHandler.Clients()
    clientData = dbc.get_all()
    for client in clientData:
        addPeople(clients, client.doc_id, client)

    vulns = copy(VULNS)
    dbv = DBHandler.Vulns()
    vulnData = dbv.get_all()
    for vuln in vulnData:
        addVuln(vulns, vuln.doc_id, vuln)

    tabLst = collections.OrderedDict()
    tabLst["Mission"] = copy(MISSION)
    tabLst["Auditors"] = {"lst":auditors, "db":dba}
    tabLst["Clients"] = {"lst":clients, "db":dbc}
    tabLst["Vulns"] = {"vulns":{"class":Vulns,"arg":(vulns, dbv)}}

    app=QApplication(args)
    window = Window('Repator', tabLst)

    window.loadJson('{"Mission": {"dateStart": "lun. avr. 23 2018", "dateEnd": "ven. avr. 27 2018", "client": "feafe", "environment": "pr\u00e9-production"}, "Auditors": {}, "Vulns": {"AV1": "P"}}')
    window.showMaximized()

    app.exec_()

if __name__ == "__main__" :
    main(sys.argv)
