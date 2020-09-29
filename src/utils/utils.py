from cmp.ast import *
from utils.macros import *
from utils.exceptions import *
from cmp.pycompiler import EOF
from utils.type_check import type_check
from cmp.utils_parser import ShiftReduceParser, Action

class Utils:

    @type_check
    def CheckParams(args : list) -> bool:
        '''
        Verifica que solamente se pase un solo parametro.
        '''
        if len(args) == 1:
            return True
        else:
            print(INVALID_ARGS)
            return False

    @type_check
    def CheckPath(path : str) -> bool:
        '''
        Verifica si la ruta tiene la extension correcta.
        '''
        file = Utils.GetFile(path)
        EXTENSION = DOT + CL

        if not file.endswith(EXTENSION):
            print(INVALID_EXTENSION % (file))
            return False
        return True

    @type_check
    def ReverseString(string : str) -> str:
        '''
        Devuelve el reverso de una cadena.
        '''
        reverse_string = NULL
        for i in range(-1, -len(string) - 1, -1):
            reverse_string += string[i]
        return reverse_string

    @type_check
    def GetFile(path : str) -> str:
        '''
        Devuelve el archivo dado una ruta.
        '''
        file_reverse = NULL
        for i in range(-1, -len(path) - 1, -1):
            if path[i] == SLACH:
                break
            else:
                file_reverse += path[i]
        file = Utils.ReverseString(file_reverse)
        return file

    @type_check
    def GetProgramCode(path : str):
        '''
        Devuelve el codigo fuente dado una ruta.
        '''
        code = NULL
        try:
            with open(path, encoding = UTF8) as file:
                code += file.read()
        except (IOError, FileNotFoundError):
            print(PATH_NOT_FOUND % (path))
            return None
        return code

    @type_check
    def GetString(text : str, console_len : int) -> str:
        '''
        Devuelve el string de forma linda, segun la variable text.
        '''
        right = (console_len - len(text) - 2) // 2
        left = console_len - len(text) - 2 - right
        line = NULL

        for _ in range(right):
            line += EQUAL
        
        line += SPACE
        line += text
        line += SPACE

        for _ in range(left):
            line += EQUAL

        return line

    @type_check
    def Print(text : str, console_len : int) -> None:
        '''
        Imprime en la consola de forma linda, segun la variable text.
        '''
        line = Utils.GetString(text, console_len)
        print(line)

    @type_check
    def EvaluateReverseParse(right_parse : list, operations : list, tokens : list) -> ProgramNode:
        '''
        Evalua las reglas semanticas de la gramatica atributada para 
        obtener la raiz del AST.
        '''
        if not right_parse or not operations or not tokens:
            return

        right_parse = iter(right_parse)
        tokens = iter(tokens)
        stack = []

        for operation in operations:
            if operation == Action.SHIFT:
                token = next(tokens)
                stack.append(token)
            elif operation == Action.REDUCE:
                production = next(right_parse)
                head, body = production
                attributes = production.attributes
                rule = attributes[0]

                if len(body):
                    synteticed = [None] + stack[-len(body):]
                    value = rule(None, synteticed)
                    stack[-len(body):] = [value]
                else:
                    stack.append(rule(None, None))
            else:
                raise Exception(INVALID_ACTION)

        return stack[0]
