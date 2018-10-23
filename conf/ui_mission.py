from PyQt5.QtWidgets import QLineEdit,QDateEdit,QComboBox
from PyQt5.QtCore import QDate
import collections
import os

from conf.report import *

MISSION = collections.OrderedDict()
MISSION["client"] = {"label":"Client",
                     "class":QLineEdit,
                     "signal":"textChanged"}
MISSION["target"] = {"label":"Target",
                     "class":QLineEdit,
                     "signal":"textChanged"}
MISSION["code"] = {"label":"Code",
                   "class":QLineEdit,
                   "signal":"textChanged"}
MISSION["dateStart"] = {"label":"Start date",
                        "class":QDateEdit,
                        "signal":"dateChanged",
                        "arg":QDate.currentDate()}
MISSION["dateEnd"] = {"label":"End date",
                      "class":QDateEdit,
                      "signal":"dateChanged",
                      "arg":QDate.currentDate()}
MISSION["environment"] = {"label":"Environment",
                          "class":QLineEdit,
                          "signal":"textChanged"}
MISSION["template"] = {"label":"Template",
                       "class":QComboBox,
                       "signal":"currentTextChanged",
                       "items":os.listdir(REPORT_TEMPLATE_DIR)}
