#
# Created on Sun May 17 2020
#
# Copyright (c) 2020 Your Company
# Name: Luka Jeromel
#
# ******************************Python imports***********************************
# ******************************PyQt5 imports*************************************
from PyQt5.QtCore import pyqtSignal, QThread, QMutex

# ******************************Other third party imports************************
# ******************************My modules***************************************


class ExerciseThread(QThread):

    new_AA = pyqtSignal(int)
    answer_AA = pyqtSignal()
    update_time_pb = pyqtSignal()
    finished = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ExerciseThread, self).__init__(parent)
        self.indices = []
        self.time_sec = 10
        self.answer_time_sec = 10
        self.stopped = False
        self.completed = False
        self.mutex = QMutex()

    def initialize(self, lst_of_idx, time_sec, answer_time_sec=10):
        self.stopped = False
        self.indices = lst_of_idx
        self.time_sec = time_sec
        self.answer_time_sec = answer_time_sec
        self.completed = False

    def run(self):

        for idx in self.indices:
            if self.is_stopped():
                return
            self.new_AA.emit(idx)
            for i in range(self.time_sec):
                if self.is_stopped():
                    return
                self.update_time_pb.emit()
                self.sleep(1)
            if self.is_stopped():
                return
            self.answer_AA.emit()
            # to review the result
            # TODO move 5 to options that can be set
            self.parent.timer_pb.seValue(0)
            for j in range(self.answer_time_sec):
                if self.is_stopped():
                    return
                self.update_time_pb.emit()
                self.sleep(1)
        self.completed = True
        self.stop()
        self.finished.emit(self.completed)

    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def is_stopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()
