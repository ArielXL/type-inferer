import itertools as itt
from utils.macros import *
from utils.exceptions import *
from utils.type_check import type_check

class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class Attribute:

    @type_check
    def __init__(self, name : str, typex) -> None:
        self.name = name
        self.type = typex

    @type_check
    def __str__(self) -> str:
        return f'[attrib] {self.name} : {self.type.name} ;'

    @type_check
    def __repr__(self) -> str:
        return str(self)

class Method:

    @type_check
    def __init__(self, name : str, param_names : list, params_types : list, return_type) -> None:
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.param_infos = [VariableInfo(f'_{name}_{pname}', ptype) for pname, ptype in zip(param_names, params_types)] 
        self.return_type = return_type
        self.return_info = VariableInfo(f'_{name}', return_type)

    @type_check
    def __str__(self) -> str:
        params = ', '.join(f'{n} : {t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}) : {self.return_type.name} ;'

    @type_check
    def __eq__(self, other) -> bool:
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:

    def __init__(self, name : str, sealed=False) -> None:
        self.name = name
        self.attributes = []
        self.methods = {}
        self.parent = None
        self.sealed = sealed

    def SetParent(self, parent) -> None:
        if self.parent is not None:
            raise SemanticError(PARENT_ALREADY_DEFINED % (self.name))
        if parent.sealed:
            raise SemanticError(TYPE_SEALED % (parent.name))
        self.parent = parent

    def TypeUnion(self, other):
        if self == other:
            return other

        t1 = [self]
        while t1[-1] != None:
            t1.append(t1[-1].parent)

        t2 = [other]
        while t2[-1] != None:
            t2.append(t2[-1].parent)

        while t1[-2] == t2[-2]:
            t1.pop()
            t2.pop()

        return t1[-1]

    def GetAttribute(self, name : str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(ATTR_NOT_DEFINED % (name, self.name))
            try:
                return self.parent.GetAttribute(name)
            except SemanticError:
                raise SemanticError(ATTR_NOT_DEFINED % (name, self.name))

    def DefineAttribute(self, name : str, typex):
        try:
            self.GetAttribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(ATTR_ALREADY_DEFINED % (name, self.name))

    def GetMethod(self, name : str):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                raise SemanticError(METHOD_NOT_DEFINED % (name, self.name))
            try:
                return self.parent.GetMethod(name)
            except SemanticError:
                raise SemanticError(METHOD_NOT_DEFINED % (name, self.name))

    def DefineMethod(self, name : str, param_names : list, param_types : list, return_type):
        if name in self.methods:
            raise SemanticError(METHOD_ALREADY_DEFINED % (name, self.name))

        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

    def ConformsTo(self, other):
        return other.ByPass() or self == other or self.parent is not None and self.parent.ConformsTo(other)

    def ByPass(self):
        return False

    def __str__(self):
        output = f'tipo {self.name}'
        parent = NULL if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n    ' if self.attributes or self.methods else NULL
        output += '\n    '.join(str(x) for x in self.attributes)
        output += '\n    ' if self.attributes else NULL
        output += '\n    '.join(str(x) for x in self.methods.values())
        output += '\n' if self.methods else NULL
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class SelfType(Type):
    def __init__(self):
        Type.__init__(self, SELF_TYPE)
        self.sealed = True

    def ConformsTo(self, other):
        return False

    def ByPass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, SelfType)

class AutoType(Type):
    def __init__(self):
        Type.__init__(self, AUTO_TYPE)
        self.sealed = True

    def UnionType(self, other):
        return self

    def ConformsTo(self, other):
        return True

    def ByPass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, LESS + ERROR + GREATER)
        self.sealed = True

    def UnionType(self, other):
        return self

    def ConformsTo(self, other):
        return True

    def ByPass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class Context:

    @type_check
    def __init__(self) -> None:
        self.types = {}

    @type_check
    def CreateType(self, name : str) -> Type:
        if name in self.types:
            raise SemanticError(TYPE_ALREADY_DEFINED_CONTEXT % (name))
        typex = self.types[name] = Type(name)
        return typex

    @type_check
    def AddType(self, typex : Type) -> Type:
        if typex.name in self.types:
            raise SemanticError(TYPE_ALREADY_DEFINED_CONTEXT % ({typex.name}))
        self.types[typex.name] = typex
        return typex

    @type_check
    def GetType(self, name : str) -> Type:
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(TYPE_NOT_DEFINED % (name))

    @type_check
    def __str__(self) -> str:
        return '{\n    ' + '\n    '.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    @type_check
    def __repr__(self) -> str:
        return str(self)

class VariableInfo:

    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype
        self.infered = not isinstance(vtype, AutoType)
        self.upper_types = []
        self.lower_types = []

    def SetUpperType(self, typex):
        if not self.infered and not isinstance(typex, AutoType):
            self.upper_types.append(typex)

    def SetLowerType(self, typex):
        if not self.infered:
            self.lower_types.append(typex)

    def InferType(self):
        if not self.infered:
            upper_type = None
            for typex in self.upper_types:
                if not upper_type or typex.ConformsTo(upper_type):
                    upper_type = typex
                elif upper_type.ConformsTo(typex):
                    pass
                else:
                    upper_type = ErrorType()
                    break

            lower_type = None
            for typex in self.lower_types:
                lower_type = typex if not lower_type else lower_type.TypeUnion(typex)

            if lower_type:
                self.type = lower_type if not upper_type or lower_type.ConformsTo(upper_type) else ErrorType()
            else:
                self.type = upper_type

            if not self.type or isinstance(self.type, ErrorType):
                self.type = AutoType()

            self.infered = not isinstance(self.type, AutoType)
            self.upper_types = []
            self.lower_types = []

            return self.infered

        return False

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def CreateChild(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def DefineVariable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def FindVariable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.FindVariable(vname, self.index) if self.parent is not None else None

    def IsDefined(self, vname):
        return self.FindVariable(vname) is not None

    def IsLocal(self, vname):
        return any(True for x in self.locals if x.name == vname)

