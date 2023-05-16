#!/usr/bin/env python3

from collections import namedtuple
import nfa
import regular
import backref
import sys
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

    # print(toks)
    length = len(toks) - 1
    while pos < length:
        length = len(toks) - 1
        # print(toks[pos])
        # print(toks[pos:pos+3]) 
        if toks[pos:pos+3] == ['\\','g','<']:
            first = toks.pop(pos+1)
            # print(first)
            second = toks.pop(pos+1)
            toks[pos] = toks[pos] + first + second 
            # print('in')
            j = pos + 1
            # print(toks[j])
            while(j < len(toks)-1 and toks[j] in ['0','1','2','3','4','5','6','7','8','9']):
                toks[pos] += toks.pop(j)
            toks[pos] += toks.pop(j)
            pos + 4
        elif toks[pos] == '\\':
            j = pos + 1
            # print(j)
            while(j < len(toks)-1 and toks[j] in ['0','1','2','3','4','5','6','7','8','9']):
                # toks[i].append(toks.pop(j))
                toks[pos] += toks.pop(j)
                # print(f'new toks: {toks[pos]}')
            
        pos += 1
    # print(toks)

    # print(toks)

    # for i in range(len(toks)):
    #     if toks[i] == '/':
    #         backref_num, j = parse_number(toks[i:], i+1)
    #         i = j
    
    pos = 0

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

        elif isinstance(stack[-1], str) and stack[-1] not in ['(', ')', '|', '*', '\\'] and stack[-1][0] != '\\':
            sym = stack[-1]
            stack[-1] = Primary
            values.append(['symbol', sym])

        #second two CP4 transitions
        elif isinstance(stack[-1], str) and stack[-1] not in ['(', ')', '|', '*']:
            k = ''
            ref = stack[-1]
            i = 1
            if ref[1] == 'g':
                i = 3
            while (i <= len(ref) - 1 and ref[i] in ['0','1','2','3','4','5','6','7','8','9']):
                k += ref[i]
                i += 1
            stack[-1] = Primary
            values.append(['backref', k])

        elif stack[-3:] == ['(', Expr, ')']:
            stack[-3:] = [Primary]
            values[-1] = ['group', values[-1]]
        
        #this should take care of the first CP4 transitions?
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

def to_nfa(alpha):
    group = 1
    def visit(alpha):
        nonlocal group
        op, *args = alpha
        if op == 'union':
            return reduce(regular.union, map(visit, args))
        elif op == 'concat':
            return reduce(regular.concat, map(visit, args))
        elif op == 'star':
            return regular.star(visit(args[0]))
        elif op == 'symbol':
            return regular.singleton(args)
        elif op == 'epsilon':
            return regular.singleton([])
        elif op == 'group':
            thisgroup = group
            group += 1
            return regular.group(visit(args[0]), thisgroup)
        elif op == 'backref':
            m = regular.backref(args[0])
            # nfa.write(m, sys.stdout)
            return m
        else:
            raise NotImplementedError()
    return visit(alpha)


#parse('(a)\\1\g<1>')
# parse('(a)\\1\\10')
