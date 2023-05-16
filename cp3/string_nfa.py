#!/usr/bin/env python3

import nfa
import regular
import sys

m = regular.singleton(sys.argv[1])
nfa.write(m, sys.stdout)


