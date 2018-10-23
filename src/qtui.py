#!/usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QDateTime, Qt
import json
import collections

from conf.ui import *
from src.cvss import *
from src.reportgenerator import *
from src.dbhandler import *

class Window(QWidget):
    def __init__(self, title, tabLst):
        super().__init__()

        self.setWindowTitle(title)
        self.setContentsMargins(0,0,0,0)

        tabw = QTabWidget()
        self.tabs = {}

        for label, tab in tabLst.items():
            if "addFct" in  tab:
                self.tabs[label] = Tab(tabw, tab["lst"], tab["db"], tab["addFct"])
            elif "db" in tab:
                self.tabs[label] = Tab(tabw, tab["lst"], tab["db"])
            else:
                self.tabs[label] = Tab(tabw, tab)
            tabw.addTab(self.tabs[label], label)

        saveBtn = QPushButton("Save", self)
        saveBtn.clicked.connect(self.save)
        loadBtn = QPushButton("Load", self)
        loadBtn.clicked.connect(self.load)
        generateBtn = QPushButton("Generate", self)
        generateBtn.clicked.connect(self.generate)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5,5,5,5)

        self.grid.addWidget(tabw, 0, 0, 1, 3)
        self.grid.addWidget(saveBtn, 1, 0)
        self.grid.addWidget(loadBtn, 1, 1)
        self.grid.addWidget(generateBtn, 1, 2)

        self.setLayout(self.grid)

    def loadJson(self, jsonStr):
        self.loadDict(json.loads(jsonStr))

    def loadDict(self, values):
        for tabname, tabval in values.items():
            self.tabs[tabname].load(tabval)

    def load(self):
        projectFilename = QFileDialog.getOpenFileName(self, "Load Repator Project", "projects/", "Repator Project files [*.rep] (*.rep);;All files [*] (*)")[0]
        if len(projectFilename) > 0:
            try:
                with open(projectFilename, 'r') as projectFile:
                    self.loadJson(projectFile.read())
            except:
                print("LoadFileError")

    def save(self):
        values = {}
        for tabname, tab in self.tabs.items():
            values[tabname] = tab.save(db=True)

        projectFilename = QFileDialog.getSaveFileName(self, "Save Repator Project", "projects/test.rep", "Repator Project files [*.rep] (*.rep);;All files [*] (*)")[0]
        if len(projectFilename) > 0:
            try:
                with open(projectFilename, 'w') as projectFile:
                    projectFile.write(json.dumps(values))
            except:
                print("SaveFileError")

    def generate(self):
        values = {}
        for tabname, tab in self.tabs.items():
            values[tabname] = tab.save(db=False)

        outputFilename = QFileDialog.getSaveFileName(self, "Generate Report", "output.docx", "Microsoft Document [*.docx] (*.docx);;All files [*] (*)")[0]

        Generator.generate_all(values, outputFilename)

class Tab(QScrollArea):
    def __init__(self, parent, lst, db=None, addFct=None):
        super().__init__(parent)
        self.headLst = lst
        self.db = db
        self.addFct = addFct
        self.initTab()
        self._parent = parent

    def initTab(self):
        self.row = 0
        self.lst = self.headLst
        self.values = collections.OrderedDict()
        self.fields = {}

        if self.db is not None and self.addFct is not None:
            items = self.db.get_all()
            for item in items:
                self.addFct(self.lst, item.doc_id, item)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5,5,5,5)
        self.grid.setAlignment(Qt.AlignTop)

        self.parseLst()

        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.setWidget(self.widget)
        self.setWidgetResizable(True)

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
        if "vulns" in self.fields:
            self.fields["vulns"].load(values)
            return

        if self.db is not None and "db" in values:
            creationDate = QDateTime.currentDateTime().toString("yyyyMMdd-hhmmss")
            dbPath = self.db.path+"-tmp-"+creationDate+".json"
            defaultValues = self.db.defaultValues
            self.db.close()
            self.db = DBHandler(dbPath, defaultValues)
            self.db.insert_multiple(values["db"])

            if self.addFct is not None:
                self.row = 0
                self.lst = self.headLst
                self.values.clear()
                self.fields.clear()

                items = self.db.get_all()
                for item in items:
                    self.addFct(self.lst, item.doc_id, item)
                self.parseLst()

        for name, value in values.items():
            if name.isdigit():
                docId = name
                if "check-"+docId in self.fields:
                    self.fields["check-"+docId].setCheckState(Qt.Checked)

                if "status" in value and "isVuln-"+docId in self.fields:
                        self.fields["isVuln-"+docId].setCurrentText(value["status"])

            elif name in self.fields:
                field = self.fields[name]
                if "setText" in dir(field):
                    field.setText(value)
                if "setCurrentText" in dir(field):
                    field.setCurrentText(value)
                if "setDate" in dir(field):
                    field.setDate(QDate.fromString(value))

    def save(self, db=False):
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

        if db and self.db is not None:
            self.values["db"] = self.db.get_all()

        return self.values

    def editVuln(self):
        sender = self.sender()
        docId = sender.accessibleName().split("-")[1]
        vuln = self.db.search_by_id(int(docId))
        lst = vulnEditing(docId, vuln)
        self._parent.addTab(str(docId), lst, self.db)
        if len(LANGUAGES) > 1:
            for lang in LANGUAGES:
                self._parent.tabs[str(docId)][lang].updateCvss(docId)
        else:
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
        addFct = args[2]

        self.tabw = QTabWidget()
        self.tabw.setTabsClosable(True)
        self.tabw.tabCloseRequested.connect(self.closeTab)
        self.tabs = {}

        tabLst = collections.OrderedDict()
        tabLst["All"] = lst

        for label, lst in tabLst.items():
            self.addTab(label, lst, db, addFct)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5,5,5,5)

        self.grid.addWidget(self.tabw)

        self.setLayout(self.grid)

    def addTab(self, label, lst, db, addFct=None):
        if label in self.tabs:
            self.tabw.setCurrentWidget(self.tabs[label])
        else:
            if label == "All" or len(LANGUAGES) == 1:
                self.tabs[label] = Tab(self, lst, db, addFct)
                self.tabw.addTab(self.tabs[label], label)
                self.tabw.setCurrentWidget(self.tabs[label])
            else:
                tabw = QTabWidget()
                tabs = collections.OrderedDict()
                for lang in LANGUAGES:
                    tabs[lang] = Tab(self, lst, db, addFct)
                    tabw.addTab(tabs[lang], lang)
                self.tabs[label] = tabs
                self.tabw.addTab(tabw, label)
                self.tabw.setCurrentWidget(tabw)

    def closeTab(self, index):
        self.tabs[self.tabw.tabText(index)].saveHistories()
        del self.tabs[self.tabw.tabText(index)]
        self.tabw.removeTab(index)

    def load(self, values):
        return self.tabs["All"].load(values)

    def save(self):
        return self.tabs["All"].save()

