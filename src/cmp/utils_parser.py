from cmp.automata import *
from utils.macros import *
from cmp.pycompiler import *
from utils.exceptions import *
from utils.type_check import type_check

class ContainerSet:

    def __init__(self, *values, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    @type_check
    def Add(self, value : Item) -> bool:
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    @type_check
    def Extend(self, values : list) -> bool:
        change = False
        for value in values:
            change |= self.Add(value)
        return change

    @type_check
    def SetEpsilon(self, value=True) -> bool:
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    @type_check
    def Update(self, other) -> bool:
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    @type_check
    def EpsilonUpdate(self, other) -> bool:
        return self.SetEpsilon(self.contains_epsilon | other.contains_epsilon)

    @type_check
    def HardUpdate(self, other) -> bool:
        return self.Update(other) | self.EpsilonUpdate(other)

    def FindMatch(self, match):
        for item in self.set:
            if item == match:
                return item
        return None

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        return '%s-%s' % (str(self.set), self.contains_epsilon)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.set)

    def __nonzero__(self):
        return len(self) > 0

    def __eq__(self, other):
        if isinstance(other, set):
            return self.set == other
        return isinstance(other, ContainerSet) and self.set == other.set and self.contains_epsilon == other.contains_epsilon

class Action(tuple):
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __str__(self):
        try:
            action, tag = self
            return f"{'S' if action == Action.SHIFT else 'OK' if action == Action.OK else NULL}{tag}"
        except:
            return str(tuple(self))

    __repr__ = __str__

class ShiftReduceParser: 

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self.BuildParsingTable()
    
    def BuildParsingTable(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output, operations = [], []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor].token_type
            if self.verbose: print(stack, w[cursor:])
                
            try:
                action, tag = self.action[state][lookahead][0]
                if action == Action.SHIFT:
                    stack.append(tag)
                    cursor += 1
                    operations.append(action)
                elif action == Action.REDUCE:
                    for _ in range(len(tag.Right)): stack.pop()
                    stack.append(self.goto[stack[-1]][tag.Left][0])
                    output.append(tag)
                    operations.append(action)
                elif action == Action.OK:
                    return output, operations
                else:
                    assert False, 'Must be something wrong!'
            except KeyError:
                print('Parsing Error:', stack, w[cursor:])
                return w[cursor:][0], None

