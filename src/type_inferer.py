import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *

from uis.Ayuda import Ui_Ayuda
from uis.AcercaAutores import Ui_AcercaAutores
from uis.InferenciaTipos import Ui_InferenciaTipos

from cmp.lexer import *
from utils.macros import *
from utils.utils import Utils
from utils.exceptions import *
from cmp.parser import CoolParser
from utils.type_check import type_check
from visitors.type_builder import TypeBuilder
from visitors.type_checker import TypeChecker
from visitors.type_inferer import TypeInferer
from visitors.format_visitor import FormatVisitor
from visitors.type_collector import TypeCollector

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_InferenciaTipos()
        self.ui.setupUi(self)

        self.ui.actionNuevoCodigo.triggered.connect(self.NewCode)
        self.ui.actionCargarCodigo.triggered.connect(self.LoadCode)
        self.ui.actionGuardarCodigo.triggered.connect(self.SaveCode)
        self.ui.actionGuardarResultados.triggered.connect(self.SaveResult)
        self.ui.actionAnalisis.triggered.connect(self.AnalyseCode)
        self.ui.actionSalir.triggered.connect(self.Exit)
        self.ui.actionAyuda.triggered.connect(self.Help)
        self.ui.actionAcercaAutores.triggered.connect(self.AboutAuthors)

        self.NewCode()

    def ClearResults(self):
        self.ui.tabWidgetCodigo.setTabEnabled(0, True)
        self.ui.tabWidgetCodigo.setCurrentIndex(0)
        self.ui.textResultados.setPlainText(NULL)
    
    def UpdateStatus(self):
        self.ui.tabWidgetCodigo.setStatusTip(self.path if self.path else STAR + NUEVO_CODIGO)

    def NewCode(self):
        self.path = None
        self.ui.textCodigoCOOL.setPlainText(NULL)
        self.UpdateStatus()
        self.ClearResults()

    def DialogCritical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def LoadCode(self):
        path, _ = QFileDialog.getOpenFileName(self, CARGAR_CODIGO, NULL, DOCUMENTO_COOl)

        if not path:
            return

        try:
            with open(path, READ) as file:
                code = file.read()
        except Exception as exception:
            self.DialogCritical(str(exception))
        else:
            self.path = path
            self.ui.textCodigoCOOL.setPlainText(code)
            self.UpdateStatus()
            self.ClearResults()

    def SaveCode(self):
        path, _ = QFileDialog.getSaveFileName(self, GUARDAR_CODIGO, NULL, DOCUMENTO_COOl)
        code = self.ui.textCodigoCOOL.toPlainText()

        if not path:
            return

        try:
            with open(path, WRITE) as file:
                file.write(code)
        except Exception as exception:
            self.dialog_critical(str(exception))
        else:
            self.path = path
            self.UpdateStatus()        

    def SaveResult(self):
        path, _ = QFileDialog.getSaveFileName(self, GUARDAR_RESULTADO, NULL, DOCUMENTO_TEXTO)
        result = self.ui.textResultados.toPlainText()

        if not path:
            return

        try:
            with open(path, WRITE) as file:
                file.write(result)
        except Exception as exception:
            self.dialog_critical(str(exception))
        else:
            self.path = path
            self.UpdateStatus()
        
    def Exit(self):
        self.close()

    def AnalyseCode(self):

        self.ui.textResultados.setPlainText('')
        code = self.ui.textCodigoCOOL.toPlainText()
        Utils.Print(CODIGO, LENGTH_CONSOLE)
        print(code)

        Utils.Print(LEXER, LENGTH_CONSOLE)
        tokens = Tokenizer(code)
        PrintTokens(tokens)

        Utils.Print(PARSER, LENGTH_CONSOLE)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{Utils.GetString(PARSER, 64)}\n')
        parse, operations = CoolParser(tokens)
        if not operations:
            self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{UNEXCEPTED_TOKEN % (parse.lex, parse.line, parse.column)}\n')
            print(UNEXCEPTED_TOKEN % (parse.lex, parse.line, parse.column))
            return
        productions = '\n'.join(repr(x) for x in parse)
        print(productions)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{productions}\n')

        Utils.Print(AST, LENGTH_CONSOLE)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{Utils.GetString(AST, 64)}\n')
        ast = Utils.EvaluateReverseParse(parse, operations, tokens)
        formatter = FormatVisitor()
        tree = formatter.visit(ast)
        print(tree)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{tree}\n')

        Utils.Print(COLECCIONANDO_TIPOS, LENGTH_CONSOLE)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{Utils.GetString(COLECCIONANDO_TIPOS, 68)}\n')
        errors = []
        collector = TypeCollector(errors)
        collector.visit(ast)
        context = collector.context
        print('ERRORES :', errors)
        print('CONTEXTO :')
        print(context)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}ERRORES : [\n')
        for error in errors:
            self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}    {error}\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}]\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}CONTEXTO :\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{context}\n')

        Utils.Print(CONSTRUYENDO_TIPOS, LENGTH_CONSOLE)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{Utils.GetString(CONSTRUYENDO_TIPOS, 67)}\n')
        builder = TypeBuilder(context, errors)
        builder.visit(ast)
        print('ERRORES : [')
        for error in errors:
            print(SPACE * 4, error)
        print(']')
        print('CONTEXTO :')
        print(context)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}ERRORES : [\n')
        for error in errors:
            self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}    {error}\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}]\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}CONTEXTO :\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{context}\n')

        Utils.Print(CHEQUEANDO_TIPOS, LENGTH_CONSOLE)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{Utils.GetString(CHEQUEANDO_TIPOS, 67)}\n')
        checker = TypeChecker(context, errors)
        scope = checker.visit(ast)
        print('ERRORES : [')
        for error in errors:
            print(SPACE * 4, error)
        print(']')
        print('CONTEXTO :')
        print(context)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}ERRORES : [\n')
        for error in errors:
            self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}    {error}\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}]\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}CONTEXTO :\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{context}\n')

        Utils.Print(INFERENCIA_DE_TIPOS, LENGTH_CONSOLE)
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{Utils.GetString(INFERENCIA_DE_TIPOS, 69)}\n')
        inferences = []
        inferer = TypeInferer(context, errors, inferences)
        while inferer.visit(ast, scope): 
            pass
        print('INFERENCIA : [')
        for inference in inferences:
            print(SPACE * 4, inference)
        print(']')
        print('CONTEXTO :')
        print(context)
        print(f'SCOPE : {scope}')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}INFERENCIA : [\n')
        for inference in inferences:
            self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}    {inference}\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}]\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}CONTEXTO :\n')
        self.ui.textResultados.setPlainText(f'{self.ui.textResultados.toPlainText()}{context}')
        
        self.ui.tabWidgetCodigo.setTabEnabled(1, True)
        self.ui.tabWidgetCodigo.setCurrentIndex(1)
        
    def Help(self):
        dialog = QDialog()
        ui_dialog = Ui_Ayuda()
        ui_dialog.setupUi(dialog)

        dialog.exec()

    def AboutAuthors(self):
        dialog = QDialog()
        ui_dialog = Ui_AcercaAutores()
        ui_dialog.setupUi(dialog)

        dialog.exec()

def Main():

    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == FUNC_MAIN:
    Main()
