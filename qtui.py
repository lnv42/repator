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

tabLst = collections.OrderedDict()
tabLst["Mission"] = missionLst
tabLst["Auditors"] = auditors
tabLst["Vulns"] = {}

def main(args) :
    app=QApplication(args)
    window = Window('Repator', tabLst)

    window.loadJson('{"Mission": {"Date de d\u00e9but": "lun. avr. 23 2018", "Date de fin": "ven. avr. 27 2018", "Client": "feafe", "Environnement": "pr\u00e9-production"}, "Auditors": {}, "Vulns": {}}')
    window.showMaximized()

    app.exec_()

if __name__ == "__main__" :
    main(sys.argv)
