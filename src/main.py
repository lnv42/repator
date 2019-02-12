# coding=utf-8

from copy import copy
from sys import path
import fire
from configparser import ConfigParser
from collections import OrderedDict
from PyQt5.QtWidgets import QApplication

from conf.ui import *
from src.dbhandler import *
from src.ui.window import Window
from src.ui.vulns import Vulns

def main(conf=None):
    tabLst = OrderedDict()
    tabLst["Mission"] = copy(MISSION)
    tabLst["Auditors"] = dict(lst=copy(PEOPLE), db=DBHandler.Auditors(), addFct=addPeople)
    tabLst["Clients"] = dict(lst=copy(PEOPLE), db=DBHandler.Clients(), addFct=addPeople)
    tabLst["Vulns"] = dict(vulns={"class": Vulns, "arg": (copy(VULNS), DBHandler.Vulns(), addVuln)})

    app = QApplication([])  # as we don't use arguments, I prefer to use python-fire
    window = Window('Repator', tabLst)

    # this allows us to have a directory for every mission with a file that can be automatically configured
    # then, just use repator.py --conf=path or repator.py path (or nothing to use default)
    if conf is not None:
        if path.exists(conf):
            config = ConfigParser()
            config.optionxform = str
            config.read(conf)
            window.loadDict({s: dict(config.items(s)) for s in config.sections()})
        else:
            window.loadDict({})
    window.showMaximized()

    app.exec_()


if __name__ == "__main__":
    fire.Fire(main)
