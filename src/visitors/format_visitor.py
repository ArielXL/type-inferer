from cmp.ast import *
from utils.macros import *
from visitors import visitor

class FormatVisitor:

    @visitor.on('node')
    def visit(self, node, space):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, space=0):
        ans = (SPACE * 4) * space + f'\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, space + 1) for child in node.declarations)
        return f'{ans}\n{statements}'
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, space=0):
        parent = NULL if node.parent is None else f"inherits {node.parent.lex}"
        ans = (SPACE * 4) * space + f'\__ClassDeclarationNode : class {node.id.lex} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(self.visit(child, space + 1) for child in node.features)
        return f'{ans}\n{features}'
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, space=0):
        ans = (SPACE * 4) * space + f'\__AttrDeclarationNode : {node.id.lex} : {node.type.lex}' + (' <- <expr>' if node.expression else NULL) + SEMI_COLON
        expr = self.visit(node.expression, space + 1) if node.expression else None
        return f'{ans}' + (f'\n{expr}' if expr else NULL)
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, space=0):
        params = ', '.join(' : '.join(tok.lex for tok in param) for param in node.params)
        ans = (SPACE * 4) * space + f'\__FuncDeclarationNode : {node.id.lex}({params}) : {node.type.lex} {{ <expr> }}'
        body = self.visit(node.body, space + 1)
        return f'{ans}\n{body}'

    @visitor.when(IfThenElseNode)
    def visit(self, node, space=0):
        ans = (SPACE * 4) * space + f'\__IfThenElseNode : if <expr> then <expr> else <expr> fi'
        cond = self.visit(node.condition, space + 1)
        if_body = self.visit(node.if_body, space + 1)
        else_body = self.visit(node.else_body, space + 1)
        return f'{ans}\n{cond}\n{if_body}\n{else_body}'

    @visitor.when(WhileLoopNode)
    def visit(self, node, space=0):
        ans = (SPACE * 4) * space + f'\__WhileNode : while <expr> loop <expr> pool'
        cond = self.visit(node.condition, space + 1)
        body = self.visit(node.body, space + 1)
        return f'{ans}\n{cond}\n{body}'

    @visitor.when(BlockNode)
    def visit(self, node, space=0):
        ans = (SPACE * 4) * space + f'\__BlockNode : {{ <expr>; ... <expr>; }}'
        expressions = '\n'.join(self.visit(expr, space + 1) for expr in node.expressions)
        return f'{ans}\n{expressions}'

    @visitor.when(LetInNode)
    def visit(self, node, space=0):
        let_body = ', '.join(f'{idx.lex} : {typex.lex}' + (' <- <expr>' if expr else NULL) for idx, typex, expr in node.let_body)
        ans = (SPACE * 4) * space + f'\__LetInNode : let {let_body} in <expr>'
        lets = '\n'.join(self.visit(expr, space + 1) for _, _, expr in node.let_body if expr)
        body = self.visit(node.in_body, space + 1)
        return f'{ans}\n{lets}\n{body}'

    @visitor.when(CaseOfNode)
    def visit(self, node, space=0):
        case_body = ' '.join(f'{idx.lex} : {typex.lex} => <expr>;' for idx, typex, expr in node.branches)
        ans = (SPACE * 4) * space + f'\__CaseOfNode : case <expr> of {case_body} esac'
        expression = self.visit(node.expression, space + 1)
        body = '\n'.join(self.visit(expr, space + 1) for _, _, expr in node.branches)
        return f'{ans}\n{expression}\n{body}'

    @visitor.when(AssignNode)
    def visit(self, node, space=0):
        ans = (SPACE * 4) * space + f'\__AssingNode : {node.id.lex} <- <expr>'
        expr = self.visit(node.expression, space + 1)
        return f'{ans}\n{expr}'

    @visitor.when(UnaryNode)
    def visit(self, node, space=0):
        ans = (SPACE * 4) * space + f'\__{node.__class__.__name__} <expr>'
        expression = self.visit(node.expression, space + 1)
        return f'{ans}\n{expression}'

    @visitor.when(BinaryNode)
    def visit(self, node, space=0):
        ans = (SPACE * 4) * space + f'\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, space + 1)
        right = self.visit(node.right, space + 1)
        return f'{ans}\n{left}\n{right}'    

    @visitor.when(FunctionCallNode)
    def visit(self, node, space=0):
        obj = self.visit(node.obj, space + 1)
        typex = f'@{node.type.lex}' if node.type else NULL
        ans = (SPACE * 4) * space + f'\__FunctionCallNode : <obj>{typex}.{node.id.lex}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, space + 1) for arg in node.args)
        return f'{ans}\n{obj}\n{args}'

    @visitor.when(MemberCallNode)
    def visit(self, node, space=0):
        ans = (SPACE * 4) * space + f'\__MemberCallNode : {node.id.lex}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, space + 1) for arg in node.args)
        return f'{ans}\n{args}'
    
    @visitor.when(NewNode)
    def visit(self, node, space=0):
        return (SPACE * 4) * space + f'\__NewNode : new {node.type.lex}'

    @visitor.when(AtomicNode)
    def visit(self, node, space=0):
        return (SPACE * 4) * space + f'\__{node.__class__.__name__} : {node.token.lex}'

