from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AcercaInferenciaTipos(object):
    def setupUi(self, AcercaInferenciaTipos):
        AcercaInferenciaTipos.setObjectName("AcercaInferenciaTipos")
        AcercaInferenciaTipos.resize(562, 279)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Qt.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AcercaInferenciaTipos.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(AcercaInferenciaTipos)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(AcercaInferenciaTipos)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(AcercaInferenciaTipos)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(AcercaInferenciaTipos)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(AcercaInferenciaTipos)
        self.buttonBox.accepted.connect(AcercaInferenciaTipos.accept)
        self.buttonBox.rejected.connect(AcercaInferenciaTipos.reject)
        QtCore.QMetaObject.connectSlotsByName(AcercaInferenciaTipos)

    def retranslateUi(self, AcercaInferenciaTipos):
        _translate = QtCore.QCoreApplication.translate
        AcercaInferenciaTipos.setWindowTitle(_translate("AcercaInferenciaTipos", "Acerca de Inferencia de Tipos"))
        self.textBrowser.setHtml(_translate("AcercaInferenciaTipos", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:600; color:#000000;\">Inferencia de Tipos</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; color:#005500;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; color:#000000;\">es una aplicación que dada un programa en Classroom Object-Oriented Language (COOL) realiza un análisis de la inferencia de tipos.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; color:#000000;\">Esta aplicación corre tanto en Window como en Linux, siempre y cuando esté instalado </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:600; color:#000000;\">python3</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; color:#000000;\"> y </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:600; color:#000000;\">PyQt5</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; color:#000000;\">.</span></p></body></html>"))
        self.label.setText(_translate("AcercaInferenciaTipos", "<html><head/><body><p align=\"center\">Acerca de Inferencia de Tipos</p></body></html>"))
