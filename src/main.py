# coding=utf-8

from copy import copy
from sys import path
import configparser
import fire

from src.qtui import *


def main(conf=None):
    tabLst = collections.OrderedDict()
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
            config = configparser.ConfigParser()
            config.read(conf)
            # for a reason I can't explain dates are not parsed... any idea lnv42?
            window.loadDict({s: dict(config.items(s)) for s in config.sections()})
        else:
            window.loadDict({})
    # window.loadJson('{"Mission": {"dateStart": "lun. avr. 23 2018", "dateEnd": "ven. avr. 27 2018", "client":"feafe", '
    #                 '"environment": "pr\u00e9-production"}, "Auditors": {}, "Vulns": {"AV1": "P"}}')
    window.showMaximized()

    app.exec_()


if __name__ == "__main__":
    fire.Fire(main)
