class Token:
    def __init__(self, lex, token_type, line=0, column=0):
        self.lex = lex
        self.token_type = token_type
        self.line = line
        self.column = column

    def __str__(self):
        return f'FILA: {self.line}, COLUMNA: {self.column}, TIPO: {self.token_type}, LEXEMA: {self.lex}'

    def __repr__(self):
        return str(self)

    @property
    def IsValid(self):
        return True

