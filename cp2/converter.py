#!/usr/bin/env python3

import os
import sys
from nfa_path import *

# Grace Bezold, Jacob Gutierrez
''' This file holds fucntions for converter '''

def string_nfa(w: str):
    '''Creates an NFA that accepts exactly one string
    Args: 
        w: a string (possibly empty)
    Returns:
        an NFA recognizing the language {w}
    '''
    # create nfa
    M = NFA(Q=[], alpha=[], trans={}, start=None, accept=[])

    # create all the states, set up a dicitonary for those states to accomodate 
    for state in range(len(w)+1): # aight so this creates a state for each letter in the word + an extra state
        M.Q.append(f'q{state}')  
    for index in range(len(M.Q)): 
        M.trans[M.Q[index]] = {}

    # set start state
    M.start = ('q0')

    # add transitions
    for index in range(0, len(w)):
        # adding transitions where w[index] the symbol q{index} is where we are and q{index+1} is where the transition ends
        if w[index] not in M.trans[f'q{index}']: 
            M.trans[f'q{index}'][w[index]] = [f'q{index+1}'] 
        else:
            M.trans[f'q{index}'][w[index]].append(f'q{index+1}') # adds to dictionary IF not already in there  
        
    # add new characters to the alphabet 
    if len(w) == 0: # if empty 
        M.alpha.append('&')
    for index in range(0,len(w)):
        if w[index] not in M.alpha:
            M.alpha.append(w[index])

    # set end states
    M.accept.append(f'q{len(w)}')  

    # return created NFA
    return M


''' functions that perform the three regular operations, using the constructions given in the book '''

def union_nfa(N1: NFA,N2: NFA):
    ''' Performs a union by making a new NFA to combine the two languages
    args: 
        N1, N2: NFAs
    returns:
        NFA recognizing langauge L(N1) U L(N2)
    '''
    # Create a new start state called 'q0'
    new_start = ('q0')
    # Create a list of new states, new transtitions, new accepts
    new_states  = [new_start] # already have th enew start state there 
    new_trans   = {}
    new_accepts = []
    # Create a new alphabet that is the union of the alphabets of N1 and N2
    alpha1    = set(N1.alpha) 
    alpha2    = set(N2.alpha) 
    new_alpha = list(alpha1.union(alpha2)) # utilize the union method for sets and then convret it back to a list 

    # for each transition in N1, add a new transition to the new transitions set with updated state names that start with 'r'
    # For each state in N1, add a new state to the new states set with an updated name that starts with 'r'
    # right now i have it so it writes it as rq0, rq1, rq2... maybe change to indexes so it can just be r1, r2
    for state in N1.Q: 
        new_trans[f'r{state}'] = {}
        new_states.append(f'r{state}')
    for from_state, transitions in N1.trans.items():
        for symbol, to_states in transitions.items():
            for to_state in to_states:
                if symbol not in new_trans[f'r{from_state}']:
                    new_trans[f'r{from_state}'][symbol] = [f'r{to_state}'] 
                else:
                    new_trans[f'r{from_state}'][symbol].append(f'r{to_state}')

    # same thing we did for N1 but for N2 and instead of r start em with 's'
    for state in N2.Q: 
        new_trans[f's{state}'] = {}
        new_states.append(f's{state}')
    for from_state, transitions in N2.trans.items():
        for symbol, to_states in transitions.items():
            for to_state in to_states:
                if symbol not in new_trans[f's{from_state}']:
                    new_trans[f's{from_state}'][symbol] = [f's{to_state}'] 
                else:
                    new_trans[f's{from_state}'][symbol].append(f's{to_state}')

    # Add epsilon transitions from the new start state to the old start states in N1 and N2 with updated state names
    new_trans[f'{new_start}'] = {}
    new_trans[f'{new_start}']['&'] = ['sq1','rq1']

    # Add each of N1's accept states to the new accept states set with updated state names that start with 'r'
    for state in N1.accept:
        new_accepts.append(f'r{state}')
    # Add each of N2's accept states to the new accept states set with updated state names that start with 's'
    for state in N2.accept:
        new_accepts.append(f's{state}')

    # Create a new NFA with the updated states, alphabet, start state, accept states, and transitions and return it
    return NFA(new_states, new_alpha, new_trans, new_start, new_accepts)


