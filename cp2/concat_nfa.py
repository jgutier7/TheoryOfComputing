#!/usr/bin/env python3
import sys
from nfa_path import *
from converter import *

args = sys.argv

N1 = NFA()
N1.read_nfa(args[1])
N2 = NFA()
N2.read_nfa(args[2])
M = concat_nfa(N1, N2)

M.print_nfa()