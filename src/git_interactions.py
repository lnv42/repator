"""Defines Git class, a helper to use Git."""
# coding=utf-8

from subprocess import Popen, PIPE
from re import findall
import json
import time
from threading import Thread
from shutil import copyfile
from PyQt5.QtCore import QCoreApplication, QObject
from conf.db import DB_VULNS_GIT, DB_VULNS_INITIAL, DB_VULNS_GIT_UPDATED
from conf.report import SSH_KEY, GIT, REFRESH_RATE


class Git(QObject):
    """Defines interactions between repator and git."""

    def __init__(self):
        super().__init__()
        self.dismiss_changes = False
        self.git_reachable = False
        self.init_git()
        self.app = QCoreApplication.instance()
        self.setParent(self.app)
        self.background_thread = Thread(
            target=self.timer_vulnerabilities, daemon=True)
        self.background_update = Thread(
            target=self.git_update, daemon=True)

    @staticmethod
    def execute_command(arg, cwd="."):
        """Executes the command arg in a subprocess with the option of setting the cwd."""
        process = Popen(arg, shell=True, cwd=cwd, stdout=PIPE, stderr=PIPE)
        res = process.communicate()
        for line in res:
            if line:
                result = line.decode('utf-8')
                err = findall("[eE][rR][rR][oO][rR]", result)
                fat = findall("fatal", result)
                if err or fat:
                    raise RuntimeError(result)

    def init_git(self):
        """Initialises the git repository in a new directory."""
        arg = "rm -rf .tmpGit"
        Git.execute_command(arg)
        arg = "mkdir .tmpGit"
        Git.execute_command(arg)
        args = []
        try:
            args.append("git init")
            args.append("git config core.sshCommand \"ssh -i " +
                        SSH_KEY + " -F /dev/null\"")
            args.append("git remote add origin " + GIT)
            for arg in args:
                self.execute_command(arg, "./.tmpGit")
        except RuntimeError as err:
            print(err)

    def clean_git(self):
        """Removes the git file (the thread doesn't need to be killed since it is deamonized)."""
        args = "rm -rf .tmpGit"
        self.execute_command(args)

    @staticmethod
    def vulnerabilities_changed():
        """Compares DB_VULNS_INITIAL and DB_VULNS_GIT"""
        json_db_initial = json.loads(
            open(DB_VULNS_INITIAL, 'r').read())["_default"]
        json_db_updated = json.loads(
            open(DB_VULNS_GIT, 'r').read())["_default"]
        return not json_db_updated == json_db_initial

    def git_update(self):
        """Pulls git repo and colors View changes button if the repository is unreachable."""
        arg = "git pull origin master"
        for window in self.app.topLevelWidgets():
            if window.windowTitle() == "Repator":
                repator = window
            elif window.windowTitle() == "Diffs":
                diffs = window
        try:
            process = Popen(arg, shell=True, cwd="./.tmpGit",
                            stdout=PIPE, stderr=PIPE)
            res = process.communicate()
            for line in res:
                if line:
                    result = line.decode('utf-8')
                    err = findall("[eE][rR][rR][oO][rR]", result)
                    fat = findall("fatal", result)
                    if err:
                        raise RuntimeError(result)
                    if fat:
                        raise RuntimeError(result)
            self.git_reachable = True
        except RuntimeError:
            self.git_reachable = False
            repator.layout().itemAt(3).widget().setStyleSheet(
                "QPushButton { background-color : grey }")
            diffs.layout().itemAt(0).widget().widget(0).widget.layout().itemAt(
                3).widget().setStyleSheet("QPushButton { background-color : grey }")

    @staticmethod
    def git_changed():
        """Compares DB_VULNS_GIT_UPDATED and DB_VULNS_GIT"""
        if DB_VULNS_GIT_UPDATED:
            json_db_initial = json.loads(
                open(DB_VULNS_GIT, 'r').read())["_default"]
            json_db_updated = json.loads(open(DB_VULNS_GIT_UPDATED, 'r').read())[
                "_default"]
            return json_db_updated != json_db_initial
        else:
            return False

    def timer_vulnerabilities(self):
        """Every REFRESH_RATE seconds, tries to update git."""
        repator = None
        diffs = None
        while True:
            self.git_update()
            for window in self.app.topLevelWidgets():
                if window.windowTitle() == "Repator":
                    repator = window
                elif window.windowTitle() == "Diffs":
                    diffs = window
            if self.git_reachable:
                Git.update_changes_button_colors(repator, diffs)
            time.sleep(REFRESH_RATE)

    @staticmethod
    def update_changes_button_colors(repator, diffs):
        """Updates View changes and refresh colors"""
        if not repator.dismiss_changes and Git.vulnerabilities_changed():
            if diffs and diffs.isVisible():
                if Git.git_changed():
                    diffs.layout().itemAt(0).widget().widget(0).widget.layout().itemAt(
                        3).widget().setStyleSheet("QPushButton { background-color : red }")
                else:
                    diffs.layout().itemAt(0).widget().widget(0).widget.layout().itemAt(
                        3).widget().setStyleSheet("QPushButton { background-color : light gray }")
            repator.layout().itemAt(3).widget().setStyleSheet(
                "QPushButton { background-color : red }")
        else:
            repator.layout().itemAt(3).widget().setStyleSheet(
                "QPushButton { background-color : light gray }")

    def refresh(self):
        """Updates git file and refreshes "Diffs" window"""
        if not self.background_update.isAlive():
            self.background_update = Thread(
                target=self.git_update, daemon=True)
            self.background_update.start()
        for window in self.app.topLevelWidgets():
            if window.windowTitle() == "Diffs" and self.git_reachable:
                copyfile(DB_VULNS_GIT_UPDATED, DB_VULNS_GIT)
                window.refresh_tab_widget()

    def git_routine(self):
        """Sets up the git subprocess"""
        self.init_git()
        self.background_thread.start()
