"""Creation of the app repator and of git interactions."""

# coding=utf-8

from copy import copy
from os import path
from configparser import ConfigParser
from collections import OrderedDict
from shutil import copyfile
import fire
from PyQt5.QtWidgets import QApplication

from conf.ui_mission import MISSION
from conf.ui_auditors import PEOPLE, add_people
from conf.ui_vulns import VULNS, add_vuln
from src.dbhandler import DBHandler, DB_VULNS, DB_VULNS_INITIAL
from src.ui.window import Window
from src.ui.vulns import Vulns
from src.git_interactions import Git


def main(conf=None):
    """Creates the window repator, initializing the databases and the git repository."""
    tab_lst = OrderedDict()
    tab_lst["Mission"] = copy(MISSION)
    tab_lst["Auditors"] = dict(
        lst=copy(PEOPLE), db=DBHandler.auditors(), add_fct=add_people)
    tab_lst["Clients"] = dict(
        lst=copy(PEOPLE), db=DBHandler.clients(), add_fct=add_people)
    tab_lst["Vulns"] = dict(vulns={"class": Vulns, "arg": (
        copy(VULNS), DBHandler.vulns(), add_vuln)})

    copyfile(DB_VULNS, DB_VULNS_INITIAL)

    # as we don't use arguments, I prefer to use python-fire
    app = QApplication([])
    window = Window('Repator', tab_lst)
    Git()

    # this allows us to have a directory for every mission with a file that can
    # be automatically configured
    # then, just use repator.py --conf=path or repator.py path (or nothing to
    # use default)
    if conf is not None:
        if path.exists(conf):
            config = ConfigParser()
            config.optionxform = str
            config.read(conf)
            window.load_dict({s: dict(config.items(s))
                              for s in config.sections()})
        else:
            window.load_dict({})
    window.showMaximized()

    app.exec_()


if __name__ == "__main__":
    fire.Fire(main)
