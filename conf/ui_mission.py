from PyQt5.QtWidgets import QLineEdit,QDateEdit
from PyQt5.QtCore import QDate
import collections

MISSION = collections.OrderedDict()
MISSION["client"] = {"label":"Client",
                        "class":QLineEdit,
                        "signal":"textChanged"}
MISSION["target"] = {"label":"Cible",
                        "class":QLineEdit,
                        "signal":"textChanged"}
MISSION["code"] = {"label":"Code",
                      "class":QLineEdit,
                      "signal":"textChanged"}
MISSION["dateStart"] = {"label":"Date de début",
                           "class":QDateEdit,
                           "signal":"dateChanged",
                           "arg":QDate.currentDate()}
MISSION["dateEnd"] = {"label":"Date de fin",
                         "class":QDateEdit,
                         "signal":"dateChanged",
                         "arg":QDate.currentDate()}
MISSION["environment"] = {"label":"Environment",
                             "class":QLineEdit,
                             "signal":"textChanged"}

