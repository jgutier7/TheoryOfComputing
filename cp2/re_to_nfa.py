#!/usr/bin/env python3

import sys

# Grace Bezold, Jacob Gutierrez

#importing all functions
from converter import *
from parse_re import *
from nfa_path import*
from functools import *
import argparse

# def re_to_nfa(regexp):
#     #get the tree representation of the input
#     # tree = Node()
#     if type(regexp) == str:
#         pass
#     else:
#         regexp = str(regexp)

#     print(f'regexp type: {type(regexp)} REGEX: {regexp}')
#     tree = Node()
#     tree = parse_re(regexp)


#     #get to bottom of the tree
#     if tree.children != []: 
#         child_nfas = [re_to_nfa(child) for child in tree.children]

#         if tree.value == 'concat':
#             return concat_nfa(0,1)
#         elif tree.value == 'union':
#             return union_nfa(0,1)
#         elif tree.value == 'star':
#             return star_nfa(0,1)

    
#     else:
#         return string_nfa(tree.value)


def re_to_nfa(regexp) -> NFA:
    '''converts (the syntax tree of) a regular expression to an NFA, by walking the tree bottom-up '''
    # note: only use parse_re once
    # send it to node_to_nfa, which takes in anode as an argument 
    return node_to_nfa(parse_re(regexp)) 

def node_to_nfa(node):
    ''' regular expression to an equivalent NFA by going through it dnode by node '''
    print(f'node: {node} node value: {node.value}')
    # if node.value == 'symbol': 
    if node.value in {'a', 'b', 'c', 'd'}:
        print("returning string_nfa(symbol)")
        print(f'node.value {node.value}')
        return string_nfa(node.value)
    elif node.value == 'epsilon':
        # print("returning strin_nfa")
        return string_nfa('')
    elif node.value == 'union':
        nfa_list = []
        for child in node.children:
            nfa = node_to_nfa(child)
            nfa_list.append(nfa)
        result_nfa = nfa_list[0]
        for nfa in nfa_list[1:]:
            result_nfa = union_nfa(result_nfa, nfa)
        # print("returning union result")
        return result_nfa 
    elif node.value == 'concat':
        nfa_list = []
        for child in node.children:
            nfa = node_to_nfa(child)
            nfa_list.append(NFA(nfa))
        result_nfa = nfa_list[0]

        for nfa in nfa_list[1:]:
            result_nfa = concat_nfa(result_nfa, nfa)
        # print("returning cocat result")
        return result_nfa
    
    elif node.value == 'star':
        return star_nfa(node_to_nfa(node.children[0]))
    elif node.value == 'group':
        return node.value # didn't see that it should do nothing 
    else:
        print(node.value) 
        return

if __name__ == "__main__":
    # re_to_nfa(sys.argv[1])    
    parser = argparse.ArgumentParser()
    parser.add_argument('regex')
    args, ignore = parser.parse_known_args()            
    N = re_to_nfa(args.regex)
    N.print_nfa()