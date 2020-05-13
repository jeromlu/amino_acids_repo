
__version__ = "1.0.0"

import sys

from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QIcon

from amino_acids.amino_acids import AminoAcidsUI
import qrc_resources

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/main_window_icon.png"))
    main_frame = AminoAcidsUI()
    main_frame.show()
    app.exec_()

if __name__ == '__main__':
    main()
