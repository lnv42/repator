"""Defines the UI for the window "Diffs"."""

# coding=utf-8

import collections

from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit

from src.ui.diff_status import DiffStatus
from src.ui.sort_button import SortButton

VULNS_INITIAL = collections.OrderedDict()
VULNS_INITIAL["categorySort"] = {"class": SortButton,
                                 "args": ["category", False],
                                 "col": 2}
VULNS_INITIAL["sub_categorySort"] = {"class": SortButton,
                                     "args": ["sub_category", False],
                                     "col": 3}
VULNS_INITIAL["nameSort"] = {"class": SortButton,
                             "args": ["name", False],
                             "col": 4}
VULNS_INITIAL["refresh"] = {"class": QPushButton,
                            "arg": "Refresh",
                            "col": 5}
VULNS_INITIAL["id0"] = {"class": QLabel,
                        "arg": "ID",
                        "col": 0,
                        "colspan": 2}
VULNS_INITIAL["category0"] = {"class": QLabel,
                              "arg": "Category",
                              "col": 2}
VULNS_INITIAL["sub_category0"] = {"class": QLabel,
                                  "arg": "Sub Category",
                                  "col": 3}
VULNS_INITIAL["name0"] = {"class": QLabel,
                          "arg": "Vulnerability",
                          "col": 4}


def add_vuln_initial(lst, doc_id, vuln):
    """Function to add a member with this UI."""
    lst["id-" + str(doc_id)] = {"class": QLabel,
                                "arg": str(doc_id),
                                "setLength": 3,
                                "col": 0}
    lst["diff-" + str(doc_id)] = {"class": DiffStatus,
                                  "setLength": 3,
                                  "col": 1}
    lst["category-" + str(doc_id)] = {"class": QLineEdit,
                                      "arg": vuln["category"],
                                      "setReadOnly": True,
                                      "col": 2}
    lst["sub_category-" + str(doc_id)] = {"class": QLineEdit,
                                          "arg": vuln["sub_category"],
                                          "setReadOnly": True,
                                          "col": 3}
    lst["name-" + str(doc_id)] = {"class": QLineEdit,
                                  "arg": vuln["name"],
                                  "setReadOnly": True,
                                  "col": 4}
    lst["changes-" + str(doc_id)] = {"class": QPushButton,
                                     "clicked": "see_changes_vuln",
                                     "arg": "View changes",
                                     "setLength": 15,
                                     "col": 5}
