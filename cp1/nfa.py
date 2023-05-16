#!/usr/bin/env python3

import sys

#file contains def of NFA M 
#1: list of states, Q
#2: whitespace list of symbols in the alphabet
#3: start state
#4: whitespace list of accept states
#5-end: transitions, one transistion/ line, leave from state symbol end state

#read a .nfa file into a dict containing the nfa elements
def read_nfa(file):
    f = open(file, "r")

    nfa = {}
    states = []
    alphabet = []
    accept_states = []
    transitions = []
    count = 0

    nfa["Q"] = states
    nfa["alpha"] = alphabet
    nfa["accept"] = accept_states
    nfa["transitions"] = transitions

    for line in f:

        line = line.rstrip()

        count += 1
        for symbol in line:
            if count == 1:
                states.append(symbol)
            elif count == 2:
                alphabet.append(symbol)
            elif count == 3:
                nfa["start"] = symbol
            elif count == 4:
                accept_states.append(symbol)
            else:
                transitions.append(line)
                break
    return nfa

    f.close()

#write definition of NFA M to file
def write_nfa(M, file):
    f = open(file, "w")

    for state in M["Q"]:
        f.write(state + " ")
    f.write("\n")

    for sym in M["alpha"]:
        f.write(sym + " ")
    f.write("\n")

    f.write(M["start"] + "\n")

    for state in M["accept"]:
        f.write(state + " ")
    f.write("\n")

    for transition in M["transitions"]:
        f.write(transition + "\n")

    f.close()


