# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 15:32:38 2019

@author: jeromlu2
"""

__version__ = "1.0.0"

# **************************Pure python imports***********************************
import sys
import time
import random

# **************************Third party imports***********************************
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy, QPushButton, QDialog, QVBoxLayout, QFrame
from PyQt5.QtWidgets import QComboBox, QProgressBar, QMessageBox

from PyQt5.QtGui import QImage, QIcon, QPixmap

from PyQt5.QtCore import QSize, Qt, QTimer, QThread, pyqtSignal

# **************************Local imports*****************************************
from amino_acids.AA_data_structure import AminoAcids
from amino_acids.settings_dialog import SettingsDialog
from amino_acids import qrc_resources
from amino_acids import utils
from amino_acids.exercise_thread import ExerciseThread


class AminoAcidsUI(QMainWindow):
    def __init__(self, parent=None):
        super(AminoAcidsUI, self).__init__(parent)

        # data initialization
        self.amino_acids = AminoAcids()
        self.amino_acids.load_data()
        self.current_AA_idx = None
        self.indices = []
        self.amino_acid = None
        self.settings = {
            "show_only": "Letter_label",
            "seconds": 45,  # "inf",
            "AA_repetition": True,  # se ne dela
            "AA_num_to_test": 2,
        }

        # UI initialization
        self.create_main_window()

        # secon thread
        self.exer_thread = ExerciseThread(self)

        # connections
        # secondary thread connections
        self.exer_thread.new_AA.connect(self.show_next_rnd_AA)
        self.exer_thread.new_AA.connect(self.update_AA_progress_bar)
        self.exer_thread.answer_AA.connect(self.show_answer_of_AA)
        self.exer_thread.update_time_pb.connect(self.update_time_progress_bar)
        self.exer_thread.finished.connect(self.exercise_thread_finished)
        # other connections
        self.btn_end.clicked.connect(self.on_btn_end)
        self.combo_AA_list.currentTextChanged.connect(self.populate_UI_w_AA_info)
        self.btn_next.clicked.connect(self.show_next_rnd_AA)
        self.btn_start.clicked.connect(self.start_full_test)
        # self.btn_end.clicked.connect(self.show_image)
        self.btn_show_sol.clicked.connect(self.show_answer_of_AA)
        self.btn_settings.clicked.connect(self.set_settings)

    def create_main_window(self):

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # figure of skeletal formula of AA
        self.label_AA = QLabel("Amino acid info")
        self.label_AA.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.label_AA.setMinimumWidth(300)
        style_sheet = """
        QLabel { background-color : white; color : black; font: 16px;}"""
        self.label_AA.setStyleSheet(style_sheet)
        # self.label_AA.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.image_label_AA = QLabel("Skeletal formula")
        self.image_label_AA.setMinimumSize(270, 540)
        self.image_label_AA.setAlignment(Qt.AlignCenter)

        # create buttons
        self.btn_start = QPushButton("Start")
        self.btn_end = QPushButton("End")
        self.btn_end.setEnabled(False)
        self.btn_next = QPushButton("Next")
        self.btn_show_sol = QPushButton("Answer")
        self.btn_settings = QPushButton("Settings")

        # spinbox for selecting the amino acid
        self.combo_AA_list = QComboBox()
        self.combo_AA_list.addItem("")
        self.combo_AA_list.addItems(self.amino_acids.get_AA_names())
        self.AA_pb = QProgressBar()
        self.AA_pb.setValue(0)
        self.AA_pb.setMaximum(self.settings["AA_num_to_test"])
        self.AA_pb.setFormat("0/{}".format(self.settings["AA_num_to_test"]))
        self.timer_pb = QProgressBar()
        self.timer_pb.setValue(0)
        self.timer_pb.setMaximum(self.settings["seconds"])
        self.timer_pb.setFormat("  0/{:3} s".format(self.settings["seconds"]))
        # self.timer_pb.setFormat("12")
        print("  0/{:3} s".format(self.settings["seconds"]))

        pb_vbox = QVBoxLayout()
        pb_vbox.addWidget(self.AA_pb)
        pb_vbox.addWidget(self.timer_pb)

        combo_hbox = QHBoxLayout()
        combo_hbox.addWidget(self.combo_AA_list)
        combo_hbox.addLayout(pb_vbox)
        # combo_hbox.addStretch(1)

        button_hbox = QHBoxLayout()
        button_hbox.addWidget(self.btn_start)
        button_hbox.addWidget(self.btn_end)
        button_hbox.addWidget(self.btn_next)
        button_hbox.addWidget(self.btn_show_sol)
        button_hbox.addWidget(self.btn_settings)
        button_hbox.addStretch(1)

        main_hbox = QHBoxLayout()
        main_hbox.addWidget(self.label_AA)
        main_hbox.addWidget(self.image_label_AA)

        vbox = QVBoxLayout()
        vbox.addLayout(combo_hbox)
        vbox.addLayout(main_hbox)
        vbox.addLayout(button_hbox)

        self.main_widget.setLayout(vbox)

        # self.statusBar().showMessage('Ready')

        self.setWindowTitle("Amino acids tool")

    def start_full_test(self):
        try:
            self.indices = random.sample(
                range(1, len(self.amino_acids)),
                self.settings["AA_num_to_test"],  # len(self.amino_acids) - 1
            )
            # print(self.indices)
            self.btn_end.setEnabled(True)
            self.btn_start.setEnabled(False)
            # self.btn_next.setEnabled(False)
            self.btn_show_sol.setEnabled(False)
            self.btn_settings.setEnabled(True)
            self.timer_pb.setValue(0)
            self.timer_pb.setFormat("  0/{:3} s".format(self.settings["seconds"]))
            self.AA_pb.setValue(0)
            self.AA_pb.setFormat(
                "{}/{}".format(self.AA_pb.value(), self.settings["AA_num_to_test"])
            )
            # print(self.settings["seconds"], "  s")
            self.timer_pb.setMaximum(self.settings["seconds"])
            self.exer_thread.initialize(self.indices, self.settings["seconds"])
            self.btn_next.clicked.disconnect()
            self.btn_next.clicked.connect(self.on_btn_nxt_during_thread)
            # print("before start")
            self.exer_thread.start()
        except Exception:
            utils.print_err()

    def on_btn_nxt_during_thread(self):
        try:
            # self.exer_thread.new_AA.emit()
            self.remove_index()
        except Exception:
            utils.print_err()

    def on_btn_end(self):
        if self.exer_thread.isRunning():
            self.exer_thread.stop()
            self.exercise_thread_finished()
        else:
            print("not running")

    def remove_index(self):
        if len(self.indices) > 0:
            self.show_next_rnd_AA(self.indices.pop(0))
            self.update_AA_progress_bar()
        else:
            self.exercise_thread_finished()

    def exercise_thread_finished(self):
        print("finished wait")
        self.exer_thread.wait()
        print("finished")
        self.btn_end.setEnabled(False)
        self.btn_start.setEnabled(True)
        self.btn_next.setEnabled(True)
        self.btn_show_sol.setEnabled(True)
        self.btn_settings.setEnabled(True)
        self.AA_pb.setValue(0)
        self.AA_pb.setFormat("0/{}".format(self.settings["AA_num_to_test"]))
        self.timer_pb.setValue(0)
        self.timer_pb.setFormat("  0/{:3} s".format(self.settings["seconds"]))
        if self.exer_thread.completed:
            QMessageBox.information(
                self, "Congratulations!", "You have completed whole exercise set."
            )
        self.btn_next.clicked.disconnect()
        self.btn_next.clicked.connect(self.show_next_rnd_AA)

    def show_next_rnd_AA(self, idx="rnd"):
        self.timer_pb.setValue(0)
        if idx == False:
            idx = "rnd"
        if not self.select_AA(idx):  # selects random amino acid
            print("No AA was selected, error in show_next_rnd_AA!")
            return

        if self.settings["show_only"] == "Skeletal_formula":
            self.show_image(True)
            self.update_info_text(False)
        else:
            self.show_image(False)
            self.update_info_text(False)
        self.combo_AA_list.setEnabled(False)  # disable comboBox
        if self.combo_AA_list.currentIndex() != 0:
            self.current_AA_idx = self.combo_AA_list.currentIndex()
        self.combo_AA_list.blockSignals(True)
        self.combo_AA_list.setCurrentIndex(0)
        # print("idx ", self.current_AA_idx)

    def show_answer_of_AA(self):
        # print("idx ", self.current_AA_idx)
        if self.current_AA_idx:
            self.combo_AA_list.setCurrentIndex(self.current_AA_idx)
            self.show_image(True)
            self.update_info_text()
        else:
            print("No amino acid.")
        self.combo_AA_list.setEnabled(True)
        self.combo_AA_list.blockSignals(False)

    def select_AA(self, idx="rnd"):
        """Selects amino acid by:
            - random
            - index
            - from combo box name
        """
        # print("select AA ", idx)
        if isinstance(idx, int):
            if idx > self.combo_AA_list.count():
                print("index out of range")
                return False
            self.current_AA_idx = idx
            self.combo_AA_list.setCurrentIndex(idx)
        elif isinstance(idx, str):
            if idx == "rnd":
                self.current_AA_idx = random.randint(1, len(self.amino_acids) - 1)
                self.combo_AA_list.setCurrentIndex(self.current_AA_idx)
                # print("idx ", self.current_AA_idx)
            else:
                self.current_AA_idx = self.combo_AA_list.currentIndex()

        AA_name = self.combo_AA_list.currentText()
        self.amino_acid = self.amino_acids.get_AA(AA_name)
        if self.amino_acid == None or self.amino_acid.skeletal_formula == None:
            print("No AA was selected, error in select_AA!")
            return False
        return True

    def populate_UI_w_AA_info(self):

        if not self.select_AA("from_combo_box"):
            print("No AA was selected, error in populate_UI_w_AA_info!")
            return
        self.show_image(True)
        self.update_info_text(True)

    def show_image(self, show=True):
        # print(show, self.amino_acid)
        if show and self.amino_acid:
            image = self.amino_acid.skeletal_formula
            self.image_label_AA.setPixmap(QPixmap.fromImage(image))
        else:
            self.image_label_AA.clear()

    def update_info_text(self, update_all=True):

        lst_info = [
            self.amino_acid.name,
            self.amino_acid.short_label,
            self.amino_acid.one_letter_label,
            self.amino_acid.MW,
            self.amino_acid.pI,
            self.amino_acid.pKa1,
            self.amino_acid.pKa2,
            self.amino_acid.pKa,
            self.amino_acid.hydropathy_idx,
            self.amino_acid.classification,
            self.amino_acid.side_chain,
        ]
        lst = ["???"] * len(lst_info)
        if self.settings["show_only"] == "Letter_label":
            lst[2] = lst_info[2]
        elif self.settings["show_only"] == "Short_label":
            lst[1] = lst_info[1]
        elif self.settings["show_only"] == "AA_name":
            lst[0] = lst_info[0]

        if update_all == True:
            txt = """
        Name: {0}\n
        Short name: {1}\n
        Letter label: {2}\n
        Molecular weight: {3:.2f} g/mol\n
        Isoelectric point: {4}\n
        pKa1 (COOH): {5}\n
        pKa2 (NH2):: {6}\n
        pKa side_chain: {7}\n
        Hydropathy index: {8}\n
        Class: {9}\n
        Side chain: {10}\n
            """
            self.label_AA.setText(txt.format(*lst_info))
        else:
            txt = """
        Name: {0}\n
        Short name: {1}\n
        Letter label: {2}\n
        Molecular weight: {3} g/mol\n
        Isoelectric point: {4}\n
        pKa1 (COOH): {5}\n
        pKa2 (NH2): {6}\n
        pKa side_chain: {7}
        Hydropathy index: {8}\n
        Class: {9}\n
        Side chain: {10}\n
            """
            self.label_AA.setText(txt.format(*lst))

    def update_AA_progress_bar(self):
        value = self.AA_pb.value() + 1
        self.AA_pb.setValue(value)
        self.AA_pb.setFormat("{}/{}".format(value, self.settings["AA_num_to_test"]))

    def update_time_progress_bar(self):
        value = self.timer_pb.value() + 1
        self.timer_pb.setValue(value)
        self.timer_pb.setFormat("{:3}/{:3} s".format(value, self.settings["seconds"]))

    def set_settings(self):
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_():
            try:
                self.settings = dialog.settings
                self.AA_pb.setFormat("0/{}".format(self.settings["AA_num_to_test"]))
                self.AA_pb.setMaximum(self.settings["AA_num_to_test"])
                self.timer_pb.setFormat("  0/{:3} s".format(self.settings["seconds"]))
                self.timer_pb.setMaximum(self.settings["seconds"])
            except Exception:
                utils.print_err()

    def closeEvent(self, evt):
        self.exer_thread.stop()
        self.exer_thread.wait()


if __name__ == "__main__":

    def run_app():
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(":/main_window_icon.png"))
        main_frame = AminoAcidsUI()
        main_frame.show()
        app.exec_()

    run_app()
