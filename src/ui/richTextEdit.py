
import re
from collections import OrderedDict
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

class RichTextEdit(QWidget):
    bbcode = OrderedDict()
    bbcode[re.compile("<p.*?>")] = ""
    bbcode["</p>"] = ""
    bbcode[re.compile("<span.*?font-weight:600; font-style:italic; text-decoration: underline;.*?>(.*?)</span>")] = "[b][i][u]\\1[/u][/i][/b]"
    bbcode[re.compile("<span.*?font-weight:600; font-style:italic;.*?>(.*?)</span>")] = "[b][i]\\1[/i][/b]"
    bbcode[re.compile("<span.*?font-weight:600; text-decoration: underline;.*?>(.*?)</span>")] = "[b][u]\\1[/u][/b]"
    bbcode[re.compile("<span.*?font-style:italic; text-decoration: underline;.*?>(.*?)</span>")] = "[i][u]\\1[/u][/i]"
    bbcode[re.compile("<span.*?font-weight:600;.*?>(.*?)</span>")] = "[b]\\1[/b]"
    bbcode[re.compile("<span.*?font-style:italic;.*?>(.*?)</span>")] = "[i]\\1[/i]"
    bbcode[re.compile("<span.*?text-decoration: underline;.*?>(.*?)</span>")] = "[u]\\1[/u]"

    html = OrderedDict()
    html["\n"] = "<br/>"
    html["[b][i][u]"] = '<span style="font-weight:600; font-style:italic; text-decoration: underline;">'
    html["[/u][/i][/b]"] = "</span>"
    html["[b][i]"] = '<span style="font-weight:600; font-style:italic;">'
    html["[/i][/b]"] = "</span>"
    html["[b][u]"] = '<span style="font-weight:600; text-decoration: underline;">'
    html["[/u][/b]"] = "</span>"
    html["[i][u]"] = '<span style="font-style:italic; text-decoration: underline;">'
    html["[/u][/i]"] = "</span>"
    html["[b]"] = '<span style="font-weight:600;">'
    html["[/b]"] = "</span>"
    html["[i]"] = '<span style="font-style:italic;">'
    html["[/i]"] = "</span>"
    html["[u]"] = '<span style="text-decoration: underline;">'
    html["[/u]"] = "</span>"
    html[re.compile("^(<br.*?/>)+", re.M)] = ""

    def megaReplace(strin, replaceTab):
        strout = strin
        for regex, replace in replaceTab.items():
            if "replace" in dir(regex):
                strout = strout.replace(regex, replace)
            else:
                strout = regex.sub(replace, strout)

        return strout

    def __init__(self, args, parent):
        super().__init__(parent)
        self.textEdit = QTextEdit(self)
        self.textChanged = self.textEdit.textChanged
        self.cursorPositionChanged = self.textEdit.cursorPositionChanged
        self.currentFont = self.textEdit.currentFont
        self.setCurrentFont = self.textEdit.setCurrentFont
        self.initEditor()
        self.setPlainText(args)

        self.grid = QGridLayout()
        self.grid.addWidget(self.toolBar, 0, 0)
        self.grid.addWidget(self.textEdit, 1, 0)
        self.setLayout(self.grid)

    def toPlainText(self):
        html = self.textEdit.toHtml()
        body = html[html.find("<body"):]
        body = body[body.find(">")+1:]
        body = body[0:body.find("</body>")]
        text = RichTextEdit.megaReplace(body, RichTextEdit.bbcode)
        return text

    def setPlainText(self, text):
        html = RichTextEdit.megaReplace(text, RichTextEdit.html)
        self.textEdit.setHtml(html)

    def initEditor(self):
        self.toolBar = QToolBar("Format Actions", self)
        self.cursorPositionChanged.connect(self.reloadStatus)
        self.boldBtn = QToolButton(self)
        self.boldBtn.setText("B")
        self.boldBtn.setCheckable(True)
        self.boldBtn.clicked.connect(self.toggleBold)
        self.toolBar.addWidget(self.boldBtn)
        self.italicBtn = QToolButton(self)
        self.italicBtn.setText("I")
        self.italicBtn.setCheckable(True)
        self.italicBtn.clicked.connect(self.toggleItalic)
        self.toolBar.addWidget(self.italicBtn)
        self.underlineBtn = QToolButton(self)
        self.underlineBtn.setText("U")
        self.underlineBtn.setCheckable(True)
        self.underlineBtn.clicked.connect(self.toggleUnderline)
        self.toolBar.addWidget(self.underlineBtn)
        self.reloadStatus()

    def reloadStatus(self):
        self.font = self.currentFont()
        self.boldBtn.setChecked(self.font.bold())
        self.italicBtn.setChecked(self.font.italic())
        self.underlineBtn.setChecked(self.font.underline())

    def toggleBold(self, a):
        self.font.setBold(not self.font.bold())
        self.setCurrentFont(self.font)

    def toggleItalic(self, a):
        self.font.setItalic(not self.font.italic())
        self.setCurrentFont(self.font)

    def toggleUnderline(self, a):
        self.font.setUnderline(not self.font.underline())
        self.setCurrentFont(self.font)
