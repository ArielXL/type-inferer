from cmp.ast import *
from utils.macros import *
from visitors import visitor
from utils.exceptions import *
from visitors.semantic import *

class TypeCollector(object):

    def __init__(self, errors=[]):
        self.context = Context()
        self.errors = errors

        self.context.AddType(SelfType())
        self.context.AddType(AutoType())

        self.context.CreateType(OBJECT)
        self.context.CreateType(IO)
        self.context.CreateType(INT)
        self.context.CreateType(STRING)
        self.context.CreateType(BOOL)
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):       
        for declaration in node.declarations:
            self.visit(declaration)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.CreateType(node.id.lex)
        except SemanticError as exception:
            self.errors.append(ERROR_ON % (node.line, node.column) + exception.text)

