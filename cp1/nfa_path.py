#!/usr/bin/env python3
''' Grace Bezold and Jacob Gutierrez '''

import sys

class NFA:    

    def __init__(self, Q=[], alpha=[], trans={}, start=None, accept=[]):
        ''' NFA with attributes: Q: states, alpha: alphabet, trans: transtions, start state, accept state'''
        self.Q      = Q
        self.alpha  = alpha
        self.trans  = trans
        self.start  = start
        self.accept = accept

    
    def read_nfa(self, file):
        '''Reads file containing NFA M, Retruns the NFA M'''
        # open de file and save lines to lines w/ readlines()
        f        = open(file, "r")
        lines    = f.readlines()
        file_end = len(lines)

        #strip the whitespace ffrom said lines
        for i in range(file_end):
            lines[i] = lines[i].strip()

        #indexes for accessing the lines for the specific attribtues from the input file
        states_i = 0 # first line
        alpha_i  = 1 # second line, etc.
        start_i  = 2
        accept_i = 3
        trans_i  = 4

        self.Q      = lines[states_i].split() # states
        self.alpha  = lines[alpha_i].split()  # alphabet
        self.start  = lines[start_i]          # start state
        self.accept = lines[accept_i].split() # accept state

        # transitons, saved as a dictionary 
        # disctionary of transitions where each transition has a dictinoary 
        # format for the transitions ------> { state, { symbol, [ending_states] } }
        self.trans = {}

        # loops through the number of states and sets up the  dictionary 
        for i in range(len(self.Q)):
            self.trans[self.Q[i]] = {}

        # indexes to parse the rest of the lines which list the transitions 
        q = 0 # the state that the transition leaves from
        a = 1 # the symbol that the transtion reads, or & for the empty string 
        r = 2 # the state that the transition goes to 
        # loops through the last lines (starting at transition index) and splits those lines and saves them 
        for i in range(trans_i, file_end): 
            lines[i] = lines[i].split()
            # make sure a trnasition is unique, such that "each configuration appears only once with two incoming edges"
            if lines[i][a] not in self.trans[lines[i][q]]:  # this line should ensure that ^
                self.trans[lines[i][q]][lines[i][a]] = [lines[i][r]]
            else: # else add that transition to the state and symbol that are already there
                self.trans[lines[i][q]][lines[i][a]].append(lines[i][r])
        
        # close the file
        f.close()

    def write_nfa(self, file_path):
        '''This writes the NFA M to a file. This function takes in M as the NFA to write and the file path to write to. '''
        # note: use with open(...) as file for write_nfa 
        with open(file_path, 'w') as file:
            # Write the states to the file
            file.write(" ".join(self.Q))
            file.write("\n")
            
            # Write the alphabet to the file
            file.write(" ".join(self.alpha))
            file.write("\n")
            
            # Write the start state to the file
            file.write(self.start)
            file.write("\n")
            
            # Write the accept states to the file
            file.write(" ".join(self.accept))
            file.write("\n")
            
            # Write the transitions to the file
            for state, trans_mapping in self.trans.items():
                for symbol, trans_list in trans_mapping.items():
                    for target_state in trans_list:
                        file.write(f'{state} {symbol} {target_state}\n')


    def match(self, w):
        '''The tests whether the NFA accepts the string w'''
        #list of nodes to visit during the breadth first search
        nodes_to_visit = [(self.start, 0)]
        # visited -> { (state,level) : (prev_state, level, 'symbol') } #thankyouTAs
        visited = {}

        # checks the state of the match
        accepted = False
    
        while nodes_to_visit:
            #pop from front of the list because breadth first search
            node = nodes_to_visit.pop(0)
            state = node[0]
            level = node[1]
            
            # check if it is the last letter of the string there are no more transitions
            if level == len(w) and state in self.accept: 
                # final_node = (state, level) # saves the final state and level 
                accepted = True
                break

            # check if there are still symbols to read AND check if symbol has other transitions 
            if level < (len(w)):
                sym = w[level]
                if sym in self.trans[state]:
                    #add each new state to nodes_to_visit, but move onto the next char in string
                    for curr_node in self.trans[state][sym]: # loop through next symbol
                        if (curr_node, level + 1) not in visited: # if this next node hasn't been visitied yet
                            new_node = (curr_node, level + 1)
                            nodes_to_visit.append(new_node) # add it to our list for nodes to visit
                            # add it to our dictionary for visited, where the value is the state, level, and the symbol
                            visited[new_node] = (state, level, sym) 
            
            #if the state has empty string transitions
            if '&' in self.trans[state]: 
                # loop through it's destiantions
                for curr_node in self.trans[state]['&']:                  
                    #add each new state to nodes_to_visit, same level b/c empty transition
                    if (curr_node, level) not in visited:
                        new_node = (curr_node,level)
                        nodes_to_visit.append(new_node)
                        visited[new_node] = (state, level, '&')

        if accepted is False:
            print("reject")
            return False
        else: # we found a match
            print("accept")
            # node is the most currently popped item and since it was accepted, the last part of the path
            # therefore, we can go backwards fromt here in visited and construct the final path, then reverse that list 
            found_path = [node] #starts with node

            # while count != len(w):
            while node in visited:
                node = visited[node][0:2] # the [0:2] is to get the prev_state, level, symbol
                found_path.append(node) # adds it to the path

            # reverse this path
            found_path.reverse()

            # Iterates through the identified path (excluding the first item since that's the start state we started with at level 0) and prints the path
            for node in found_path[1:]:
                print(f'{visited[node][0]} {visited[node][2]} {node[0]}')
            
            return True


if len(sys.argv) != 3:
    print('''Usage: ./nfa_path {path to NFA file} "{string to match}"''')
    sys.exit(0)

path = sys.argv[1] # gets the file path to the NFA
w    = sys.argv[2] # gets the string to match 
M    = NFA()

# read and match
M.read_nfa(path)
M.match(w)
exit(0)