def concat_nfa(N1: NFA,N2:NFA):
    ''' Performs a concat
    args: 
        N1, N2: NFAs
    returns:
        NFA recognizing langauge L(N1) o L(N2)
    '''   
    # create everything for the new NFA (same thing as unioon)
     # Create a new start state called 'q0'
    new_start = ('q0')
    # Create a list of new states, new transtitions, new accepts
    new_states  = [new_start] # already have th enew start state there 
    new_trans   = {}
    new_accepts = []
    # Create a new alphabet that is the union of the alphabets of N1 and N2
    alpha1    = set(N1.alpha) 
    alpha2    = set(N2.alpha) 
    new_alpha = list(alpha1.union(alpha2)) # utilize the union method for sets and then convret it back to a list 

    # add and rename stufff from N1 and N2 like done in union
    for state in N1.Q: 
        new_trans[f'r{state}'] = {}
        new_states.append(f'r{state}')
    for from_state, transitions in N1.trans.items():
        for symbol, to_states in transitions.items():
            for to_state in to_states:
                if symbol not in new_trans[f'r{from_state}']:
                    new_trans[f'r{from_state}'][symbol] = [f'r{to_state}'] 
                else:
                    new_trans[f'r{from_state}'][symbol].append(f'r{to_state}')
    for state in N2.Q: 
        new_trans[f's{state}'] = {}
        new_states.append(f's{state}')
    for from_state, transitions in N2.trans.items():
        for symbol, to_states in transitions.items():
            for to_state in to_states:
                if symbol not in new_trans[f's{from_state}']:
                    new_trans[f's{from_state}'][symbol] = [f's{to_state}'] 
                else:
                    new_trans[f's{from_state}'][symbol].append(f's{to_state}')

    # epsilon transitions from N1's accept states to N2's start state
    # Add each of N1's accept states to the new accept states set with updated state names that start with 'r'
    for old_accept_state in N1.accept:
        if '&' not in new_trans[f'r{old_accept_state}']:
            new_trans[f'r{old_accept_state}']['&'] = ['sq1']  
        else:
            new_trans[f'r{old_accept_state}']['&'].append('sq1')
    
    # add transition from new start state to N1's start 
    new_trans[f'{new_start}'] = {}
    new_trans[f'{new_start}']['&'] = ['rq1']

    # Add each of N2's accept states to the new accept states set with updated state names that start with 's'
    for state in N2.accept:
        new_accepts.append(f's{state}')
    # Create a new NFA with the concatenated states, alphabet, start state, accept states, and transitions

    return NFA(new_states, new_alpha, new_trans, new_start, new_accepts) 


def star_nfa(N: NFA):
    ''' Performs the kleene star
    args: 
        N: an NFA
    returns:
        NFA recognizing langauge L(N)*
    '''
    # create a new start state, new accept state, and new set of states literally exactly like union and concat 
    new_start   = ('q0')
    new_accepts = []
    new_accepts.append(new_start)
    new_states  = [new_start] # already have th enew start state there 
    new_trans   = {}
    new_alpha   = N.alpha

    # add and rename stufff from N like done in union and concat
    for state in N.Q: 
        new_trans[f'r{state}'] = {}
        new_states.append(f'r{state}')
    for from_state, transitions in N.trans.items():
        for symbol, to_states in transitions.items():
            for to_state in to_states:
                if symbol not in new_trans[f'r{from_state}']:
                    new_trans[f'r{from_state}'][symbol] = [f'r{to_state}'] 
                else:
                    new_trans[f'r{from_state}'][symbol].append(f'r{to_state}')
    
    # for each accept state in the old NFA, add an epsilon transition to q0 (the start)
    for old_accept_state in N.accept:
        if '&' not in new_trans[f'r{old_accept_state}']:
            new_trans[f'r{old_accept_state}']['&'] = ['q0']  
        else:
            new_trans[f'r{old_accept_state}']['&'].append('q0')

    # add a transition from new start, symbol &, to N's original start state
    new_trans[f'{new_start}'] = {}
    new_trans[f'{new_start}']['&'] = ['rq1']

    # create and return the new NFA using the updated start state, accept states, states, and transitions
    return NFA(new_states, new_alpha, new_trans, new_start, new_accepts) 


# ''''testing converter functions'''
# # testing string_nfa
# M = string_nfa('this is a string')
# N = string_nfa(' and another one')

# # testing union
# print('\nTesting union')
# unfa = union_nfa(M,N)
# unfa.match('this is a string')
# unfa.match(' and another one')

# #testing concat
# print('\ntesting concat')
# cnfa = concat_nfa(M,N)
# cnfa.match('this is a string and another one')

# #testing star
# print('\ntesting star')
# snfa = star_nfa(M)
# print('testing: this is a stringthis is a stringthis is a string')
# snfa.match('this is a stringthis is a stringthis is a string')