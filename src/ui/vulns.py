"""Defines the features used for the "Vulns" tab."""

# coding=utf-8

from collections import OrderedDict

from PyQt5.QtWidgets import QWidget, QTabWidget, QTabBar, QGridLayout

from conf.report import LANGUAGES
from src.ui.tab import Tab


class Vulns(QWidget):
    """Class for the features of the "Vulns" tab."""

    def __init__(self, args, parent):
        super().__init__(parent)

        self.lst = args[0]
        self.database = args[1]
        self.add_fct = args[2]

        self.tabs = {}
        self.init_tab()
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5, 5, 5, 5)

        self.grid.addWidget(self.tabw)

        self.setLayout(self.grid)

    def init_tab(self):
        """Tab widget initialization."""
        self.tabw = QTabWidget()
        self.tabw.setTabsClosable(True)
        self.tabw.tabCloseRequested.connect(self.close_tab)

        tab_lst = OrderedDict()
        tab_lst["All"] = self.lst

        for label, lst in tab_lst.items():
            self.add_tab(label, lst, self.database, self.add_fct)

        # Remove close button for the first tab ("All")
        self.tabw.tabBar().setTabButton(0, QTabBar.RightSide, None)
        self.tabw.tabBar().setTabButton(0, QTabBar.LeftSide, None)

        self.tabs["All"].fields["categorySort"].init_sorts()

    def add_tab(self, label, lst, database, add_fct=None):
        """Method to add a tab to the Vulns tab widget."""
        if label in self.tabs:
            for i in range(self.tabw.count()):
                if self.tabw.tabText(i) == label:
                    self.tabw.setCurrentWidget(self.tabw.widget(i))
                    return
        else:
            if label == "All" or len(LANGUAGES) == 1:
                self.tabs[label] = Tab(self, lst, database, add_fct)
                self.tabw.addTab(self.tabs[label], label)
                self.tabw.setCurrentWidget(self.tabs[label])
            else:
                tabw = QTabWidget()
                tabs = OrderedDict()
                for lang in LANGUAGES:
                    tabs[lang] = Tab(self, lst[lang], database, add_fct)
                    tabw.addTab(tabs[lang], lang)
                self.tabs[label] = tabs
                self.tabw.addTab(tabw, label)
                self.tabw.setCurrentWidget(tabw)

    def close_tab(self, index):
        """Close tab button handler."""
        if len(LANGUAGES) == 1:
            self.tabs[self.tabw.tabText(index)].save_histories()
        else:
            for lang in LANGUAGES:
                self.tabs[self.tabw.tabText(index)][lang].save_histories()
        del self.tabs[self.tabw.tabText(index)]
        self.tabw.removeTab(index)

    def load(self, values):
        """Tab load."""
        return self.tabs["All"].load(values)

    def save(self):
        """Tab save."""
        return self.tabs["All"].save()
