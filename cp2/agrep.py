#!/usr/bin/env python3

# Grace Bezold, Jacob Guiterrez
from converter import *
from re_to_nfa import *
from parse_re import *

args   = sys.argv
re     = args[1]
re_nfa = re_to_nfa(re) # convert to nfa

for line in sys.stdin:
    w = line.strip()
    #check if matches the regex and print it out if so 
    matched = re_nfa.match(w) # match it
    if matched:
        print(w)
