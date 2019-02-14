
import re
from collections import OrderedDict
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

class RichTextEdit(QWidget):
    bbcode1 = OrderedDict()
    bbcode1[re.compile("<p.*?>")] = ""
    bbcode1["</p>"] = ""
    bbcode1[re.compile("<span(.*?)>(.*?)</span>")] = "<\\1>\\2</\\1>"

    bbcode2 = OrderedDict()
    bbcode2["</"] = "/"
    bbcode2["font-weight"] = "b"
    bbcode2["italic"] = "i"
    bbcode2["underline"] = "u"

    html = OrderedDict()
    html["\n"] = "<br/>"
    html["[biu]"] = '<span style="font-weight:600; font-style:italic; text-decoration:underline;">'
    html["[/biu]"] = "</span>"
    html["[bi]"] = '<span style="font-weight:600; font-style:italic;">'
    html["[/bi]"] = "</span>"
    html["[bu]"] = '<span style="font-weight:600; text-decoration:underline;">'
    html["[/bu]"] = "</span>"
    html["[iu]"] = '<span style="font-style:italic; text-decoration:underline;">'
    html["[/iu]"] = "</span>"
    html["[b]"] = '<span style="font-weight:600;">'
    html["[/b]"] = "</span>"
    html["[i]"] = '<span style="font-style:italic;">'
    html["[/i]"] = "</span>"
    html["[u]"] = '<span style="text-decoration:underline;">'
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

    def bbcodeEncoder(strin, replaceTab):
        strout = strin
        pos1 = strout.find('<')
        while pos1 >= 0:
            pos2 = strout.find('>')
            str1 = strout[pos1:pos2+1]
            str2 = ""
            for match, replace in replaceTab.items():
                if str1.find(match) >= 0:
                    str2 += replace

            if len(str2) > 0:
                str2 = "[" + str2 + "]"

            strout = strout.replace(str1, str2)
            pos1 = strout.find('<')
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
        text = RichTextEdit.megaReplace(body, RichTextEdit.bbcode1)
        text = RichTextEdit.bbcodeEncoder(text, RichTextEdit.bbcode2)
        return text

    def setPlainText(self, text):
        html = RichTextEdit.megaReplace(text, RichTextEdit.html)
        self.textEdit.setHtml(html)

    def initEditor(self):
        font = QFont()
        self.toolBar = QToolBar("Format Actions", self)
        self.cursorPositionChanged.connect(self.reloadStatus)
        self.boldBtn = QToolButton(self)
        self.boldBtn.setText("B")
        font.setBold(True)
        self.boldBtn.setFont(font)
        font.setBold(False)
        self.boldBtn.setCheckable(True)
        self.boldBtn.clicked.connect(self.toggleBold)
        self.toolBar.addWidget(self.boldBtn)
        self.italicBtn = QToolButton(self)
        self.italicBtn.setText("I")
        font.setItalic(True)
        self.italicBtn.setFont(font)
        font.setItalic(False)
        self.italicBtn.setCheckable(True)
        self.italicBtn.clicked.connect(self.toggleItalic)
        self.toolBar.addWidget(self.italicBtn)
        self.underlineBtn = QToolButton(self)
        self.underlineBtn.setText("U")
        font.setUnderline(True)
        self.underlineBtn.setFont(font)
        font.setUnderline(False)
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
