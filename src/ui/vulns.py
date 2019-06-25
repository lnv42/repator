#!/usr/bin/python3
# coding=utf-8

from PyQt5.QtWidgets import *
from collections import OrderedDict

from conf.ui import *
from src.ui.tab import Tab

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

        tabLst = OrderedDict()
        tabLst["All"] = lst

        for label, lst in tabLst.items():
            self.addTab(label, lst, db, addFct)

        # Remove close button for the first tab ("All")
        self.tabw.tabBar().setTabButton(0, QTabBar.RightSide, None)
        self.tabw.tabBar().setTabButton(0, QTabBar.LeftSide, None)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5, 5, 5, 5)

        self.grid.addWidget(self.tabw)

        self.setLayout(self.grid)
        self.tabs["All"].initSorts()

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
                tabs = OrderedDict()
                for lang in LANGUAGES:
                    tabs[lang] = Tab(self, lst[lang], db, addFct)
                    tabw.addTab(tabs[lang], lang)
                self.tabs[label] = tabs
                self.tabw.addTab(tabw, label)
                self.tabw.setCurrentWidget(tabw)

    def closeTab(self, index):
        if len(LANGUAGES) == 1:
            self.tabs[self.tabw.tabText(index)].saveHistories()
        else:
            for lang in LANGUAGES:
                self.tabs[self.tabw.tabText(index)][lang].saveHistories()
        del self.tabs[self.tabw.tabText(index)]
        self.tabw.removeTab(index)

    def load(self, values):
        return self.tabs["All"].load(values)

    def save(self):
        return self.tabs["All"].save()
