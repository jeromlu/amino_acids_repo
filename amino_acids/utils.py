#
# Created on Thu May 07 2020
#
# Copyright (c) 2020 Your Company
# Name: Luka Jeromel
#
# ******************************Python imports***********************************
import os
import sys

# ******************************PyQt5 imports*************************************
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

# ******************************Other third party imports************************
# ******************************My modules***************************************


def add_actions(target, actions):
    for action in actions:
        if action is None:
            target.addSeparator()
        else:
            target.addAction(action)


def create_action(
    text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, parent=None
):
    action = QAction(text, parent)
    if icon is not None:
        action.setIcon(QIcon(":/{}.png".format(icon)))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        action.triggered.connect(slot)
    if checkable:
        action.setCheckable(True)
    return action


def print_err():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    err_msg = "{0}:\n{1}\nError occurred in fle: {2}\n at line: {3}".format(
        exc_type, exc_obj, fname, exc_tb.tb_lineno
    )
    print(err_msg)
