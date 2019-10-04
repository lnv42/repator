"""Defines the UI for the diferrences tabs in Diffs window."""

# coding=utf-8

import collections

from PyQt5.QtWidgets import QLabel, QComboBox

from conf.report import BLUE, RED, GREEN


def vuln_changes(doc_id, vuln1, vuln2, style, lang=""):
    """Adds a the arguments to construct a differences tab given later to src.ui.tab.parseLst"""
    if style == BLUE:
        status = "Modified"
    elif style == RED:
        status = "Removed"
    elif style == GREEN:
        status = "Added"

    # To avoid the crash when editing a new vuln or a partial vuln loaded from
    # db.
    if not vuln1:
        vuln1 = dict()
    if not vuln2:
        vuln2 = dict()
    vuln1 = collections.defaultdict(lambda: "", vuln1)
    vuln2 = collections.defaultdict(lambda: "", vuln2)

    lst = collections.OrderedDict()

    lst["id-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "ID  " + str(doc_id),
        "col": 0
    }
    lst["status"] = {
        "class": QLabel,
        "arg": status,
        "col": 1
    }

    lst["category" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Category",
        "col": 0}
    lst["category" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QLabel,
        "arg": vuln1["category"+lang] if "category"+lang in vuln1 else (
            "" if "category"+lang in vuln2 else vuln1["category"]),
        "col": 1,
        "colspan": 4}
    lst["category" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QLabel,
        "arg": vuln2["category"+lang] if "category"+lang in vuln2 else (
            "" if "category"+lang in vuln1 else vuln2["category"]),
        "col": 5,
        "colspan": 4}

    lst["sub_category" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Sub Category",
        "col": 0}
    lst["sub_category" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QLabel,
        "arg": vuln1["sub_category"+lang] if "sub_category"+lang in vuln1 else (
            vuln1["sub_category"]),
        "col": 1,
        "colspan": 4}
    lst["sub_category" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QLabel,
        "arg": vuln2["sub_category"+lang] if "sub_category"+lang in vuln2 else (
            vuln2["sub_category"]),
        "col": 5,
        "colspan": 4}

    lst["name" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Vulnerability",
        "col": 0}
    lst["name" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QLabel,
        "arg": vuln1["name"+lang] if "name"+lang in vuln1 else vuln1["name"],
        "col": 1,
        "colspan": 4}
    lst["name" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QLabel,
        "arg": vuln2["name"+lang] if "name"+lang in vuln2 else vuln2["name"],
        "col": 5,
        "colspan": 4}

    lst["labelNeg" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Negative Label",
        "col": 0}
    lst["labelNeg" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QLabel,
        "arg": vuln1["labelNeg"+lang] if "labelNeg"+lang in vuln1 else vuln1["labelNeg"],
        "col": 1,
        "colspan": 4}
    lst["labelNeg" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QLabel,
        "arg": vuln2["labelNeg"+lang] if "labelNeg"+lang in vuln2 else vuln2["labelNeg"],
        "col": 5,
        "colspan": 4}

    lst["labelPos" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Positive Label",
        "col": 0}
    lst["labelPos" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QLabel,
        "arg": vuln1["labelPos"+lang] if "labelPos"+lang in vuln1 else vuln1["labelPos"],
        "col": 1,
        "colspan": 4}
    lst["labelPos" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QLabel,
        "arg": vuln2["labelPos"+lang] if "labelPos"+lang in vuln2 else vuln2["labelPos"],
        "col": 5,
        "colspan": 4}

    lst["observPosHistory" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Positive Observation History",
        "col": 0}
    lst["observPosHistory" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QComboBox,
        "signal": "currentIndexChanged",
        "signalFct": "update_history",
        "items": list(map(lambda x: x.replace('\n', ' ')[:50], vuln1["observPosHistory"+lang])) if (
            "observPosHistory"+lang in vuln1) else (
                list(map(lambda x: x.replace(
                    '\n', ' ')[:50], vuln1["observPosHistory"]))),
        "col": 1,
        "colspan": 4,
        "setLength": 50}
    lst["observPosHistory" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QComboBox,
        "signal": "currentIndexChanged",
        "signalFct": "update_history",
        "items": list(map(lambda x: x.replace('\n', ' ')[:50], vuln2["observPosHistory"+lang])) if (
            "observPosHistory"+lang in vuln2) else (
                list(map(lambda x: x.replace(
                    '\n', ' ')[:50], vuln2["observPosHistory"]))),
        "col": 5,
        "colspan": 4,
        "setLength": 50}

    lst["observPos" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Positive Observation",
        "col": 0}
    lst["observPos" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QLabel,
        "arg": vuln1["observPos"+lang].replace("\n", "<br/>") if "observPos"+lang in vuln1 else (
            vuln1["observPos"].replace("\n", "<br/>")),
        "col": 1,
        "colspan": 4}
    lst["observPos" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QLabel,
        "arg": vuln2["observPos"+lang].replace("\n", "<br/>") if "observPos"+lang in vuln2 else (
            vuln2["observPos"].replace("\n", "<br/>")),
        "col": 5,
        "colspan": 4}

    lst["observNegHistory" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Negative Observation History",
        "col": 0}
    lst["observNegHistory" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QComboBox,
        "signal": "currentIndexChanged",
        "signalFct": "update_history",
        "items": list(map(lambda x: x.replace('\n', ' ')[:50], vuln1["observNegHistory"+lang])) if (
            "observNegHistory"+lang in vuln1) else (
                list(map(lambda x: x.replace(
                    '\n', ' ')[:50], vuln1["observNegHistory"]))),
        "col": 1,
        "colspan": 4,
        "setLength": 50}
    lst["observNegHistory" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QComboBox,
        "signal": "currentIndexChanged",
        "signalFct": "update_history",
        "items": list(map(lambda x: x.replace('\n', ' ')[:50], vuln2["observNegHistory"+lang])) if (
            "observNegHistory"+lang in vuln2) else (
                list(map(lambda x: x.replace(
                    '\n', ' ')[:50], vuln2["observNegHistory"]))),
        "col": 5,
        "colspan": 4,
        "setLength": 50}

    lst["observNeg" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Negative Observation",
        "col": 0}
    lst["observNeg" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QLabel,
        "arg": vuln1["observNeg"+lang].replace("\n", "<br/>") if "observNeg"+lang in vuln1 else (
            vuln1["observNeg"].replace("\n", "<br/>")),
        "col": 1,
        "colspan": 4}
    lst["observNeg" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QLabel,
        "arg": vuln2["observNeg"+lang].replace("\n", "<br/>") if "observNeg"+lang in vuln2 else (
            vuln2["observNeg"].replace("\n", "<br/>")),
        "col": 5,
        "colspan": 4}

    lst["riskHistory" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Risk History",
        "col": 0}
    lst["riskHistory" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QComboBox,
        "signal": "currentIndexChanged",
        "signalFct": "update_history",
        "items": list(map(lambda x: x.replace('\n', ' ')[:50], vuln1["riskHistory"+lang])) if (
            "riskHistory"+lang in vuln1) else (
                list(map(lambda x: x.replace(
                    '\n', ' ')[:50], vuln1["riskHistory"]))),
        "col": 1,
        "colspan": 4,
        "setLength": 50}
    lst["riskHistory" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QComboBox,
        "signal": "currentIndexChanged",
        "signalFct": "update_history",
        "items": list(map(lambda x: x.replace('\n', ' ')[:50], vuln2["riskHistory"+lang])) if (
            "riskHistory"+lang in vuln2) else (
                list(map(lambda x: x.replace(
                    '\n', ' ')[:50], vuln2["riskHistory"]))),
        "col": 5,
        "colspan": 4,
        "setLength": 50}

    lst["risk" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Risk",
        "col": 0}
    lst["risk" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QLabel,
        "arg": vuln1["risk"+lang].replace("\n", "<br/>") if "risk"+lang in vuln1 else (
            vuln1["risk"].replace("\n", "<br/>")),
        "col": 1,
        "colspan": 4}
    lst["risk" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QLabel,
        "arg": vuln2["risk"+lang].replace("\n", "<br/>") if "risk"+lang in vuln2 else (
            vuln2["risk"].replace("\n", "<br/>")),
        "col": 5,
        "colspan": 4}

    lst["recoHistory" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Recommandation History",
        "col": 0}
    lst["recoHistory" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QComboBox,
        "signal": "currentIndexChanged",
        "signalFct": "update_history",
        "items": list(map(lambda x: x.replace('\n', ' ')[:50], vuln1["recoHistory"+lang])) if (
            "recoHistory"+lang in vuln1) else (
                list(map(lambda x: x.replace(
                    '\n', ' ')[:50], vuln1["recoHistory"]))),
        "col": 1,
        "colspan": 4,
        "setLength": 50}
    lst["recoHistory" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QComboBox,
        "signal": "currentIndexChanged",
        "signalFct": "update_history",
        "items": list(map(lambda x: x.replace('\n', ' ')[:50], vuln2["recoHistory"+lang])) if (
            "recoHistory"+lang in vuln2) else (
                list(map(lambda x: x.replace(
                    '\n', ' ')[:50], vuln2["recoHistory"]))),
        "col": 5,
        "colspan": 4,
        "setLength": 50}

    lst["reco" + lang + "-" + str(doc_id)] = {
        "class": QLabel,
        "arg": "Recommandation",
        "col": 0}
    lst["reco" + lang + "-" + str(doc_id) + "-1"] = {
        "class": QLabel,
        "arg": vuln1["reco"+lang].replace("\n", "<br/>") if "reco"+lang in vuln1 else (
            vuln1["reco"].replace("\n", "<br/>")),
        "col": 1,
        "colspan": 4}
    lst["reco" + lang + "-" + str(doc_id) + "-2"] = {
        "class": QLabel,
        "arg": vuln2["reco"+lang].replace("\n", "<br/>") if "reco"+lang in vuln2 else (
            vuln2["reco"].replace("\n", "<br/>")),
        "col": 5,
        "colspan": 4}

    lst["CVSSLabel"] = {"class": QLabel,
                        "arg": "CVSSv3 metrics",
                        "col": 0}
    lst["AV0-1" + "-" + str(doc_id)] = {"class": QLabel,
                                        "arg": "Attack Vector",
                                        "col": 1}
    lst["AC0-1" + "-" + str(doc_id)] = {"class": QLabel,
                                        "arg": "Attack Complexity",
                                        "col": 2}
    lst["PR0-1" + "-" + str(doc_id)] = {"class": QLabel,
                                        "arg": "Privileges Required",
                                        "col": 3}
    lst["UI0-1" + "-" + str(doc_id)] = {"class": QLabel,
                                        "arg": "User Interaction",
                                        "col": 4}
    lst["AV0-2" + "-" + str(doc_id)] = {"class": QLabel,
                                        "arg": "Attack Vector",
                                        "col": 5}
    lst["AC0-2" + "-" + str(doc_id)] = {"class": QLabel,
                                        "arg": "Attack Complexity",
                                        "col": 6}
    lst["PR0-2" + "-" + str(doc_id)] = {"class": QLabel,
                                        "arg": "Privileges Required",
                                        "col": 7}
    lst["UI0-2" + "-" + str(doc_id)] = {"class": QLabel,
                                        "arg": "User Interaction",
                                        "col": 8}

    lst["CVSSLine2"] = {"class": QLabel,
                        "col": 0}
    lst["AV-" + str(doc_id) + "-1"] = {"class": QLabel,
                                       "setText": vuln1["AV"],
                                       "col": 1}
    lst["AC-" + str(doc_id) + "-1"] = {"class": QLabel,
                                       "setText": vuln1["AC"],
                                       "col": 2}
    lst["PR-" + str(doc_id) + "-1"] = {"class": QLabel,
                                       "setText": vuln1["PR"],
                                       "col": 3}
    lst["UI-" + str(doc_id) + "-1"] = {"class": QLabel,
                                       "setText": vuln1["UI"],
                                       "col": 4}
    lst["AV-" + str(doc_id) + "-2"] = {"class": QLabel,
                                       "setText": vuln2["AV"],
                                       "col": 5}
    lst["AC-" + str(doc_id) + "-2"] = {"class": QLabel,
                                       "setText": vuln2["AC"],
                                       "col": 6}
    lst["PR-" + str(doc_id) + "-2"] = {"class": QLabel,
                                       "setText": vuln2["PR"],
                                       "col": 7}
    lst["UI-" + str(doc_id) + "-2"] = {"class": QLabel,
                                       "setText": vuln2["UI"],
                                       "col": 8}

    lst["CVSSLine3"] = {"class": QLabel,
                        "col": 0}
    lst["S0-" + str(doc_id) + "-1"] = {"class": QLabel,
                                       "arg": "Scope",
                                       "col": 1}
    lst["C0-" + str(doc_id) + "-1"] = {"class": QLabel,
                                       "arg": "Confidentiality",
                                       "col": 2}
    lst["I0-" + str(doc_id) + "-1"] = {"class": QLabel,
                                       "arg": "Integrity",
                                       "col": 3}
    lst["A0-" + str(doc_id) + "-1"] = {"class": QLabel,
                                       "arg": "Availability",
                                       "col": 4}
    lst["S0-" + str(doc_id) + "-2"] = {"class": QLabel,
                                       "arg": "Scope",
                                       "col": 5}
    lst["C0-" + str(doc_id) + "-2"] = {"class": QLabel,
                                       "arg": "Confidentiality",
                                       "col": 6}
    lst["I0-" + str(doc_id) + "-2"] = {"class": QLabel,
                                       "arg": "Integrity",
                                       "col": 7}
    lst["A0-" + str(doc_id) + "-2"] = {"class": QLabel,
                                       "arg": "Availability",
                                       "col": 8}
    lst["CVSSLine4"] = {"class": QLabel,
                        "col": 0}
    lst["S-" + str(doc_id) + "-1"] = {"class": QLabel,
                                      "setText": vuln1["S"],
                                      "col": 1}
    lst["C-" + str(doc_id) + "-1"] = {"class": QLabel,
                                      "setText": vuln1["C"],
                                      "col": 2}
    lst["I-" + str(doc_id) + "-1"] = {"class": QLabel,
                                      "setText": vuln1["I"],
                                      "col": 3}
    lst["A-" + str(doc_id) + "-1"] = {"class": QLabel,
                                      "setText": vuln1["A"],
                                      "col": 4}
    lst["S-" + str(doc_id) + "-2"] = {"class": QLabel,
                                      "setText": vuln2["S"],
                                      "col": 5}
    lst["C-" + str(doc_id) + "-2"] = {"class": QLabel,
                                      "setText": vuln2["C"],
                                      "col": 6}
    lst["I-" + str(doc_id) + "-2"] = {"class": QLabel,
                                      "setText": vuln2["I"],
                                      "col": 7}
    lst["A-" + str(doc_id) + "-2"] = {"class": QLabel,
                                      "setText": vuln2["A"],
                                      "col": 8}

    lst["CVSSScoreLabel"] = {"class": QLabel,
                             "arg": "CVSSv3 score",
                             "col": 0}
    lst["CVSS11" + str(doc_id) + "-1"] = {"class": QLabel,
                                          "arg": "Base score",
                                          "col": 1}
    lst["CVSS12" + str(doc_id) + "-1"] = {"class": QLabel,
                                          "arg": "Impact score",
                                          "col": 2}
    lst["CVSS13" + str(doc_id) + "-1"] = {"class": QLabel,
                                          "arg": "Exploitability score",
                                          "col": 3}

    lst["CVSS11" + str(doc_id) + "-2"] = {"class": QLabel,
                                          "arg": "Base score",
                                          "col": 5}
    lst["CVSS12" + str(doc_id) + "-2"] = {"class": QLabel,
                                          "arg": "Impact score",
                                          "col": 6}
    lst["CVSS13" + str(doc_id) + "-2"] = {"class": QLabel,
                                          "arg": "Exploitability score",
                                          "col": 7}

    lst["CVSS2"] = {"class": QLabel,
                    "col": 0}
    lst["CVSS-" + str(doc_id) + "-1"] = {"class": QLabel,
                                         "col": 1}
    lst["CVSSimp-" + str(doc_id) + "-1"] = {"class": QLabel,
                                            "col": 2}
    lst["CVSSexp-" + str(doc_id) + "-1"] = {"class": QLabel,
                                            "col": 3}
    lst["CVSS-" + str(doc_id) + "-2"] = {"class": QLabel,
                                         "col": 5}
    lst["CVSSimp-" + str(doc_id) + "-2"] = {"class": QLabel,
                                            "col": 6}
    lst["CVSSexp-" + str(doc_id) + "-2"] = {"class": QLabel,
                                            "col": 7}

    lst["CVSSRiskLabel"] = {"class": QLabel,
                            "arg": "Risk analysis",
                            "col": 0}
    lst["CVSS31" + str(doc_id) + "-1"] = {"class": QLabel,
                                          "arg": "Risk level",
                                          "col": 1}
    lst["CVSS32" + str(doc_id) + "-1"] = {"class": QLabel,
                                          "arg": "Impact level",
                                          "col": 2}
    lst["CVSS33" + str(doc_id) + "-1"] = {"class": QLabel,
                                          "arg": "Exploitability level",
                                          "col": 3}
    lst["CVSS31" + str(doc_id) + "-2"] = {"class": QLabel,
                                          "arg": "Risk level",
                                          "col": 5}
    lst["CVSS32" + str(doc_id) + "-2"] = {"class": QLabel,
                                          "arg": "Impact level",
                                          "col": 6}
    lst["CVSS33" + str(doc_id) + "-2"] = {"class": QLabel,
                                          "arg": "Exploitability level",
                                          "col": 7}

    lst["CVSS4"] = {"class": QLabel,
                    "col": 0}
    lst["riskLvl-" + str(doc_id) + "-1"] = {"class": QLabel,
                                            "col": 1}
    lst["impLvl-" + str(doc_id) + "-1"] = {"class": QLabel,
                                           "col": 2}
    lst["expLvl-" + str(doc_id) + "-1"] = {"class": QLabel,
                                           "col": 3}
    lst["riskLvl-" + str(doc_id) + "-2"] = {"class": QLabel,
                                            "col": 5}
    lst["impLvl-" + str(doc_id) + "-2"] = {"class": QLabel,
                                           "col": 6}
    lst["expLvl-" + str(doc_id) + "-2"] = {"class": QLabel,
                                           "col": 7}

    return lst
