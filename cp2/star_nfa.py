#!/usr/bin/env python3

import sys
from nfa_path import *
from converter import *

args = sys.argv

N1 = NFA()
N1.read_nfa(args[1])
M = star_nfa(N1)

M.print_nfa()