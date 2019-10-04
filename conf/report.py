"""Defines global settings for report and git."""

# coding=utf-8

REPORT_TEMPLATE_DIR = "templates/"
REPORT_TEMPLATE_MAIN = "main.json"
REPORT_TEMPLATE_BASE = "template.docx"

REPORT_OUTPUT = "output.docx"

LANGUAGES = ["EN", "FR"]
# LANGUAGES = ["EN"]

GREEN = '#008000'
RED = '#ff0000'
BLUE = '#4169e1'
DEFAULT = '#000000'
COLORS = [BLUE, GREEN, RED, DEFAULT]
HEADERS = {"category", "sub_category", "name", "labelNeg", "labelPos"}
CVSS = {"AV", "AC", "PR", "UI", "S", "C", "I", "A"}
HISTORIES = {"reco", "observPos", "observNeg", "risk"}

GIT = "git@10.0.0.103:~/vulnerabilities.git"
SSH_KEY = "~/.ssh/git_tries"
REFRESH_RATE = 10
