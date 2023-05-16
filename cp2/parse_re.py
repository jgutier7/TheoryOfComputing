#!/usr/bin/env python3
'''Grace Bezold and Jacob Gutierrez'''

import sys

class Node:

    def __init__(self, value='', children=[], string_rep=''):
        self.value = value
        self.children = children
        self.string_rep = string_rep

    def __repr__(self):

        if self.children != []:
            string_rep = "(" + self.value + " " + " ".join([repr(x) for x in (self.children)]) + " " + ")"
        else:
            if self.value == 'epsilon':
                string_rep= "(" + self.value + ")"
            else:
                string_rep = '(symbol "' + self.value + '")' 
        
        return string_rep


#run the parser and convert input regexp into a string represenatation of the syntax tree for regexp
def parse_re(regex):

    stack = []
    
    #using ? as the terminal character
    regex = regex + '?'

    i = 0
    stack.append('$')
    
    #if it reads the right symbols, can pop the right symbols, has the correct below, has the correct next, then use that transition

    while 1:
        
        if regex[i] in {'a', 'b', 'c', 'd'} and stack[-1][0] == 'T':
            stack.append((regex[i]))
            i = i + 1
            continue

        elif regex[i] == '(' and stack[-1][0] == 'T':
            stack.append('(')
            i = i + 1
            continue

        elif regex[i] == ')' and stack[-1][0] == 'E':
            stack.append(')')
            i = i + 1
            continue

        elif regex[i] == '|' and stack[-1][0] == 'E':
            stack.append('|')
            i = i + 1
            continue

        elif regex[i] == '*' and stack[-1][0] == 'P':
            stack.append('*')
            i = i + 1
            continue

        elif stack[-1] == '$' or stack[-1] == '(' or stack[-1] == '|':

            tree12 = Node()
            tree12.value = 'epsilon'
            tree12.children = []

            stack.append(('T', tree12))
            #epsilon
            continue

        
        #add for all the alpha
        elif stack[-1][0] == 'P' and regex[i] in {'a','b', 'c', 'd', '(', ')', '|', '?'}:
            
            tree13 = Node()

            (sym, tree13) = stack.pop(-1)
            
            stack.append(('F', tree13))
            continue
        
        #add for all the alpha
 
        elif stack[-1] in {'a', 'b', 'c', 'd'}:
            
            tree14 = Node()

            sym = stack.pop(-1)

            tree14.value = sym
            tree14.children = []

            stack.append(('P', tree14))
            continue


        elif (len(stack) >= 2) and stack[-1][0] == 'T' and stack[-2] == '$' or stack[-2] == '(' and regex[i] in {'|', ')', '?'}:
                
                tree4 = Node()

                (sym, tree4) = stack.pop(-1)

                stack.append(('E', tree4))
                continue

        elif (len(stack) >= 2) and stack[-1][0] == 'F' and stack[-2][0] == 'T':

                tree5 = Node()
                tree6 = Node()

                (sym1, tree5) = stack.pop(-1)
                (sym2, tree6) = stack.pop(-1)

                tree7 = Node()
                tree7.value = 'concat'
                tree7.children = [tree6, tree5]

                stack.append(('T', tree7))
                #make new head which concats children
                continue

        elif (len(stack) >= 2) and stack[-1] == '*' and stack[-2][0] == 'P':
                
                tree8 = Node()
                
                stack.pop(-1)
                (sym, tree8) = stack.pop(-1)

                tree9 = Node()
                tree9.value = 'star'
                tree9.children = [tree8]

                stack.append(('F', tree9))
                continue
 

        elif (len(stack) >= 3) and stack[-1][0] == 'T' and stack[-2] == '|' and stack[-3][0] == 'E' and regex[i] in {'|', ')', '?'}:
                
                tree1 = Node()
                tree2 = Node()

                (sym, tree1) = stack.pop(-1)
                stack.pop(-1)
                (sym2,tree2) = stack.pop(-1)

                tree3 = Node()
                tree3.value = 'union'
                tree3.children = [tree2, tree1]
            
                stack.append(('E', tree3))
                continue


        elif (len(stack) >= 3) and stack[-1] == ')' and stack[-2][0] == 'E' and stack[-3] == '(':

                tree10 = Node()

                stack.pop(-1)
                (sym, tree10) = stack.pop(-1)
                stack.pop(-1)
                
                tree11 = Node()
                tree11.value = 'group'
                tree11.children = [tree10]

                stack.append(('P', tree11))
                #group
                continue
        

        if regex[i] == '?' and stack[-1][0] == 'E' and stack[-2] == '$':
            break
        
        #will this return __repr__?
    return stack[-1][1]

    
if __name__ == "__main__":
    print(parse_re(sys.argv[1]))
    


