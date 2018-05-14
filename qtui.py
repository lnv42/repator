#!/usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
import sys
import json

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
        #print(json.dumps(self.values))
        return self.values

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

            if "list" in field:
                for line in field["list"]["lines"]:
                    field["list"]["class"](line, w)

            if "label" in field:
                l = QLabel(field["label"])
                self.grid.addWidget(l,cpt,0)
                self.grid.addWidget(w,cpt,1)

            else:
                self.grid.addWidget(w,cpt,0,1,2)

            cpt += 1



missionLst = {
    "client":{"label":"Client",
              "class":QLineEdit,
              "signal":"textChanged"},
    "target":{"label":"Cible",
              "class":QLineEdit,
              "signal":"textChanged"},
    "code":{"label":"Code",
            "class":QLineEdit,
            "signal":"textChanged"},
    "dateStart":{"label":"Date de début",
                 "class":QDateEdit,
                 "signal":"dateChanged",
                 "arg":QDate.currentDate()},
    "dateEnd":{"label":"Date de fin",
               "class":QDateEdit,
               "signal":"dateChanged",
               "arg":QDate.currentDate()},
    "environment":{"label":"Environment",
                   "class":QLineEdit,
                   "signal":"textChanged"},
    "list":{"class":QListWidget,
            "list":{"class":QListWidgetItem,
                    "lines":["aa"]}}
}

tabLst = {"Mission":missionLst, "Auditors":{}, "Vulns":{}}

def main(args) :
    app=QApplication(args)
    window = Window('Repator', tabLst)

    window.loadJson('{"Mission": {"Date de d\u00e9but": "lun. avr. 23 2018", "Date de fin": "ven. avr. 27 2018", "Client": "feafe", "Environnement": "pr\u00e9-production"}, "Auditors": {}, "Vulns": {}}')
    window.showMaximized()

    app.exec_()

if __name__ == "__main__" :
    main(sys.argv)
