
__version__ = "1.0.0"

import sys

from PyQt5.QtWidgets import QApplication

import qrc_resources

if __name__ == '__main__':
    def run_app():
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(":/main_window_icon.png"))
        main_frame = AminoAcidsUI()
        main_frame.show()
        app.exec_()
    run_app()
