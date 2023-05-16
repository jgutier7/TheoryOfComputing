#!/usr/bin/env python3

import nfa
import regular
import sys

m1 = nfa.read(open(sys.argv[1]))
m2 = nfa.read(open(sys.argv[2]))
mu = regular.union(m1, m2)
nfa.write(mu, sys.stdout)


