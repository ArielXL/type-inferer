import sys
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

@type_check
def Main(input_file_path : str) -> None:

    if not Utils.CheckPath(input_file_path):
        return

    code = Utils.GetProgramCode(input_file_path)
    if code == None or code == NULL:
        return
    Utils.Print(CODIGO, LENGTH_CONSOLE)
    print(code)

    Utils.Print(LEXER, LENGTH_CONSOLE)
    tokens = Tokenizer(code)
    PrintTokens(tokens)

    Utils.Print(PARSER, LENGTH_CONSOLE)
    parse, operations = CoolParser(tokens)
    if not operations:
        print(UNEXCEPTED_TOKEN % (parse.lex, parse.line, parse.column))
        return
    print('\n'.join(repr(x) for x in parse))

    Utils.Print(AST, LENGTH_CONSOLE)
    ast = Utils.EvaluateReverseParse(parse, operations, tokens)
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    print(tree)

    Utils.Print(COLECCIONANDO_TIPOS, LENGTH_CONSOLE)
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    print('ERRORES :', errors)
    print('CONTEXTO :')
    print(context)

    Utils.Print(CONSTRUYENDO_TIPOS, LENGTH_CONSOLE)
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    print('ERRORES : [')
    for error in errors:
        print(SPACE * 4, error)
    print(']')
    print('CONTEXTO :')
    print(context)

    Utils.Print(CHEQUEANDO_TIPOS, LENGTH_CONSOLE)
    checker = TypeChecker(context, errors)
    scope = checker.visit(ast)
    print('ERRORES : [')
    for error in errors:
        print(SPACE * 4, error)
    print(']')
    print('CONTEXTO :')
    print(context)

    Utils.Print(INFERENCIA_DE_TIPOS, LENGTH_CONSOLE)
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

if __name__ == FUNC_MAIN:

    if not Utils.CheckParams(sys.argv[1:]):
        sys.exit(1)
    input_file_path = sys.argv[1]

    Main(input_file_path)