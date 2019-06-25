#!/usr/bin/python3
# coding=utf-8

from PyQt5.QtWidgets import *

from conf.ui import *
from src.dbhandler import *
from src.reportgenerator import *
from src.ui.tab import Tab

class Window(QWidget):
    def __init__(self, title, tabLst):
        super().__init__()

        self.setWindowTitle(title)
        self.setContentsMargins(0, 0, 0, 0)

        tabw = QTabWidget()
        self.tabs = {}

        for label, tab in tabLst.items():
            if "addFct" in tab:
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
        self.grid.setContentsMargins(5, 5, 5, 5)

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
        projectFilename = QFileDialog.getOpenFileName(self, "Load Repator Project", "projects/",
                                                      "Repator Project files [*.rep] (*.rep);;All files [*] (*)")[0]
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

        projectFilename = QFileDialog.getSaveFileName(self, "Save Repator Project", "projects/test.rep",
                                                      "Repator Project files [*.rep] (*.rep);;All files [*] (*)")[0]
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

        outputFilename = QFileDialog.getSaveFileName(self, "Generate Report", "output.docx",
                                                     "Microsoft Document [*.docx] (*.docx);;All files [*] (*)")[0]

        if outputFilename:
            Generator.generate_all(values, outputFilename)
