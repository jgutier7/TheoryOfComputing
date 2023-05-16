#!/usr/bin/env python3

import sys
from nfa_path import *
from converter import *

args = sys.argv[1]
NFA = string_nfa(args)
NFA.print_nfa()