import sys

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui.mian_rc import Ui_MainWindow


class Ui_Action_MainWindow(Ui_MainWindow):
    def __init__(self, window):
        super(Ui_Action_MainWindow, self).__init__()
        self.setupUi(window)
        self.setupAction()

    def setupAction(self):
        self.action_add.triggered.connect(lambda: self.openFile())

    def openFile(self):
        files, file_type = QFileDialog.getOpenFileNames(self.centralwidget, "打开文件", "", "exc(*.xlsx);;txt(*.txt)")
        print(files, file_type)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_Action_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
