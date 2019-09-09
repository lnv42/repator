"""Module to have edition icons in repator."""

# coding=utf-8

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

from conf.ui_diff import DIFF_EDITED_IMG, DIFF_ADDED_IMG, DIFF_DELETED_IMG


class DiffStatus(QPushButton):
    """Class used to show editing icons in repator window when edit, add or
    delete buttons are pushed.
    """
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
        self.cur_status = DiffStatus.NONE

    def added(self):
        """Changes the diff_status to ADDED."""
        self.cur_status = DiffStatus.ADDED
        self.setIcon(DiffStatus.imgAdded)
        self.setToolTip("Added")

    def edited(self):
        """Changes the diff_status to EDITED."""
        if self.cur_status != DiffStatus.ADDED:
            self.cur_status = DiffStatus.EDITED
            self.setIcon(DiffStatus.imgEdited)
            self.setToolTip("Edited")

    def deleted(self):
        """Changes the diff_status to DELETED."""
        self.cur_status = DiffStatus.DELETED
        self.setIcon(DiffStatus.imgDeleted)
        self.setToolTip("Deleted")

    def status(self):
        """Returns the current status."""
        return self.cur_status
