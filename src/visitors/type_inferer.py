from cmp.ast import *
from utils.macros import *
from visitors import visitor
from utils.exceptions import *
from visitors.semantic import *

class TypeInferer:
    def __init__(self, context, errors=[], inferences=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        self.inferences = inferences

        self.object_type = self.context.GetType(OBJECT)
        self.io_type = self.context.GetType(IO)
        self.int_type = self.context.GetType(INT)
        self.string_type = self.context.GetType(STRING)
        self.bool_type = self.context.GetType(BOOL)
        
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        self.changed = False

        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return self.changed

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.GetType(node.id.lex)

        for feature, child_scope in zip(node.features, scope.children):
            self.visit(feature, child_scope)

        for attr, var in zip(self.current_type.attributes, scope.locals):
            if var.InferType():
                self.changed = True
                attr.type = var.type
                self.inferences.append(INFERENCE_ATTR % (self.current_type.name, attr.name, var.type.name))

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        expression = node.expression
        if expression:

            attr = self.current_type.GetAttribute(node.id.lex)
            self.visit(expression, scope.children[0], attr.type)
            expr_type = expression.static_type
            var = scope.FindVariable(node.id.lex)
            var.SetUpperType(expr_type)

            if var.InferType():
                self.changed = True
                attr.type = var.type
                self.inferences.append(INFERENCE_ATTR % (self.current_type.name, attr.name, var.type.name))

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.GetMethod(node.id.lex)
        return_type = self.current_method.return_type
        self.visit(node.body, scope.children[0], self.current_type if isinstance(return_type, SelfType) else return_type)

        for i, var in enumerate(scope.locals[1:]):
            if var.InferType():
                self.changed = True
                self.current_method.param_types[i] = var.type
                self.inferences.append(INFERENCE_PARAMETER % (var.type.name, var.name, self.current_method.name, self.current_type.name))
               
        body_type = node.body.static_type
        var = self.current_method.return_info
        var.SetLowerType(body_type)

        if var.InferType():
            self.changed = True
            self.current_method.return_type = var.type
            self.inferences.append(INFERENCE_RETURN % (var.type.name, self.current_method.name, self.current_type.name))

    @visitor.when(IfThenElseNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.condition, scope.children[0], self.bool_type)
        self.visit(node.if_body, scope.children[1])
        self.visit(node.else_body, scope.children[2])
        if_type = node.if_body.static_type
        else_type = node.else_body.static_type
        node.static_type = if_type.TypeUnion(else_type)

    @visitor.when(WhileLoopNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.condition, scope.children[0], self.bool_type)
        self.visit(node.body, scope.children[1])
        node.static_type = self.object_type

    @visitor.when(BlockNode)
    def visit(self, node, scope, expected_type=None):
        for expr, child_scope in zip(node.expressions[:-1], scope.children[:-1]):
            self.visit(expr, child_scope)

        self.visit(node.expressions[-1], scope.children[-1], expected_type)
        node.static_type = node.expressions[-1].static_type
            
    @visitor.when(LetInNode)
    def visit(self, node, scope, expected_type=None):
        for (idx, typex, expr), child_scope, (i, var) in zip(node.let_body, scope.children[:-1], enumerate(scope.locals)):
            if expr:
                self.visit(expr, child_scope, var.type if var.infered else None)
                expr_type = expr.static_type
                var.SetUpperType(expr_type)

                if var.InferType():
                    self.changed = True
                    typex.name = var.type.name
                    self.inferences.append(INFERENCE_ON % (idx.line, idx.column) + INFERENCE_VARIABLE % (var.type.name, var.name))

        self.visit(node.in_body, scope.children[-1], expected_type)

        for i, var in enumerate(scope.locals):
            if var.InferType():
                self.changed = True
                idx, typex, _ = node.let_body[i]
                typex.name = var.type.name
                self.inferences.append(INFERENCE_ON % (idx.line, idx.column) + INFERENCE_VARIABLE % (var.type.name, var.name))

        node.static_type = node.in_body.static_type

    @visitor.when(CaseOfNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.expression, scope.children[0])
        node.static_type = None

        for (idx, typex, expr), child_scope in zip(node.branches, scope.children[1:]):
            self.visit(expr, child_scope)
            expr_type = expr.static_type
            node.static_type = node.static_type.TypeUnion(expr_type) if node.static_type else expr_type

    @visitor.when(AssignNode)
    def visit(self, node, scope, expected_type=None):
        var = scope.FindVariable(node.id.lex) if scope.IsDefined(node.id.lex) else None
        self.visit(node.expression, scope.children[0], var.type if var and var.infered else expected_type)
        expr_type = node.expression.static_type
        var.SetLowerType(expr_type)
        node.static_type = expr_type

    @visitor.when(NotNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.expression, scope.children[0], self.bool_type)
        node.static_type = self.bool_type

    @visitor.when(LessEqualNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.left, scope.children[0], self.int_type)
        self.visit(node.right, scope.children[1], self.int_type)
        node.static_type = self.bool_type

    @visitor.when(LessNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.left, scope.children[0], self.int_type)
        self.visit(node.right, scope.children[1], self.int_type)
        node.static_type = self.bool_type

    @visitor.when(EqualNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.left, scope.children[0], node.right.static_type)
        self.visit(node.right, scope.children[1], node.left.static_type)
        node.static_type = self.bool_type

    @visitor.when(ArithmeticNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.left, scope.children[0], self.int_type)
        self.visit(node.right, scope.children[1], self.int_type)
        node.static_type = self.int_type

    @visitor.when(IsVoidNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.expression, scope.children[0])
        node.static_type = self.bool_type

    @visitor.when(ComplementNode)
    def visit(self, node, scope, expected_type=None):
        self.visit(node.expression, scope.children[0], self.int_type)
        node.static_type = self.int_type

    @visitor.when(FunctionCallNode)
    def visit(self, node, scope, expected_type=None):
        node_type = None
        if node.type:
                try:
                    node_type = self.context.GetType(node.type.lex)
                except SemanticError:
                    node_type = ErrorType()
                else:
                    if isinstance(node_type, SelfType) or isinstance(node_type, AutoType):
                        node_type = ErrorType()

        self.visit(node.obj, scope.children[0], node_type)
        obj_type = node.obj.static_type
        
        try:
            obj_type = node_type if node_type else obj_type
            obj_method = obj_type.GetMethod(node.id.lex)       
            node_type = obj_type if isinstance(obj_method.return_type, SelfType) else obj_method.return_type
        except SemanticError:
            node_type = ErrorType()
            obj_method = None
            
        if obj_method and len(node.args) == len(obj_method.param_types):
            for arg, var, child_scope in zip(node.args, obj_method.param_infos, scope.children[1:]):
                self.visit(arg, child_scope, var.type if var.infered else None)
        else:
            for arg, child_scope in zip(node.args, scope.children[1:]):
                self.visit(arg, child_scope)
        
        node.static_type = node_type

    @visitor.when(MemberCallNode)
    def visit(self, node, scope, expected_type=None):
        obj_type = self.current_type
        
        try:
            obj_method = obj_type.GetMethod(node.id.lex)
            node_type = obj_type if isinstance(obj_method.return_type, SelfType) else obj_method.return_type
        except SemanticError:
            node_type = ErrorType()
            obj_method = None

        if obj_method and len(node.args) == len(obj_method.param_types):
            for arg, var, child_scope in zip(node.args, obj_method.param_infos, scope.children):
                self.visit(arg, child_scope, var.type if var.infered else None)
        else:
            for arg, child_scope in zip(node.args, scope.children):
                self.visit(arg, child_scope)
            
        node.static_type = node_type

    @visitor.when(NewNode)
    def visit(self, node, scope, expected_type=None):
        try:
            node_type = self.context.GetType(node.type.lex)
        except SemanticError:
            node_type = ErrorType()
            
        node.static_type = node_type

    @visitor.when(IntegerNode)
    def visit(self, node, scope, expected_type=None):
        node.static_type = self.int_type

    @visitor.when(StringNode)
    def visit(self, node, scope, expected_type=None):
        node.static_type = self.string_type

    @visitor.when(IdNode)
    def visit(self, node, scope, expected_type=None):
        if scope.IsDefined(node.token.lex):
            var = scope.FindVariable(node.token.lex)

            if expected_type:
                var.SetUpperType(expected_type)

            node_type = var.type if var.infered else AutoType()   
        else:
            node_type = ErrorType()
        
        node.static_type = node_type
    
    @visitor.when(BoolNode)
    def visit(self, node, scope, expected_type=None):
        node.static_type = self.bool_type

