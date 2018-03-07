# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.filePathLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.filePathLineEdit.setGeometry(QtCore.QRect(230, 60, 351, 21))
        self.filePathLineEdit.setObjectName("filePathLineEdit")
        self.classifyButton = QtWidgets.QPushButton(self.centralwidget)
        self.classifyButton.setGeometry(QtCore.QRect(230, 400, 351, 41))
        self.classifyButton.setObjectName("classifyButton")
        self.loadFileButton = QtWidgets.QToolButton(self.centralwidget)
        self.loadFileButton.setGeometry(QtCore.QRect(590, 60, 24, 21))
        self.loadFileButton.setObjectName("loadFileButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 50, 111, 41))
        self.label.setObjectName("label")
        self.answerLabel = QtWidgets.QLabel(self.centralwidget)
        self.answerLabel.setGeometry(QtCore.QRect(30, 450, 741, 111))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.answerLabel.setFont(font)
        self.answerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.answerLabel.setObjectName("answerLabel")
        self.imageGraphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.imageGraphicsView.setGeometry(QtCore.QRect(150, 100, 501, 291))
        self.imageGraphicsView.setObjectName("imageGraphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.classifyButton.setText(_translate("MainWindow", "Classify This"))
        self.loadFileButton.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "Image file:"))
        self.answerLabel.setText(_translate("MainWindow", "Answer"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

