#!/usr/bin/env python3

import nfa
import regular
import sys

m1 = nfa.read(open(sys.argv[1]))
ms = regular.star(m1)
nfa.write(ms, sys.stdout)


