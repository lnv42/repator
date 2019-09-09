"""Module for the sort buttons in "All" tab."""

# coding=utf-8

# To make ordering cleaner and adapted to en_US
from functools import cmp_to_key
import locale

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QDialog, QGridLayout, QCheckBox,
                             QWidget, QScrollArea, QSizePolicy)


class SortButton(QPushButton):
    """Class that creates the sort buttons in "All" tab in Repator->Vuln and Diffs windows."""

    def __init__(self, column, is_repator_button, parent):
        super().__init__(parent)
        self.parent = parent
        self.tab = column
        self.values = dict()
        self.temp_values = dict()
        self.visible = dict()
        self.is_repator_button = is_repator_button
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        self.clicked.connect(self.show_popup)

    def init_sorts(self):
        """Initializes all sorting buttons"""
        self.parent.fields["categorySort"].init_button()
        self.parent.fields["sub_categorySort"].init_button()
        self.parent.fields["nameSort"].init_button()
        if self.is_repator_button:
            self.parent.fields["statusSort"].init_button()

    def update_values(self):
        """Updates the values from self.values to the current values.
        Also updates the visible ones.
        """
        values = dict()
        for widget in self.parent.fields:
            if widget[:len(self.tab) + 1] == self.tab + "-":
                value = self.parent.fields[widget].currentText(
                ) if self.tab == "isVuln" else self.parent.fields[widget].text()
                values[value] = self.values[value] if value in self.values else True
        self.values = values
        self.update_visible()

    def show_popup(self):
        """Makes the QDialog pop up and creates its layout."""
        self.temp_values = self.values
        dialog = QDialog(self)
        dialog.setMinimumWidth(300)
        dialog.setStyleSheet("Text-align:center")

        dialog.setWindowTitle("Filter " + self.accessibleName() + " by ")
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

        if self.accessibleName() != "Category":
            show_all_button.animateClick()
        else:
            show_all_button.hide()

        dialog.exec()

    def update_check_box(self):
        """Updates the list of checked boxes in self.temp_values."""
        sender = self.sender()
        self.temp_values[sender.text()] = sender.isChecked()

    def draw_layout(self, layout, show_all=False):
        """Draws the layout with the list of values that are in the window."""
        values = sorted(self.temp_values, key=cmp_to_key(locale.strcoll))
        values = [value for value in values if show_all or self.visible[value]]
        row = 0
        for value in values:
            checkbox = QCheckBox(value)
            checkbox.setCheckState(
                Qt.Checked if self.values[value] else Qt.Unchecked)
            checkbox.stateChanged.connect(self.update_check_box)
            layout.addWidget(checkbox, row, 0)
            row += 1
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(empty, row, 0)

    @staticmethod
    def remove_layout(layout):
        """Deletes the layout's widgets."""
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def show_all(self, dialog):
        """Defines the "Show all" button behavior."""
        button = dialog.layout().itemAt(2).widget()
        layout = dialog.layout().itemAt(3).widget().widget().layout()
        SortButton.remove_layout(layout)
        if button.text() == "Show all":
            button.setText("Show visible")
            self.draw_layout(layout, show_all=True)
        else:
            button.setText("Show all")
            self.draw_layout(layout)

    def update_visible(self):
        """Renews the set of visible entires."""
        visible = dict()
        for value in self.values:
            visible[value] = False
        current_categories = self.parent.fields["categorySort"].get_checked()
        current_sub_categories = self.parent.fields["sub_categorySort"].get_checked(
        )
        for widget in self.parent.fields:
            value = None
            if widget[:len("sub_category-")] == "sub_category-" or widget[:len("name-")] == "name-":
                value = self.parent.fields[widget].text()
            elif widget[:len("idVuln-")] == "isVuln-":
                value = self.parent.fields[widget].currentText()
            if value:
                doc_id = widget.split("-")[1]
                test = self.parent.fields["category-" +
                                          doc_id].text() in current_categories
                if self.tab == "name":
                    test = test and self.parent.fields["sub_category-" +
                                                       doc_id].text() in current_sub_categories
                if test:
                    visible[value] = True
        self.visible = visible

    def accept_changes(self):
        """Accept function for the dialog."""
        self.values = self.temp_values
        self.parent.fields["sub_categorySort"].update_visible()
        self.parent.fields["nameSort"].update_visible()
        self.sort_vulns()

    def set_selection(self, dialog, selection):
        """Sets all currently visible check_boxes to selection."""
        for value in self.temp_values:
            if ((dialog.layout().itemAt(2).widget().text() == "Show visible") or
                    (dialog.layout().itemAt(2).widget().text() == "Show all"
                     and self.visible[value])):
                self.temp_values[value] = selection
        layout = dialog.layout().itemAt(3).widget().widget().layout()
        for i in range(layout.count() - 1):
            layout.itemAt(i).widget().setCheckState(
                Qt.Checked if selection else Qt.Unchecked)

    def sort_vulns(self):
        """Shows and hides vulns according to the sort values selected."""
        current_categories = self.parent.fields["categorySort"].get_checked()
        current_sub_categories = self.parent.fields["sub_categorySort"].get_checked(
        )
        current_names = self.parent.fields["nameSort"].get_checked()
        if self.is_repator_button:
            current_status = self.parent.fields["statusSort"].get_checked()
        prefixes = {"id-", "diff-", "category-", "sub_category-", "name-"}
        prefixes |= {"isVuln-", "edit-",
                     "delete-"} if self.is_repator_button else {"changes-"}
        rows = set()
        for widget in self.parent.fields:
            if widget[:len("category-")] == "category-":
                rows.add(widget.split("-")[1])
        for i in rows:
            if (self.parent.fields["category-"+str(i)].text() in current_categories and
                    self.parent.fields["sub_category-"+str(i)].text() in current_sub_categories and
                    self.parent.fields["name-"+str(i)].text() in current_names
                    and (not self.is_repator_button or
                         self.parent.fields["isVuln-"+str(i)].currentText() in current_status)):
                for ident in prefixes:
                    self.parent.fields[ident + str(i)].show()
            else:
                for ident in prefixes:
                    self.parent.fields[ident + str(i)].hide()

    def get_checked(self):
        """Gets all checked values (displayed in the QDialog)."""
        res = set()
        for value in self.values:
            if self.values[value]:
                res.add(value)
        return res

    def init_button(self):
        """Updates the text written in the button, connects changes in the
        fields to an update of the field values cache and updates the values in
        the cache.
        """
        self.setAccessibleName(self.parent.fields[self.tab + "0"].text())
        self.setText(" Filter by " + self.accessibleName())
        self.setStyleSheet("Text-align:left")
        if self.is_repator_button:
            for widget in self.parent.fields:
                if widget[:len("category-")] == "category-":
                    self.parent.fields[widget].editingFinished.connect(
                        self.parent.fields["categorySort"].update_values)
                elif widget[:len("sub_category-")] == "sub_category-":
                    self.parent.fields[widget].editingFinished.connect(
                        self.parent.fields["sub_categorySort"].update_values)
                elif widget[:len("name-")] == "name-":
                    self.parent.fields[widget].editingFinished.connect(
                        self.parent.fields["nameSort"].update_values)
                elif widget[:len("isVuln-")] == "isVuln-":
                    self.parent.fields[widget].currentTextChanged.connect(
                        self.parent.fields["statusSort"].update_values)
            self.parent.fields["add"].clicked.connect(
                self.parent.fields["categorySort"].update_values)
            self.parent.fields["add"].clicked.connect(
                self.parent.fields["sub_categorySort"].update_values)
            self.parent.fields["add"].clicked.connect(
                self.parent.fields["nameSort"].update_values)
        self.update_values()

    def connect_buttons(self, doc_id):
        """Connects line buttons changes to update_values for a given doc_id."""
        self.parent.fields["category-" + str(doc_id)].editingFinished.connect(
            self.parent.fields["categorySort"].update_values)
        self.parent.fields["sub_category-" + str(doc_id)].editingFinished.connect(
            self.parent.fields["sub_categorySort"].update_values)
        self.parent.fields["name-" + str(doc_id)].editingFinished.connect(
            self.parent.fields["nameSort"].update_values)
        if self.is_repator_button:
            self.parent.fields["isVuln-" + str(doc_id)].currentTextChanged.connect(
                self.parent.fields["statusSort"].update_values)
