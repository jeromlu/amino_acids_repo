# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 20:37:22 2019

@author: JEROMLU2
"""

# ****************************Pure python*****************************************
import sys

# ****************************Third party****************************************
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QBoxLayout
from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QDialogButtonBox
from PyQt5.QtWidgets import QCheckBox

from PyQt5.QtGui import QRegExpValidator

from PyQt5.QtCore import QRegExp

# Global constants
LEFT, ABOVE = range(2)


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super(SettingsDialog, self).__init__(parent)

        # data
        self.settings = settings

        # UI initialization
        self.create_dialog()
        self.setWindowTitle("Settings")

        # connections
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def create_dialog(self):

        # defines what to show, all information or just specific
        self.lle_time = LabelledLineEdit("Time you have for answer\nin seconds", ABOVE)
        self.lle_num_of_AAs = LabelledLineEdit("Number of aminoacids to test", ABOVE)
        rx = r"[0-9]{3}"
        reg_exp = QRegExp(rx)
        self.lle_time.line_edit.setValidator(QRegExpValidator(reg_exp))
        self.lle_time.line_edit.setText(str(self.settings["seconds"]))
        rx = r"[0-9]|1[0-9]|2[0-2]"
        reg_exp = QRegExp(rx)
        self.lle_num_of_AAs.line_edit.setValidator(QRegExpValidator(reg_exp))
        self.lle_num_of_AAs.line_edit.setText(str(self.settings["AA_num_to_test"]))
        self.lcb_show = LabelledComboBox("Show", ABOVE)
        show_options = ["AA_name", "Letter_label", "Short_label", "Skeletal_formula"]
        self.lcb_show.combo_box.addItems(show_options)
        self.lcb_show.combo_box.setCurrentText("Letter_label")

        self.repetition_cb = QCheckBox("No repetition of amino acids")
        self.repetition_cb.setChecked(self.settings["AA_repetition"])

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.lle_time)
        vbox.addWidget(self.lle_num_of_AAs)
        vbox.addWidget(self.lcb_show)
        vbox.addWidget(self.repetition_cb)
        vbox.addWidget(self.buttonBox)

    def accept(self):
        self.settings["show_only"] = self.lcb_show.combo_box.currentText()
        self.settings["seconds"] = int(self.lle_time.line_edit.text())
        self.settings["AA_repetition"] = self.repetition_cb.isChecked()
        self.settings["AA_num_to_test"] = int(self.lle_num_of_AAs.line_edit.text())
        QDialog.accept(self)


class LabelledLineEdit(QWidget):
    def __init__(self, labelText="", position=LEFT, parent=None):
        super(LabelledLineEdit, self).__init__(parent)
        self.label = QLabel(labelText)
        self.line_edit = QLineEdit()
        self.label.setBuddy(self.line_edit)
        layout = QBoxLayout(
            QBoxLayout.LeftToRight if position == LEFT else QBoxLayout.TopToBottom
        )
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)


class LabelledComboBox(QWidget):
    def __init__(self, labelText="", position=LEFT, parent=None):
        super(LabelledComboBox, self).__init__(parent)
        self.label = QLabel(labelText)
        self.combo_box = QComboBox()
        self.label.setBuddy(self.combo_box)
        layout = QBoxLayout(
            QBoxLayout.LeftToRight if position == LEFT else QBoxLayout.TopToBottom
        )
        layout.addWidget(self.label)
        layout.addWidget(self.combo_box)
        self.setLayout(layout)


if __name__ == "__main__":

    settings = {
        "show_only": "All",
        "seconds": 30,
        "AA_repetition": True,
        "AA_num_to_test": 10,
    }

    def run_app():
        app = QApplication(sys.argv)

        dialog = SettingsDialog(settings)
        dialog.show()
        app.exec_()

    run_app()
