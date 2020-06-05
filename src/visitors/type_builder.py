from cmp.ast import *
from utils.macros import *
from visitors import visitor
from utils.exceptions import *
from visitors.semantic import *

class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors

        self.object_type = self.context.GetType(OBJECT)
        
        self.io_type = self.context.GetType(IO)
        self.io_type.SetParent(self.object_type)

        self.int_type = self.context.GetType(INT)
        self.int_type.SetParent(self.object_type)
        self.int_type.sealed = True

        self.string_type = self.context.GetType(STRING)
        self.string_type.SetParent(self.object_type)
        self.string_type.sealed = True

        self.bool_type = self.context.GetType(BOOL)
        self.bool_type.SetParent(self.object_type)
        self.bool_type.sealed = True

        self.object_type.DefineMethod(ABORT, [], [], self.object_type)
        self.object_type.DefineMethod(TYPE_NAME, [], [], self.string_type)
        self.object_type.DefineMethod(COPY, [], [], SelfType())
        
        self.io_type.DefineMethod(OUT_STRING, [S], [self.string_type], SelfType())
        self.io_type.DefineMethod(OUT_INT, [I], [self.int_type], SelfType())
        self.io_type.DefineMethod(IN_STRING, [], [], self.string_type)
        self.io_type.DefineMethod(IN_INT, [], [], self.int_type)

        self.string_type.DefineMethod(LENGTH, [], [], self.int_type)
        self.string_type.DefineMethod(CONCAT, [S], [self.string_type], self.string_type)
        self.string_type.DefineMethod(SUBSTR, [POS, LEN], [self.int_type, self.int_type], self.string_type)
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for def_class in node.declarations:
            self.visit(def_class)
            
        try:
            self.context.GetType(MAINN).GetMethod(MAIN)
        except SemanticError:
            self.errors.append(ERROR_ON % (node.line, node.column) + CLASS_METHOD_MAIN)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.GetType(node.id.lex)
        
        parent = node.parent
        if parent:
            try:
                parent_type = self.context.GetType(parent.lex)
                self.current_type.SetParent(parent_type)
            except SemanticError as exception:
                self.errors.append(ERROR_ON % (parent.line, parent.column) + exception.text)
                self.current_type.SetParent(self.object_type)
        else:
            self.current_type.SetParent(self.object_type)
        
        for feature in node.features:
            self.visit(feature)
            
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.GetType(node.type.lex)
        except SemanticError as exception:
            self.errors.append(ERROR_ON % (node.type.line, node.type.column) + exception.text)
            attr_type = ErrorType()
            
        try:
            self.current_type.DefineAttribute(node.id.lex, attr_type)
        except SemanticError as exception:
            self.errors.append(ERROR_ON % (node.line, node.column) + exception.text)
        
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        arg_names, arg_types = [], []
        for idx, typex in node.params:
            try:
                arg_type = self.context.GetType(typex.lex)
            except SemanticError as exception:
                self.errors.append(ERROR_ON % (typex.line, typex.column) + exception.text)
                arg_type = ErrorType()
            else:
                if isinstance(arg_type, SelfType):
                    self.errors.append(ERROR_ON % (typex.line, typex.column) + TYPE_CANNOT_PARAMETER % (arg_type.name))
                    arg_type = ErrorType()
                
            arg_names.append(idx.lex)
            arg_types.append(arg_type)
        
        try:
            ret_type = self.context.GetType(node.type.lex)
        except SemanticError as exception:
            self.errors.append(ERROR_ON % (node.type.line, node.type.column) + exception.text)
            ret_type = ErrorType()
        
        try:
            self.current_type.DefineMethod(node.id.lex, arg_names, arg_types, ret_type)
        except SemanticError as exception:
            self.errors.append(ERROR_ON % (node.line, node.column) + exception.text)

