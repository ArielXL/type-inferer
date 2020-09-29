# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Orientacion.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Orientacion(object):
    def setupUi(self, Orientacion):
        Orientacion.setObjectName("Orientacion")
        Orientacion.resize(546, 252)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Qt.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Orientacion.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Orientacion)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Orientacion)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Orientacion)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Orientacion)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Orientacion)
        self.buttonBox.accepted.connect(Orientacion.accept)
        self.buttonBox.rejected.connect(Orientacion.reject)
        QtCore.QMetaObject.connectSlotsByName(Orientacion)

    def retranslateUi(self, Orientacion):
        _translate = QtCore.QCoreApplication.translate
        Orientacion.setWindowTitle(_translate("Orientacion", "Orientación"))
        self.textBrowser.setHtml(_translate("Orientacion", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">La inferencia de tipos es la capacidad de deducir, ya sea parcial o totalmente, el tipo de una expresión en</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">tiempo de compilación. El objetivo de esta aplicación es la implementación de un intérprete del lenguaje </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">COOL </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">  (</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; text-decoration: underline;\">C</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">lassroom </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; text-decoration: underline;\">O</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">bject-</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; text-decoration: underline;\">O</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">riented </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; text-decoration: underline;\">L</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">anguage) que posea inferencia de tipos mediante la adición del tipo </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">AUTO_TYPE</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">.</span></p></body></html>"))
        self.label.setText(_translate("Orientacion", "<html><head/><body><p align=\"center\">Orientación</p></body></html>"))
