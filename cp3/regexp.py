from collections import namedtuple
import nfa
import regular
from functools import reduce

class ParseError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

Symbol = namedtuple('Symbol', ['name'])
Expr = Symbol('E')
Term = Symbol('T')
Factor = Symbol('F')
Primary = Symbol('P')
Bottom = Symbol('$')
End = Symbol('⊣')

def parse(s):
    toks = list(s) + [End]
    stack = [Bottom]
    values = []
    pos = 0
    groupnum = 1
  
    while True:
        # Just for error messages
        if toks[pos] == End:
            next = "end of string"
        else:
            next = toks[pos]
            
        if stack == [Bottom, Expr] and toks[pos:] == [End]:
            return values[-1]
        
        elif (stack[-3:] == [Expr, '|', Term] and
              toks[pos] in ['|', ')', End]):
            tree = values[-2]
            if tree[0] != 'union':
                tree = ['union', tree, values[-1]]
            else:
                tree.append(values[-1])
            stack[-3:] = [Expr]
            values[-2:] = [tree]

        elif (stack[-1:] == [Term] and
              stack[-2] in [Bottom, '('] and
              toks[pos] in ['|', ')', End]):
            stack[-1:] = [Expr]

        elif stack[-2:] == [Term, Factor]:
            tree = values[-2]
            if tree[0] == 'epsilon':
                tree = values[-1]
            elif tree[0] != 'concat':
                tree = ['concat', tree, values[-1]]
            else:
                tree.append(values[-1])
            stack[-2:] = [Term]
            values[-2:] = [tree]

        elif stack[-1] in [Bottom, '(', '|']:
            stack.append(Term)
            values.append(['epsilon'])

        elif stack[-2:] == [Primary, '*']:
            stack[-2:] = [Factor]
            values[-1] = ['star', values[-1]]

        elif stack[-1] == Primary and toks[pos] != '*':
            stack[-1] = Factor

        elif isinstance(stack[-1], str) and stack[-1] not in ['(', ')', '|', '*', '\\']:
            sym = stack[-1]
            stack[-1] = Primary
            values.append(['symbol', sym])

        elif stack[-3:] == ['(', Expr, ')']:
            stack[-3:] = [Primary]
            values[-1] = ['group', groupnum, values[-1]]
            groupnum += 1

        elif stack[-1] == Term:
            if toks[pos] not in [')', '|', '*']:
                stack.append(toks[pos])
                pos += 1
            else:
                raise ParseError(f'expected symbol or ( but found {next}')

        elif stack[-1] == Expr:
            if toks[pos] in [')', '|']:
                stack.append(toks[pos])
                pos += 1
            else:
                raise ParseError(f'expected ) or | but found {next}')

        elif stack[-1] == Primary:
            if toks[pos] == '*':
                stack.append(toks[pos])
                pos += 1
            else:
                raise ParseError(f'expected * but found {next}')

        else:
            raise ParseError(f'unexpected {next}')

def to_nfa(alpha)->nfa:
    op, *args = alpha
    if op == 'union':
        return reduce(regular.union, map(to_nfa, args))
    elif op == 'concat':
        return reduce(regular.concat, map(to_nfa, args))
    elif op == 'star':
        return regular.star(to_nfa(args[0]))
    elif op == 'symbol':
        return regular.singleton(args)
    elif op == 'epsilon':
        return regular.singleton([])
    elif op == 'group':
        return regular.group(to_nfa(args[1]), args[0])
    else:
        raise NotImplementedError()


