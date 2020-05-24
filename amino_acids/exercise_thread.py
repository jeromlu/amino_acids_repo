#
# Created on Sun May 17 2020
#
# Copyright (c) 2020 Your Company
# Name: Luka Jeromel
#
# ******************************Python imports***********************************
# ******************************PyQt5 imports*************************************
from PyQt5.QtCore import pyqtSignal, QThread

# ******************************Other third party imports************************
# ******************************My modules***************************************


class ExerciseThread(QThread):

    new_AA = pyqtSignal(int)
    answer_AA = pyqtSignal()
    update_time_pb = pyqtSignal()

    def __init__(self, lst_of_idx, time_sec):
        super(ExerciseThread, self).__init__()
        self.indices = lst_of_idx
        self.time_sec = time_sec

    def __del__(self):
        print("Deleting thread.")
        self.wait()

    def run(self):
        for idx in self.indices:
            self.new_AA.emit(idx)
            for i in range(self.time_sec):
                self.sleep(1)
                self.update_time_pb.emit()
            self.answer_AA.emit()
            # to review the result
            # TODO move 5 to options that can be set
            self.sleep(5)
