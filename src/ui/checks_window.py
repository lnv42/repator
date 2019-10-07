"""Module for the patch/dismiss/upload buttons in "All" tab."""

# coding=utf-8

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import (QPushButton, QDialog, QGridLayout, QCheckBox,
                             QWidget, QScrollArea, QSizePolicy)


class GitButton(QPushButton):
    """Class that creates the buttons at the bottom of the "All" tab in Diffs window."""

    def __init__(self, text, action, vulns_git):
        super().__init__()
        self.text = text
        self.vulns_git = vulns_git
        self.action = action
        self.checked = dict()
        self.temp_checked = dict()
        self.clicked.connect(self.show_popup)
        self.setText(text)
        self.update_check_state()

    def update_check_state(self):
        """Updates check state for current changed vulns."""
        checked = dict()
        for key in self.vulns_git.style.keys():
            checked[key] = self.checked[key] if key in self.checked else False
        self.checked = checked

    def show_popup(self):
        """Makes the QDialog pop up and creates its layout."""
        self.update_check_state()
        self.temp_checked = dict(self.checked)

        dialog = QDialog(self)
        dialog.setMinimumWidth(300)
        dialog.setStyleSheet("Text-align:center")

        dialog.setWindowTitle(self.text)
        dialog.setModal(True)
        dialog.accepted.connect(self.accept_changes)

        scroll = QScrollArea(dialog)
        viewport = QWidget(dialog)
        scroll.setWidget(viewport)
        scroll.setWidgetResizable(True)

        select_all_button = QPushButton("Select all")
        deselect_all_button = QPushButton("Deselect all")
        show_all_button = QPushButton("Show visible")
        ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Cancel")
        select_all_button.clicked.connect(
            lambda: self.set_selection(dialog, True))
        deselect_all_button.clicked.connect(
            lambda: self.set_selection(dialog, False))
        show_all_button.clicked.connect(lambda: self.show_all(dialog))
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        layout = QGridLayout(viewport)
        viewport.setLayout(layout)
        self.draw_layout(layout, show_all=True)
        dialog_layout = QGridLayout(dialog)
        dialog.setLayout(dialog_layout)

        dialog.layout().addWidget(select_all_button, 0, 0)
        dialog.layout().addWidget(deselect_all_button, 0, 1)
        dialog.layout().addWidget(show_all_button, 0, 2)
        dialog.layout().addWidget(scroll, 1, 0, 1, -1)
        dialog.layout().addWidget(ok_button, 2, 1)
        dialog.layout().addWidget(cancel_button, 2, 2)

        # To get the right QScrollArea
        show_all_button.animateClick()

        dialog.exec()

    def draw_layout(self, layout, show_all=False):
        """Draws the layout with the list of values that are in the window."""
        values = sorted(self.get_values(), key=int) if show_all else sorted(
            self.get_visible_values(), key=int)
        # For the upload, the comparison is made with the changes made locally.
        if self.action == "upload":
            values = sorted(self.get_repator_values(), key=int) if show_all else sorted(
                self.get_visible_values(), key=int)
        row = 0
        for value in values:
            checkbox = QCheckBox(value)
            checkbox.setCheckState(
                Qt.Checked if self.checked[value] else Qt.Unchecked)
            checkbox.stateChanged.connect(self.update_check_box)
            layout.addWidget(checkbox, row, 0)
            row += 1
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(empty, row, 0)

    def get_visible_values(self):
        """Gets the vulns that are visible on screen."""
        res = set()
        for key in self.vulns_git.style.keys():
            if ("id-"+key in self.vulns_git.tabw.widget(0).fields and
                    self.vulns_git.tabw.widget(0).fields["id-" + key].isVisible()):
                res.add(key)
        return res

    def get_values(self):
        """Gets all changed values."""
        res = set()
        for key in self.vulns_git.style.keys():
            res.add(key)
        return res

    def get_repator_values(self):
        """Gets all modified values from the repator window."""
        app = QCoreApplication.instance()
        for window in app.topLevelWidgets():
            if window.windowTitle() == "Repator":
                repator = window
        print(repator.tabs["Vulns"].fields["vulns"].tabs["All"])
        return []

    def update_check_box(self):
        """Updates the list of checked boxes in self.temp_checked."""
        sender = self.sender()
        self.temp_checked[sender.text()] = sender.isChecked()

    def accept_changes(self):
        """Defines actions when "Ok" is clicked."""
        self.checked = dict(self.temp_checked)
        checked = set()
        for ident in self.checked:
            if self.checked[ident]:
                checked.add(ident)
        if self.action == "patch":
            self.vulns_git.patch_changes(checked)
        elif self.action == "dismiss":
            self.vulns_git.dismiss_changes(checked)
        elif self.action == "upload":
            self.vulns_git.upload_changes(checked)

    def set_selection(self, dialog, selection):
        """Sets all currently visible check_boxes to selection."""
        for value in self.temp_checked:
            show_all_button = dialog.layout().itemAt(2).widget()
            if ((show_all_button.text() == "Show visible") or
                    (dialog.layout().itemAt(2).widget().text() == "Show all"
                     and self.visible[value])):
                self.temp_checked[value] = selection
        layout = dialog.layout().itemAt(3).widget().widget().layout()
        for i in range(layout.count() - 1):
            layout.itemAt(i).widget().setCheckState(
                Qt.Checked if selection else Qt.Unchecked)

    def show_all(self, dialog):
        """Defines the "Show all" button behavior."""
        button = dialog.layout().itemAt(2).widget()
        layout = dialog.layout().itemAt(3).widget().widget().layout()
        GitButton.remove_layout(layout)
        if button.text() == "Show all":
            button.setText("Show visible")
            self.draw_layout(layout, show_all=True)
        else:
            button.setText("Show all")
            self.draw_layout(layout)

    @staticmethod
    def remove_layout(layout):
        """Deletes the layout's widgets."""
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()