class LR1Parser(ShiftReduceParser):

    @staticmethod
    @type_check
    def Expand(item : Item, firsts : dict) -> list:
        next_symbol = item.NextSymbol
        if next_symbol is None or not next_symbol.IsNonTerminal:
            return []
        
        lookaheads = ContainerSet()
        for preview in item.Preview():
            lookaheads.HardUpdate(UtilsParsers.ComputeLocalFirst(firsts, preview))
        
        return [Item(prod, 0, lookaheads) for prod in next_symbol.productions]

    @staticmethod
    @type_check
    def Compress(items : ContainerSet) -> set:
        centers = {}

        for item in items:
            center = item.Center()
            try:
                lookaheads = centers[center]
            except KeyError:
                centers[center] = lookaheads = set()
            lookaheads.update(item.lookaheads)
        
        return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

    @staticmethod
    @type_check
    def ClosureLR1(items : frozenset, firsts : dict) -> set:
        closure = ContainerSet(*items)
        
        changed = True
        while changed:
            changed = False
            
            new_items = ContainerSet()
            for item in closure:
                new_items.Extend(LR1Parser.Expand(item, firsts))

            changed = closure.Update(new_items)
            
        return LR1Parser.Compress(closure)
    
    @staticmethod
    @type_check
    def GotoLR1(items : frozenset, symbol, firsts=None, just_kernel=False):
        items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
        return items if just_kernel else LR1Parser.ClosureLR1(items, firsts)

    def BuildLR1Automaton(self):
        G = self.augmentedG = self.G.AugmentedGrammar(True)

        firsts = UtilsParsers.ComputeFirsts(G)
        firsts[G.EOF] = ContainerSet(G.EOF)
        
        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0, lookaheads=(G.EOF,))
        start = frozenset([start_item])
        
        closure = LR1Parser.ClosureLR1(start, firsts)
        automaton = State(frozenset(closure), True)
        
        pending = [ start ]
        visited = { start: automaton }
        
        while pending:
            current = pending.pop()
            current_state = visited[current]
            
            for symbol in G.terminals + G.nonTerminals:
                kernels = LR1Parser.GotoLR1(current_state.state, symbol, just_kernel=True)
                
                if not kernels:
                    continue
                
                try:
                    next_state = visited[kernels]
                except KeyError:
                    pending.append(kernels)
                    visited[pending[-1]] = next_state = State(frozenset(LR1Parser.GotoLR1(current_state.state, symbol, firsts)), True)
                
                current_state.add_transition(symbol.Name, next_state)
        
        self.automaton = automaton

    def BuildParsingTable(self):
        self.is_lr1 = True
        self.BuildLR1Automaton()
        
        for i, node in enumerate(self.automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
            node.tag = f'I{i}'

        for node in self.automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == self.augmentedG.startSymbol:
                        self.is_lr1 &= UtilsParsers.Register(self.action, idx, self.augmentedG.EOF, 
                                                            Action((Action.OK, NULL)))
                    else:
                        for lookahead in item.lookaheads:
                            self.is_lr1 &= UtilsParsers.Register(self.action, idx, lookahead, 
                                                                Action((Action.REDUCE, prod)))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.is_lr1 &= UtilsParsers.Register(self.action, idx, next_symbol, 
                                                            Action((Action.SHIFT, node[next_symbol.Name][0].idx)))
                    else:
                        self.is_lr1 &= UtilsParsers.Register(self.goto, idx, next_symbol, 
                                                            node[next_symbol.Name][0].idx)
                pass

class UtilsParsers:

    @type_check
    def ComputeLocalFirst(firsts : dict, alpha) -> ContainerSet:
        '''
        Computa el conjunto First de la cadena alpha, esta cadena puede 
        tener tanto terminales como non-terminales.
        '''
        first_alpha = ContainerSet()
        
        try:
            alpha_is_epsilon = alpha.IsEpsilon
        except:
            alpha_is_epsilon = False

        if alpha_is_epsilon:
            first_alpha.SetEpsilon()
        else:
            for symbol in alpha:
                first_symbol = firsts[symbol]
                first_alpha.Update(first_symbol)
                if not first_symbol.contains_epsilon:
                    break
            else:
                first_alpha.SetEpsilon()

        return first_alpha

    @type_check
    def ComputeFirsts(G : Grammar) -> dict:
        '''
        Calcula el conjunto First de los terminales, los no-terminales
        y las partes derechas de la gramatica.
        '''
        firsts = {}
        change = True
        
        for terminal in G.terminals:
            firsts[terminal] = ContainerSet(terminal)
            
        for nonterminal in G.nonTerminals:
            firsts[nonterminal] = ContainerSet()
        
        while change:
            change = False
            
            for production in G.Productions:
                X = production.Left
                alpha = production.Right
                
                first_X = firsts[X]
                    
                try:
                    first_alpha = firsts[alpha]
                except:
                    first_alpha = firsts[alpha] = ContainerSet()
                
                local_first = UtilsParsers.ComputeLocalFirst(firsts, alpha)
                
                change |= first_alpha.HardUpdate(local_first)
                change |= first_X.HardUpdate(local_first)
                        
        return firsts

    @type_check
    def ComputeFollows(G: Grammar, firsts : dict) -> dict:
        '''
        Calcula el conjunto Follow de todos los no terminales de la
        gramatica.
        '''
        follows = { }
        change = True
        local_firsts = {}
        
        for nonterminal in G.nonTerminals:
            follows[nonterminal] = ContainerSet()
        follows[G.startSymbol] = ContainerSet(G.EOF)
        
        while change:
            change = False
            
            for production in G.Productions:

                X = production.Left
                alpha = production.Right                
                follow_X = follows[X]
                
                for i, symbol in enumerate(alpha):
                    if symbol.IsNonTerminal:
                        follow_symbol = follows[symbol]
                        beta = alpha[i + 1:]
                        try:
                            first_beta = local_firsts[beta]
                        except KeyError:
                            first_beta = local_firsts[beta] = UtilsParsers.ComputeLocalFirst(firsts, beta)
                        change |= follow_symbol.Update(first_beta)
                        if first_beta.contains_epsilon or len(beta) == 0:
                            change |= follow_symbol.Update(follow_X)
        
        return follows

    @type_check
    def Register(table : dict, state : int, symbol, value) -> bool:

        if state not in table:
            table[state] = dict()

        row = table[state]
        
        if symbol not in row:
            row[symbol] = []

        cell = row[symbol]

        if value not in cell:
            cell.append(value)

        return len(cell) == 1
    