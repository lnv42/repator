
from collections import OrderedDict
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QMouseEvent, QFocusEvent

from conf.ui_diff import *

class DiffStatus(QPushButton):
    imgEdited = None
    imgAdded = None
    imgDeleted = None
    NONE = 0
    ADDED = 1
    EDITED = 2
    DELETED = 3

    def __init__(self, parent):
        super().__init__(parent)
        if DiffStatus.imgEdited is None:
            DiffStatus.imgEdited = QIcon(DIFF_EDITED_IMG)
        if DiffStatus.imgAdded is None:
            DiffStatus.imgAdded = QIcon(DIFF_ADDED_IMG)   
        if DiffStatus.imgDeleted is None:
            DiffStatus.imgDeleted = QIcon(DIFF_DELETED_IMG)
        self.setFlat(1)
        self.curStatus = DiffStatus.NONE

    def added(self):
        self.curStatus = DiffStatus.ADDED
        self.setIcon(DiffStatus.imgAdded)
        self.setToolTip("Added")

    def edited(self):
        if self.curStatus != DiffStatus.ADDED:
            self.curStatus = DiffStatus.EDITED
            self.setIcon(DiffStatus.imgEdited)
            self.setToolTip("Edited")

    def deleted(self):
        self.curStatus = DiffStatus.DELETED
        self.setIcon(DiffStatus.imgDeleted)
        self.setToolTip("Deleted")

    def status(self):
        return self.curStatus
