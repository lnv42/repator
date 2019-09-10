"""Module to be able to have an improved QLineEdit."""

# coding=utf-8

import re
from collections import OrderedDict

from PyQt5.QtWidgets import QWidget, QTextEdit, QGridLayout, QToolBar, QToolButton
from PyQt5.QtGui import QFont


class RichTextEdit(QWidget):
    """Class to show an improved QLineEdit in vulnerabilities histories."""
    bbcode1 = OrderedDict()
    bbcode1[re.compile("<p.*?>")] = ""
    bbcode1["</p>"] = ""
    bbcode1[re.compile("<br.*?/>")] = "\n"
    bbcode1[re.compile("<span(.*?)>(.*?)</span>")] = "<\\1>\\2</\\1>"

    bbcode2 = OrderedDict()
    bbcode2["</"] = "/"
    bbcode2["font-weight"] = "B"
    bbcode2["italic"] = "I"
    bbcode2["underline"] = "U"

    html = OrderedDict()
    html["\n"] = "<br/>"
    html["[[BIU]]"] = '<span style="font-weight:600; font-style:italic; text-decoration:underline;">'
    html["[[/BIU]]"] = "</span>"
    html["[[BI]]"] = '<span style="font-weight:600; font-style:italic;">'
    html["[[/BI]]"] = "</span>"
    html["[[BU]]"] = '<span style="font-weight:600; text-decoration:underline;">'
    html["[[/BU]]"] = "</span>"
    html["[[IU]]"] = '<span style="font-style:italic; text-decoration:underline;">'
    html["[[/IU]]"] = "</span>"
    html["[[B]]"] = '<span style="font-weight:600;">'
    html["[[/B]]"] = "</span>"
    html["[[I]]"] = '<span style="font-style:italic;">'
    html["[[/I]]"] = "</span>"
    html["[[U]]"] = '<span style="text-decoration:underline;">'
    html["[[/U]]"] = "</span>"
    html[re.compile("^(<br.*?/>)+", re.M)] = ""

    @staticmethod
    def mega_replace(strin, replace_tab):
        """Replaces strin with a list of regex to replace with what to replace it with"""
        strout = strin
        for regex, replace in replace_tab.items():
            if "replace" in dir(regex):
                strout = strout.replace(regex, replace)
            else:
                strout = regex.sub(replace, strout)
        return strout

    @staticmethod
    def bbcode_encoder(strin, replace_tab):
        """Modifies strin to include bbcodes."""
        strout = strin
        pos1 = strout.find('<') # find first tag
        while pos1 >= 0:
            pos2 = strout.find('>')
            str1 = strout[pos1:pos2+1]
            str2 = ""
            for match, replace in replace_tab.items():
                if str1.find(match) >= 0:
                    str2 += replace
            if str2 == "/":
                str2 = ""
            elif str2:
                str2 = "[[" + str2 + "]]"
            strout = strout.replace(str1, str2)
            pos1 = strout.find('<') # find next tag
        return strout

    def __init__(self, args, parent):
        super().__init__(parent)
        self.text_edit = QTextEdit(self)
        self.text_changed = self.text_edit.textChanged
        self.cursor_position_changed = self.text_edit.cursorPositionChanged
        self.current_font = self.text_edit.currentFont
        self.set_current_font = self.text_edit.setCurrentFont
        self.init_editor()
        self.set_plain_text(args)

        self.grid = QGridLayout()
        self.grid.addWidget(self.tool_bar, 0, 0)
        self.grid.addWidget(self.text_edit, 1, 0)
        self.setLayout(self.grid)

    def to_plain_text(self):
        """Extracts the inner text of a body and encodes it with bbcodes."""
        html = self.text_edit.toHtml()
        body = html[html.find("<body"):]
        body = body[body.find(">")+2:]
        body = body[0:body.find("</body>")]
        text = RichTextEdit.mega_replace(body, RichTextEdit.bbcode1)
        text = RichTextEdit.bbcode_encoder(text, RichTextEdit.bbcode2)
        return text

    def set_plain_text(self, text):
        """Replaces bbcodes with its HTML value."""
        html = RichTextEdit.mega_replace(text, RichTextEdit.html)
        self.text_edit.setHtml(html)

    def init_editor(self):
        """"Initializes the editor widget."""
        font = QFont()
        self.tool_bar = QToolBar("Format Actions", self)
        self.cursor_position_changed.connect(self.reload_status)
        self.bold_btn = QToolButton(self)
        self.bold_btn.setText("B")
        font.setBold(True)
        self.bold_btn.setFont(font)
        font.setBold(False)
        self.bold_btn.setCheckable(True)
        self.bold_btn.clicked.connect(self.toggle_bold)
        self.tool_bar.addWidget(self.bold_btn)
        self.italic_btn = QToolButton(self)
        self.italic_btn.setText("I")
        font.setItalic(True)
        self.italic_btn.setFont(font)
        font.setItalic(False)
        self.italic_btn.setCheckable(True)
        self.italic_btn.clicked.connect(self.toggle_italic)
        self.tool_bar.addWidget(self.italic_btn)
        self.underline_btn = QToolButton(self)
        self.underline_btn.setText("U")
        font.setUnderline(True)
        self.underline_btn.setFont(font)
        font.setUnderline(False)
        self.underline_btn.setCheckable(True)
        self.underline_btn.clicked.connect(self.toggle_underline)
        self.tool_bar.addWidget(self.underline_btn)
        self.reload_status()

    def reload_status(self):
        """Updates the status in self variables."""
        self.font = self.current_font()
        self.bold_btn.setChecked(self.font.bold())
        self.italic_btn.setChecked(self.font.italic())
        self.underline_btn.setChecked(self.font.underline())

    def toggle_bold(self):
        """Toggles bold."""
        self.font.setBold(not self.font.bold())
        self.set_current_font(self.font)

    def toggle_italic(self):
        """Toggles italic."""
        self.font.setItalic(not self.font.italic())
        self.set_current_font(self.font)

    def toggle_underline(self):
        """Toggles underlining."""
        self.font.setUnderline(not self.font.underline())
        self.set_current_font(self.font)
