"""Defines the UI for the window "Diffs"."""

# coding=utf-8

import collections

from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QComboBox

from src.ui.diff_status import DiffStatus
from src.ui.sort_button import SortButton

VULNS = collections.OrderedDict()
VULNS["add"] = {"class": QPushButton,
                "arg": "Add",
                "clicked": "add_vuln",
                "col": 0,
                "colspan": 2}
VULNS["categorySort"] = {"class": SortButton,
                         "args": ["category", True],
                         "col": 2}
VULNS["sub_categorySort"] = {"class": SortButton,
                             "args": ["sub_category", True],
                             "col": 3}
VULNS["nameSort"] = {"class": SortButton,
                     "args": ["name", True],
                     "col": 4}
VULNS["statusSort"] = {"class": SortButton,
                       "args": ["isVuln", True],
                       "col": 5}
VULNS["id0"] = {"class": QLabel,
                "arg": "ID",
                "col": 0,
                "colspan": 2}
VULNS["category0"] = {"class": QLabel,
                      "arg": "Category",
                      "col": 2}
VULNS["sub_category0"] = {"class": QLabel,
                          "arg": "Sub Category",
                          "col": 3}
VULNS["name0"] = {"class": QLabel,
                  "arg": "Vulnerability",
                  "col": 4}
VULNS["isVuln0"] = {"class": QLabel,
                    "arg": "Status",
                    "col": 5}


def add_vuln(lst, doc_id, vuln):
    """Function to add a member with this UI."""
    lst["id-" + str(doc_id)] = {"class": QLabel,
                                "arg": str(doc_id),
                                "col": 0}
    lst["diff-" + str(doc_id)] = {"class": DiffStatus,
                                  "col": 1}
    lst["category-" + str(doc_id)] = {"class": QLineEdit,
                                      "signal": "textChanged",
                                      "signalFct": "update_vuln",
                                      "arg": vuln["category"],
                                      "setLength": 32,
                                      "col": 2}
    lst["sub_category-" + str(doc_id)] = {"class": QLineEdit,
                                          "signal": "textChanged",
                                          "signalFct": "update_vuln",
                                          "arg": vuln["sub_category"],
                                          "setLength": 32,
                                          "col": 3}
    lst["name-" + str(doc_id)] = {"class": QLineEdit,
                                  "signal": "textChanged",
                                  "signalFct": "update_vuln",
                                  "arg": vuln["name"],
                                  "col": 4}
    lst["isVuln-" + str(doc_id)] = {"class": QComboBox,
                                    "signal": "currentTextChanged",
                                    "signalFct": "enable_row",
                                    "items": ("NA", "TODO", "Not Vulnerable", "Vulnerable"),
                                    "col": 5}
    lst["edit-" + str(doc_id)] = {"class": QPushButton,
                                  "clicked": "edit_vuln",
                                  "arg": "Edit",
                                  "col": 6}
    lst["delete-" + str(doc_id)] = {"class": QPushButton,
                                    "clicked": "del_vuln",
                                    "arg": "Delete",
                                    "col": 7}
